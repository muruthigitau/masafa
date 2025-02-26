import json
import os
from typing import List, Dict, Any, Optional

import click

from ..utils.config import PROJECT_ROOT
from .utils.uninstalldjangoapp import uninstall_django_app
from ..sites.migrate.migrate import run_migration
from ..utils.file_operations import ensure_file_exists

@click.command()
@click.option(
    "--site", type=str, help="The name of the site where the app will be uninstalled."
)
@click.argument("app")
def uninstallapp(site: Optional[str], app: str) -> None:
    """
    Uninstall an app from a selected site and update sites.json.

    :param site: The name of the site where the app will be uninstalled.
    :param app: The name of the app to uninstall.
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
        click.echo("Select a site to uninstall the app:")
        for i, site_entry in enumerate(sites, 1):
            click.echo(f"{i}. {site_entry['site_name']}")

        site_choice: int = click.prompt("Enter the number of the site", type=int)

        if site_choice < 1 or site_choice > len(sites):
            click.echo("Invalid site selection.")
            return

        selected_site: Dict[str, Any] = sites[site_choice - 1]
    else:
        selected_site = next((s for s in sites if s["site_name"] == site), None)
        if not selected_site:
            click.echo(f"Site '{site}' not found in sites.json.")
            return

    # Ensure the site has installed apps
    if "installed_apps" not in selected_site or not selected_site["installed_apps"]:
        click.echo(f"No apps installed in '{selected_site['site_name']}'.")
        return

    # Prompt for app if not provided
    if not app:
        click.echo(f"Select an app to uninstall from '{selected_site['site_name']}':")
        for i, app_entry in enumerate(selected_site["installed_apps"], 1):
            click.echo(f"{i}. {app_entry}")

        app_choice: int = click.prompt(
            "Enter the number of the app you want to uninstall", type=int
        )

        if app_choice < 1 or app_choice > len(selected_site["installed_apps"]):
            click.echo("Invalid app selection.")
            return

        selected_app: str = selected_site["installed_apps"][app_choice - 1]
    else:
        selected_app = app
        if selected_app not in selected_site["installed_apps"]:
            click.echo(
                f"App '{selected_app}' is not installed in '{selected_site['site_name']}'."
            )
            return

    # Simulate uninstalling the app (e.g., removing files, undoing migrations, etc.)
    click.echo(f"Uninstalling '{selected_app}' from '{selected_site['site_name']}'...")

    # Remove the app from the installed_apps list
    selected_site["installed_apps"].remove(selected_app)

    with open(sites_json_path, "w") as json_file:
        json.dump(sites, json_file, indent=4)

    click.echo(
        f"The app '{selected_app}' has been successfully uninstalled from '{selected_site['site_name']}'."
    )
    run_migration()


if __name__ == "__main__":
    uninstallapp()
