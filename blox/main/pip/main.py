import json
import os
import subprocess
import sys
from typing import List, Optional

import click

from ...utils.config import APPS_PATH, PROJECT_ROOT
from ...utils.file_operations import ensure_file_exists

def install_libraries(libraries: List[str], app_name: Optional[str] = None, sites: Optional[List[str]] = None) -> None:
    """
    Install the specified libraries in the virtual environment and update the requirements file for the specified app.

    Args:
        libraries (List[str]): List of libraries to install.
        app_name (Optional[str]): Name of the app to update its requirements.txt file.
        sites (Optional[List[str]]): List of sites to install the libraries.
    """
    venv_path = os.path.join(PROJECT_ROOT, "env")
    if not os.path.exists(venv_path):
        click.echo("Virtual environment not found. Please run 'blox setup' first.")
        return

    python_executable = os.path.join(venv_path, "bin", "python")
    if sys.platform.startswith("win"):
        python_executable = os.path.join(venv_path, "Scripts", "python.exe")

    if app_name:
        requirements_file = os.path.join(APPS_PATH, f"{app_name}/requirements.txt")

        # Add libraries to requirements file
        with open(requirements_file, "a") as f:
            for library in libraries:
                f.write(f"{library}\n")
        click.echo(f"Added libraries to {requirements_file}")

    # Install libraries on the specified sites
    for site in sites:
        django_path = os.path.join(PROJECT_ROOT, "sites", site, "django")
        if os.path.exists(django_path):
            try:
                for library in libraries:
                    subprocess.check_call(
                        [python_executable, "-m", "pip", "install", library]
                    )
                click.echo(f"Installed libraries for site '{site}' successfully.")
            except subprocess.CalledProcessError as e:
                click.echo(f"Error installing libraries for site '{site}': {e}")

@click.group()
def pip() -> None:
    """
    Manage Python packages for the project.
    """

@click.command()
@click.argument("libraries", nargs=-1)
@click.option(
    "--app", type=str, help="Specify a custom app to update its requirements.txt"
)
@click.option(
    "--site",
    type=str,
    help="Specify a site to install the libraries. If not provided, a selection prompt will appear.",
)
def install(libraries: List[str], app: Optional[str], site: Optional[str]) -> None:
    """
    Install the specified Python libraries in the project.
    Usage: blox pip install <library_name> [<library_name>...] [--app <app_name>] [--site <site_name>]

    Args:
        libraries (List[str]): List of libraries to install.
        app (Optional[str]): Name of the app to update its requirements.txt file.
        site (Optional[str]): Name of the site to install the libraries.
    """
    run_pip_install(libraries, app, site)

@click.command()
@click.argument("libraries", nargs=-1)
@click.option(
    "--app", type=str, help="Specify a custom app to update its requirements.txt"
)
@click.option(
    "--site",
    type=str,
    help="Specify a site to install the libraries. If not provided, a selection prompt will appear.",
)
def i(libraries: List[str], app: Optional[str], site: Optional[str]) -> None:
    """
    Install the specified Python libraries in the project using the alias 'i'.
    Usage: blox pip i <library_name> [<library_name>...] [--app <app_name>] [--site <site_name>]

    Args:
        libraries (List[str]): List of libraries to install.
        app (Optional[str]): Name of the app to update its requirements.txt file.
        site (Optional[str]): Name of the site to install the libraries.
    """
    run_pip_install(libraries, app, site)

def run_pip_install(libraries: List[str], app: Optional[str], site: Optional[str]) -> None:
    """
    Run the pip install command for the specified libraries.

    Args:
        libraries (List[str]): List of libraries to install.
        app (Optional[str]): Name of the app to update its requirements.txt file.
        site (Optional[str]): Name of the site to install the libraries.
    """
    # Load sites from sites.json
    sites_json_path = os.path.join(PROJECT_ROOT, "sites", "sites.json")
    ensure_file_exists(sites_json_path, initial_data=[])
    if os.path.exists(sites_json_path):
        with open(sites_json_path, "r") as json_file:
            sites = json.load(json_file)
    else:
        click.echo("No sites found in sites.json.")
        return

    if not site:
        selected_sites = [site["site_name"] for site in sites]
    else:
        selected_sites = [site]

    # Check for apps in selected sites
    app_names = set()
    for selected_site in selected_sites:
        site_info = next((s for s in sites if s["site_name"] == selected_site), None)
        if site_info and "installed_apps" in site_info:
            app_names.update(site_info["installed_apps"])

    if app and app not in app_names:
        click.echo(f"App '{app}' not found in the selected sites.")
        return

    try:
        install_libraries(libraries, app, selected_sites)
        click.echo("Libraries installed successfully.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error installing libraries: {e}")

pip.add_command(install)
pip.add_command(i)
