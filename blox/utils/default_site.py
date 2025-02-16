import json
import os
from typing import Optional, Tuple, Dict, Any

import click


def get_default_site_info(PROJECT_ROOT: str) -> Optional[Dict[str, Any]]:
    """
    Utility function to get the Django path and site name of the default site.

    :param PROJECT_ROOT: The root directory of the project
    :return: A dictionary with site information if a default site is found, otherwise None
    """
    sites_json_path = os.path.join(PROJECT_ROOT, "sites", "sites.json")

    if not os.path.exists(sites_json_path):
        click.echo("No sites found in sites.json.")
        return None

    # Load sites from sites.json
    with open(sites_json_path, "r") as json_file:
        sites = json.load(json_file)

    # Find the default site
    selected_site = next((s for s in sites if s.get("default") == True), None)

    if selected_site:
        return selected_site
    else:
        return None
