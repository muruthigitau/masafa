import os
import subprocess
import sys
import traceback
from typing import NoReturn

import click
from ..utils.config import PROJECT_ROOT


@click.command()
def build() -> NoReturn:
    """
    Build the project by collecting Django static files and building the Next.js project.

    This function checks for the existence of a virtual environment, collects Django static files,
    and builds the Next.js project. If any step fails, it prints an error message.
    """
    venv_path: str = os.path.join(PROJECT_ROOT, "env")
    if not os.path.exists(venv_path):
        click.echo("Virtual environment not found. Please run 'blox setup' first.")
        return

    python_executable: str = os.path.join(venv_path, "bin", "python3")
    if sys.platform.startswith("win"):
        python_executable = os.path.join(venv_path, "Scripts", "python.exe")

    try:
        # Build Django static files
        click.echo(click.style("Building Django static files...", fg="blue"))
        subprocess.check_call(
            [python_executable, "manage.py", "collectstatic", "--noinput"],
            cwd=os.path.join(PROJECT_ROOT, "apps/core/django"),
        )
        click.echo(click.style("Django static files built successfully.", fg="green"))

        # Build Next.js project
        click.echo(click.style("Building Next.js project...", fg="blue"))
        subprocess.check_call(
            ["npm", "run", "build"], cwd=os.path.join(PROJECT_ROOT, "apps/core/nextjs")
        )
        click.echo(click.style("Next.js project built successfully.", fg="green"))

    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Build failed: {str(e)}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred: {str(e)}", fg="red"))
        exc_type, exc_value, exc_tb = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_tb)
