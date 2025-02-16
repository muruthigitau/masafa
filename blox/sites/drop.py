import json
import os
import platform
import subprocess
from typing import List, Dict, Any

import click

from ..utils.config import PROJECT_ROOT
from ..sites.migrate.migrate import run_migration
from ..utils.file_operations import ensure_file_exists

@click.command()
@click.option("--site", type=str, help="The name of the site to delete.")
def dropsite(site: str) -> None:
    """
    Delete a site and remove its entry from sites.json.

    Args:
        site (str): The name of the site to delete.
    """
    # Load sites from sites.json
    sites_json_path: str = os.path.join(PROJECT_ROOT, "sites", "sites.json")
    ensure_file_exists(sites_json_path, initial_data=[])
    if os.path.exists(sites_json_path):
        with open(sites_json_path, "r") as json_file:
            sites: List[Dict[str, Any]] = json.load(json_file)
    else:
        click.echo("No sites found in sites.json.")
        return

    # Prompt for site if not provided
    if not site:
        click.echo("Select a site to delete:")
        for i, site_entry in enumerate(sites, 1):
            click.echo(f"{i}. {site_entry['site_name']}")

        site_choice: int = click.prompt("Enter the number of the site to delete", type=int)

        if site_choice < 1 or site_choice > len(sites):
            click.echo("Invalid site selection.")
            return

        selected_site: Dict[str, Any] = sites[site_choice - 1]
    else:
        selected_site = next((s for s in sites if s["site_name"] == site), None)
        if not selected_site:
            click.echo(f"Site '{site}' not found in sites.json.")
            return

    # Confirm the deletion
    confirm: bool = click.confirm(
        f"Are you sure you want to delete the site '{selected_site['site_name']}'?",
        default=False,
    )
    if not confirm:
        click.echo("Site deletion canceled.")
        return

    # Delete the site folder with admin/superuser privileges
    site_folder_path: str = os.path.join(PROJECT_ROOT, "sites", selected_site["site_name"])

    try:
        if os.path.exists(site_folder_path):
            click.echo(
                f"Attempting to delete the site folder '{site_folder_path}' with admin privileges..."
            )

            if platform.system() == "Windows":
                # Use PowerShell on Windows
                powershell_command: str = f'Remove-Item -Recurse -Force "{site_folder_path}"'
                subprocess.check_call(
                    ["powershell", "-Command", powershell_command], shell=True
                )
            else:
                # Use sudo rm -rf on Unix-based systems
                subprocess.check_call(["sudo", "rm", "-rf", site_folder_path])

            click.echo(f"Deleted the site folder '{site_folder_path}'.")
        else:
            click.echo(f"Site folder '{site_folder_path}' does not exist.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error deleting site folder: {e}")
        return

    # Remove the site entry from sites.json
    sites = [s for s in sites if s["site_name"] != selected_site["site_name"]]

    with open(sites_json_path, "w") as json_file:
        json.dump(sites, json_file, indent=4)

    click.echo(
        f"Site '{selected_site['site_name']}' has been successfully removed from sites.json."
    )
    
    run_migration()
