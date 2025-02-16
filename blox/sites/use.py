import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any

import click

from ..utils.config import PROJECT_ROOT
from ..utils.file_operations import ensure_file_exists

# Define the path to sites.json
SITES_JSON_PATH = os.path.join(PROJECT_ROOT, "sites", "sites.json")


def load_sites() -> Optional[List[Dict[str, Any]]]:
    """
    Reads the sites.json file and returns the list of sites.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of dictionaries representing the sites, or None if no sites are found.
    """
    ensure_file_exists(SITES_JSON_PATH, initial_data=[])
    if os.path.exists(SITES_JSON_PATH):
        with open(SITES_JSON_PATH, "r") as json_file:
            sites = json.load(json_file)
            return sites
    else:
        click.echo("No sites found in sites.json.")
        return None


def set_default_site(site_name: str) -> None:
    """q
    Sets the specified site as the default site in the sites.json file.

    Args:
        site_name (str): The name of the site to set as default.
    """
    sites = load_sites()

    if not sites:
        return  # Exit early if no sites were loaded

    # Find the site by site_name
    site = next((s for s in sites if s["site_name"] == site_name), None)

    if not site:
        click.echo(f"Error: Site '{site_name}' not found.")
        return  # Exit early if the site is not found

    # Set the default status: true for the specified site, false for others
    for s in sites:
        s["default"] = s["site_name"] == site_name

    # Write the updated sites list back to sites.json
    with open(SITES_JSON_PATH, "w") as json_file:
        json.dump(sites, json_file, indent=4)

    # Print confirmation and site details
    click.echo(
        f"Default site set to '{site_name}' at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    click.echo(f"Site name: {site['site_name']}")
    click.echo(f"Django port: {site['django_port']}")
    click.echo(f"Next.js port: {site['nextjs_port']}")
    click.echo(f"Developer mode: {'Enabled' if site['developer_mode'] else 'Disabled'}")
    click.echo(f"Installed apps: {', '.join(site['installed_apps'])}")


@click.command()
@click.argument("sitename")
def usesite(sitename: str) -> None:
    """
    Sets the provided site as the default site.

    Args:
        sitename (str): The name of the site to set as default.
    """
    set_default_site(sitename)
