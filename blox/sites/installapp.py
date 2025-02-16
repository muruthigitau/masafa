import json
import os
from typing import List, Optional

import click

from ..utils.config import PROJECT_ROOT
from ..sites.migrate.migrate import run_migration
from ..utils.file_operations import ensure_file_exists

@click.command()
@click.option(
    "--site", type=str, help="The name of the site where the app will be installed."
)
@click.argument("app")
def installapp(site: Optional[str], app: str) -> None:
    """
    Install an app into a selected site and update sites.json.

    :param site: The name of the site where the app will be installed.
    :param app: The name of the app to install.
    """
    # Load sites from sites.json
    sites_json_path: str = os.path.join(PROJECT_ROOT, "sites", "sites.json")
    ensure_file_exists(sites_json_path, initial_data=[])
    if os.path.exists(sites_json_path):
        with open(sites_json_path, "r") as json_file:
            sites: List[dict] = json.load(json_file)
    else:
        click.echo("No sites found in sites.json.")
        return

    # Select or prompt for the site
    if not site:
        click.echo("Select a site to install the app into:")
        for i, site_entry in enumerate(sites, 1):
            click.echo(f"{i}. {site_entry['site_name']}")

        site_choice: int = click.prompt("Enter the number of the site", type=int)

        if site_choice < 1 or site_choice > len(sites):
            click.echo("Invalid site selection.")
            return

        selected_site: dict = sites[site_choice - 1]
    else:
        selected_site = next((s for s in sites if s["site_name"] == site), None)
        if not selected_site:
            click.echo(f"Site '{site}' not found in sites.json.")
            return

    # Load apps from apps.txt
    apps_txt_path: str = os.path.join(PROJECT_ROOT, "config", "apps.txt")
    if os.path.exists(apps_txt_path):
        with open(apps_txt_path, "r") as apps_file:
            apps: List[str] = [
                line.strip()
                for line in apps_file
                if line.strip() and not line.startswith("#")
            ]
    else:
        click.echo("No apps.txt file found.")
        return

    if not apps:
        click.echo("No available apps found in apps.txt.")
        return

    # Prompt for app if not provided
    if not app:
        click.echo(f"Select an app to install into '{selected_site['site_name']}':")
        for i, app_entry in enumerate(apps, 1):
            click.echo(f"{i}. {app_entry}")

        app_choice: int = click.prompt(
            "Enter the number of the app you want to install", type=int
        )

        if app_choice < 1 or app_choice > len(apps):
            click.echo("Invalid app selection.")
            return

        selected_app: str = apps[app_choice - 1]
    else:
        selected_app = app
        if selected_app not in apps:
            click.echo(f"App '{selected_app}' not found in apps.txt.")
            return

    # Check if the app is already installed in the site
    if "installed_apps" not in selected_site:
        selected_site["installed_apps"] = []

    if selected_app in selected_site["installed_apps"]:
        click.echo(
            f"The app '{selected_app}' is already installed in '{selected_site['site_name']}'."
        )
        return

    # Install the app using the external function
    click.echo(f"Installing '{selected_app}' into '{selected_site['site_name']}'...")

    # Update the selected site's installed_apps
    selected_site["installed_apps"].append(selected_app)

    # Replace the updated site in the sites list
    for i, site_entry in enumerate(sites):
        if site_entry["site_name"] == selected_site["site_name"]:
            sites[i] = selected_site
            break

    # Write the updated sites.json
    with open(sites_json_path, "w") as json_file:
        json.dump(sites, json_file, indent=4)

    click.echo(
        f"The app '{selected_app}' has been successfully installed in '{selected_site['site_name']}'."
    )
    run_migration(site=selected_site["site_name"])
