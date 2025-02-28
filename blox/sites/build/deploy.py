import os
import subprocess
import sys
import click
import socket
from typing import List
from ...utils.config import PROJECT_ROOT, write_running_ports
import platform

def run_with_sudo(command):
    """Run a command with sudo privileges."""
    subprocess.run(["sudo"] + command, check=True)

def detect_package_manager():
    """Detect the package manager based on the OS distribution."""
    distro = platform.system().lower()

    if distro == "linux":
        try:
            with open("/etc/os-release") as f:
                os_info = f.read().lower()
                if "almalinux" in os_info:
                    return "dnf"
        except FileNotFoundError:
            pass
    return None

def install_required_packages():
    """
    Ensure all required packages are installed based on AlmaLinux.
    """
    package_manager = detect_package_manager()
    
    if package_manager == "dnf":
        packages = ["apache2", "certbot", "python3-certbot-dns", "supervisor"]
        run_with_sudo([package_manager, "install", "-y"] + packages)
        run_with_sudo(["systemctl", "enable", "apache2", "supervisord"])
    else:
        click.echo("Unsupported OS. Please install the required packages manually.", err=True)

def find_free_port(start_port: int = 3000) -> int:
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("localhost", port)) != 0:
                return port
            port += 1

def setup_apache2(domain: str, appname: str, django_port: int, nextjs_port: int):
    """
    Set up Apache2 configuration for Django and Next.js on AlmaLinux.
    """
    conf_path = f"/etc/apache2/sites-available/{appname}.conf"
    
    # Ensure the directory exists
    run_with_sudo(["mkdir", "-p", "/etc/apache2/sites-available"])
    
    apache2_conf = f"""
<VirtualHost *:80>
    ServerName {domain}
    DocumentRoot {PROJECT_ROOT}/frontend

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:{nextjs_port}/
    ProxyPassReverse / http://127.0.0.1:{nextjs_port}/

    <Directory {PROJECT_ROOT}/frontend>
        Require all granted
    </Directory>
</VirtualHost>

<VirtualHost *:80>
    ServerName api.{domain}
    DocumentRoot {PROJECT_ROOT}/backend

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:{django_port}/
    ProxyPassReverse / http://127.0.0.1:{django_port}/

    <Directory {PROJECT_ROOT}/backend>
        Require all granted
    </Directory>
</VirtualHost>
"""
    run_with_sudo(["bash", "-c", f"echo '{apache2_conf}' | tee {conf_path}"])
    run_with_sudo(["a2ensite", appname])
    run_with_sudo(["systemctl", "restart", "apache2"])
    click.echo(f"Apache2 configuration for {appname} has been set up.")

def setup_supervisor(appname: str, django_port: int, nextjs_port: int):
    logs_dir = os.path.join(PROJECT_ROOT, "logs")
    run_with_sudo(["mkdir", "-p", logs_dir])
    django_log = os.path.join(logs_dir, f"{appname}_django.log")
    nextjs_log = os.path.join(logs_dir, f"{appname}_nextjs.log")

    username = click.prompt("Enter the username to run the Supervisor process", type=str)
    
    supervisor_conf = f"""
[program:{appname}_django]
command={PROJECT_ROOT}/env/bin/gunicorn --bind 0.0.0.0:{django_port} {appname}.wsgi:application
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
    conf_path = f"/etc/supervisord.d/{appname}.ini"
    run_with_sudo(["bash", "-c", f"echo '{supervisor_conf}' | tee {conf_path}"])
    run_with_sudo(["systemctl", "restart", "supervisord"])
    click.echo(f"Supervisor configuration for {appname} has been set up and started.")

def setup_ssl(domain: str):
    click.echo("Setting up SSL with Let's Encrypt...")
    run_with_sudo(["certbot", "--apache", "-d", domain, "-d", f"www.{domain}"])
    click.echo(f"SSL certificate for {domain} has been set up.")

def undo_setup(appname: str):
    """
    Undo the setup in case of failure.
    """
    click.echo("Rolling back setup...")
    run_with_sudo(["rm", "-f", f"/etc/apache2/sites-available/{appname}.conf"])
    run_with_sudo(["a2dissite", appname])
    run_with_sudo(["systemctl", "restart", "apache2", "supervisord"])
    click.echo("Setup has been undone.")

@click.command()
@click.argument("mode", default="prod")
def deploy(mode: str):
    django_port = find_free_port(8000)
    nextjs_port = find_free_port(3000)
    domain = click.prompt("Enter your domain name", type=str)
    appname = click.prompt("Enter your app name", type=str)
    try:
        # install_required_packages()
        setup_apache2(domain, appname, django_port, nextjs_port)
        setup_supervisor(appname, django_port, nextjs_port)
        # setup_ssl(domain)
        # write_running_ports(django_port, nextjs_port)
        click.echo("Deployment is complete. The services are running in the background.")
    except Exception as e:
        click.echo(f"Error occurred: {e}", err=True)
        undo_setup(appname)
