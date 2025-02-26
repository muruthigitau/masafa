import os
import click
import subprocess

def run_with_sudo(command):
    """Run a command with sudo privileges."""
    subprocess.run(["sudo"] + command, check=True)

def clear_all_nginx_supervisor():
    """Completely reset Nginx and Supervisor to default settings."""
    click.echo("Removing all Nginx and Supervisor configurations...")
    
    # Stop Nginx and Supervisor
    run_with_sudo(["systemctl", "stop", "nginx"])
    run_with_sudo(["systemctl", "stop", "supervisor"])
    
    # Remove all Nginx configurations
    run_with_sudo(["rm", "-rf", "/etc/nginx/sites-available/*"])
    run_with_sudo(["rm", "-rf", "/etc/nginx/sites-enabled/*"])
    run_with_sudo(["rm", "-rf", "/etc/nginx/conf.d/*"])
    run_with_sudo(["rm", "-f", "/etc/nginx/nginx.conf"])
    
    # Restore default Nginx configuration
    run_with_sudo(["apt-get", "--reinstall", "install", "nginx", "-y"])
    
    # Remove all Supervisor configurations
    run_with_sudo(["rm", "-rf", "/etc/supervisor/conf.d/*"])
    run_with_sudo(["rm", "-f", "/etc/supervisor/supervisord.conf"])
    
    # Restart services
    run_with_sudo(["systemctl", "restart", "nginx"])
    run_with_sudo(["systemctl", "restart", "supervisor"])
    
    # Enable services on startup
    run_with_sudo(["systemctl", "enable", "nginx"])
    run_with_sudo(["systemctl", "enable", "supervisor"])
    
    click.echo("Nginx and Supervisor have been reset to default settings.")

@click.command()
def clear_deploy():
    """CLI command to fully reset Nginx and Supervisor."""
    clear_all_nginx_supervisor()

