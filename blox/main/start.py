import json
import os
import socket
import subprocess
import threading
import traceback
import sys
import click

from ..utils.config import (PROJECT_ROOT, SITES_JSON_PATH,
                            write_running_ports)
from ..utils.initialize_django import initialize_django_env
from ..utils.run_process import get_python_executable, run_subprocess

def find_free_port(start_port=3000):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("localhost", port)) != 0:
                return port
            port += 1


def stream_reader(stream, color, prefix="", first_line_only=False):
    """Reads from a stream and prints lines with a given color and optional prefix."""
    first_line = True
    for line in iter(stream.readline, ""):
        if line:
            line = line.strip()
            if first_line_only:
                if first_line:
                    click.echo(click.style(prefix, fg="red"), nl=False)
                    first_line = False
            if line:
                click.echo(click.style(f"{line}", fg=color))


@click.command()
@click.argument("mode", default="prod")
def start(mode):
    """Start Django and Next.js servers for the specified site."""
    click.echo("Starting server")

    # Create Django and Next.js paths
    django_path = os.path.join(
        PROJECT_ROOT, "backend"
    )
    nextjs_path = os.path.join(
        PROJECT_ROOT
    )

    python_executable = get_python_executable()

    django_port = find_free_port(8000)
    nextjs_port = find_free_port(3000)

    django_process = None
    nextjs_process = None

    try:

        # Determine Next.js command based on mode
        nextjs_command = (
            ["npm", "run", "start"]
            if mode == "prod"
            else ["npm", "run", "dev", "--", "--port", str(nextjs_port)]
        )

        # Start Next.js process
        nextjs_process = run_subprocess(nextjs_command, cwd=nextjs_path)

        # time.sleep(3)
        initialize_django_env()

        django_process = run_subprocess(
            [python_executable, "manage.py", "runserver", f"0.0.0.0:{django_port}"],
            cwd=django_path,
        )

        write_running_ports(django_port, nextjs_port)

        # Start threads to read stdout and stderr from both processes
        django_stdout_thread = threading.Thread(
            target=stream_reader, args=(django_process.stdout, "white")
        )
        django_stderr_thread = threading.Thread(
            target=stream_reader,
            args=(django_process.stderr, "bright_black", "Django warning: ", True),
        )
        nextjs_stdout_thread = threading.Thread(
            target=stream_reader, args=(nextjs_process.stdout, "white")
        )
        nextjs_stderr_thread = threading.Thread(
            target=stream_reader,
            args=(nextjs_process.stderr, "bright_black", "Next.js warning: ", True),
        )

        nextjs_stdout_thread.start()
        nextjs_stderr_thread.start()
        django_stdout_thread.start()
        django_stderr_thread.start()

        # Load site names from SITES_JSON_PATH
        with open(SITES_JSON_PATH, 'r') as f:
            sites = json.load(f)

        # Generate and display links for all sites
        for site in sites:
            site_name = site.get('site_name', '')
            if site_name:
                click.echo(
                    click.style(f"Open {site_name} at: http://{site_name}.localhost:{nextjs_port}\n", fg="green")
                )

        try:
            django_process.wait()
            nextjs_process.wait()
        except KeyboardInterrupt:
            click.echo("Stopping blox...")
            if django_process:
                django_process.terminate()
                try:
                    django_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    django_process.kill()
            if nextjs_process:
                nextjs_process.terminate()
                try:
                    nextjs_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    nextjs_process.kill()
            django_stdout_thread.join()
            django_stderr_thread.join()
            nextjs_stdout_thread.join()
            nextjs_stderr_thread.join()

    except Exception as e:
        click.echo(click.style(f"Exception: {str(e)}", fg="red"))
        exc_type, exc_value, exc_tb = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_tb)
        
    finally:
        if django_process and django_process.poll() is None:
            django_process.terminate()
            try:
                django_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                django_process.kill()
        if nextjs_process and nextjs_process.poll() is None:
            nextjs_process.terminate()
            try:
                nextjs_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                nextjs_process.kill()