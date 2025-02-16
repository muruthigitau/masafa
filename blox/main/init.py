import json
import os
import subprocess
import click
import tempfile
import shutil
from typing import List, Any

from ..utils.file_operations import ensure_file_exists

@click.command()
@click.argument("name", required=False, default=".")
def init(name: str) -> None:
    """
    Initialize a new project similar to bench init.

    :param name: The name of the project directory.
    """
    perform_init(name)
    
def perform_init(name: str) -> None:
    """
    Initialize a new project similar to bench init.

    :param name: The name of the project directory.
    """
    
    # Determine project root
    project_root: str = os.path.abspath(name)
    if name != ".":
        os.makedirs(project_root, exist_ok=True)
    
    # Define necessary directories
    directories: List[str] = ["apps", "config", "logs", "sites"]
    for directory in directories:
        os.makedirs(os.path.join(project_root, directory), exist_ok=True)
    
    # Create necessary files
    sites_json_path: str = os.path.join(project_root, "sites", "sites.json")
    procfile_path: str = os.path.join(project_root, "Procfile") 
    blox_config_path: str = os.path.join(project_root, "blox.config") 
    
    ensure_file_exists(sites_json_path, initial_data=[])
    ensure_file_exists(blox_config_path, initial_data=[])
    
    with open(procfile_path, "w") as procfile:
        procfile.write("""
web: blox start
redis_cache: redis-server config/redis_cache.conf
redis_queue: redis-server config/redis_queue.conf
worker: blox worker
schedule: blox schedule
""")
    
    # Clone mainsite into sites/default
    core_apps_path: str = os.path.join(project_root, "apps", "core")
    repo_url: str = "https://github.com/Softleek/blox-core.git"
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            subprocess.check_call(["git", "clone", repo_url, temp_dir])
        except subprocess.CalledProcessError as e:
            click.echo(f"Failed to clone the repository: {e}")
            return

        # Ensure the sites directory exists
        os.makedirs(core_apps_path, exist_ok=True)

        # Move the cloned repository to the sites directory
        for item in os.listdir(temp_dir):
            shutil.move(os.path.join(temp_dir, item), core_apps_path)

    try:
        with open(sites_json_path, "r") as json_file:
            sites: List[dict[str, Any]] = json.load(json_file) or []
    except json.JSONDecodeError:
        sites = []
    
    # Assign available ports
    django_ports: List[int] = [site.get("django_port") for site in sites]
    next_django_port: int = 8000
    while next_django_port in django_ports:
        next_django_port += 1
    
    nextjs_ports: List[int] = [site.get("nextjs_port") for site in sites]
    next_nextjs_port: int = 3000
    while next_nextjs_port in nextjs_ports:
        next_nextjs_port += 1
    
    # Update sites.json
  
    with open(sites_json_path, "w") as json_file:
        json.dump(sites, json_file, indent=4)
    
    click.echo("Project initialized successfully!")
    
    # Run post-install commands
    try:
        subprocess.check_call(["blox", "install"])
        subprocess.check_call(["blox", "migrate"])
        subprocess.check_call(["blox", "django", "createsuperuser"])
        click.echo("Successfully initialized project.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to run post-creation commands: {e}", err=True)
