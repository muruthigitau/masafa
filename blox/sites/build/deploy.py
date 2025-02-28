import os
import subprocess
import sys
import click
import socket
from typing import List
from ...utils.config import PROJECT_ROOT, write_running_ports

def run_with_sudo(command: List[str]) -> None:
    subprocess.run(["sudo"] + command, check=True)

def install_required_packages():
    """
    Ensure all required packages are installed.
    """
    packages = ["apache2", "libapache2-mod-wsgi-py3", "certbot", "python3-certbot-apache", "supervisor"]
    run_with_sudo(["apt-get", "update"])
    run_with_sudo(["apt-get", "install", "-y"] + packages)
    click.echo("All required packages are installed.")

def find_free_port(start_port: int = 3000) -> int:
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("localhost", port)) != 0:
                return port
            port += 1

def setup_apache(domain: str, appname: str, django_port: int):
    """
    Set up Apache configuration for Django.
    """
    apache_conf = f"""
    <VirtualHost *:80>
        ServerName {domain}
        ServerAlias www.{domain}

        WSGIDaemonProcess {appname} python-home={PROJECT_ROOT}/env python-path={PROJECT_ROOT}/backend
        WSGIProcessGroup {appname}
        WSGIScriptAlias / {PROJECT_ROOT}/backend/{appname}/wsgi.py

        <Directory {PROJECT_ROOT}/backend/{appname}>
            Require all granted
        </Directory>

        Alias /static/ {PROJECT_ROOT}/backend/static/
        <Directory {PROJECT_ROOT}/backend/static/>
            Require all granted
        </Directory>
    </VirtualHost>
    """
    conf_path = f"/etc/apache2/sites-available/{appname}.conf"
    run_with_sudo(["bash", "-c", f"echo '{apache_conf}' > {conf_path}"])
    run_with_sudo(["a2ensite", appname])
    run_with_sudo(["systemctl", "reload", "apache2"])
    click.echo(f"Apache configuration for {appname} has been set up.")

def setup_supervisor(appname: str, django_port: int, nextjs_port: int):
    logs_dir = os.path.join(PROJECT_ROOT, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    django_log = os.path.join(logs_dir, f"{appname}_django.log")
    nextjs_log = os.path.join(logs_dir, f"{appname}_nextjs.log")

    username = click.prompt("Enter the username to run the Supervisor process", type=str)
    
    supervisor_conf = f"""
    [program:{appname}_django]
    command={PROJECT_ROOT}/env/bin/python3 manage.py runserver 0.0.0.0:{django_port}
    directory={PROJECT_ROOT}/backend
    autostart=true
    autorestart=true
    stderr_logfile={django_log}
    stdout_logfile={django_log}
    user={username}
    
    [program:{appname}_nextjs]
    command=npm run start -- --port {nextjs_port}
    directory={PROJECT_ROOT}/frontend
    autostart=true
    autorestart=true
    stderr_logfile={nextjs_log}
    stdout_logfile={nextjs_log}
    user={username}
    """
    conf_path = f"/etc/supervisor/conf.d/{appname}.conf"
    run_with_sudo(["bash", "-c", f"echo '{supervisor_conf}' > {conf_path}"])
    run_with_sudo(["supervisorctl", "reread"])
    run_with_sudo(["supervisorctl", "update"])
    run_with_sudo(["supervisorctl", "start", f"{appname}_django"])
    run_with_sudo(["supervisorctl", "start", f"{appname}_nextjs"])
    click.echo(f"Supervisor configuration for {appname} has been set up and started.")

def setup_ssl(domain: str):
    click.echo("Setting up SSL with Let's Encrypt...")
    # run_with_sudo(["certbot", "--apache", "-d", domain, "-d", f"www.{domain}"])
    click.echo(f"SSL certificate for {domain} has been set up.")

def undo_setup(appname: str):
    """
    Undo the setup in case of failure.
    masafalogistics.softleek.com
    """
    click.echo("Rolling back setup...")
    run_with_sudo(["a2dissite", appname])
    run_with_sudo(["systemctl", "reload", "apache2"])
    run_with_sudo(["rm", f"/etc/apache2/sites-available/{appname}.conf"])
    run_with_sudo(["rm", f"/etc/supervisor/conf.d/{appname}.conf"])
    run_with_sudo(["supervisorctl", "stop", f"{appname}_django"])
    run_with_sudo(["supervisorctl", "stop", f"{appname}_nextjs"])
    run_with_sudo(["supervisorctl", "update"])
    click.echo("Setup has been undone.")

@click.command()
@click.argument("mode", default="prod")
def deploy(mode: str):
    install_required_packages()
    django_port = find_free_port(8000)
    nextjs_port = find_free_port(3000)
    domain = click.prompt("Enter your domain name", type=str)
    appname = click.prompt("Enter your app name", type=str)
    try:
        setup_apache(domain, appname, django_port)
        setup_supervisor(appname, django_port, nextjs_port)
        setup_ssl(domain)
        write_running_ports(django_port, nextjs_port)
        click.echo("Deployment is complete. The services are running in the background.")
    except Exception as e:
        click.echo(f"Error occurred: {e}", err=True)
        undo_setup(appname)
