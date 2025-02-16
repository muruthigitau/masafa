import json
import os
from typing import List, Dict, Any

from ...utils.config import DOCS_JSON_PATH, PROJECT_ROOT
from ...utils.file_operations import ensure_file_exists

def load_existing_data() -> List[Dict[str, Any]]:
    """
    Loads existing data from the JSON file or returns an empty list.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the data from the JSON file.
    """
    ensure_file_exists(DOCS_JSON_PATH, initial_data=[])
    if os.path.exists(DOCS_JSON_PATH):
        try:
            with open(DOCS_JSON_PATH, "r") as json_file:
                content = json_file.read().strip()
                if not content:  # Handle empty file
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            return []
    return []

def get_all_sites() -> List[Dict[str, Any]]:
    """
    Retrieves all sites from the sites JSON file.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the site data.
    """
    sites_json_path = os.path.join(PROJECT_ROOT, "sites", "sites.json")
    ensure_file_exists(sites_json_path, initial_data=[])

    with open(sites_json_path, "r") as json_file:
        sites = json.load(json_file)

    return sites
