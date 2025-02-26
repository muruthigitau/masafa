import json
import os
from typing import Optional, Tuple

import click

from .default_site import get_default_site_info
from ..utils.file_operations import ensure_file_exists

def find_project_root(current_path: str) -> str:
    while current_path != "/":
        if "blox.config" in os.listdir(current_path):
            return current_path
        current_path = os.path.dirname(current_path)
    raise FileNotFoundError("Project root with 'blox.config' not found.")

def find_django_path(site: str) -> str:
    return os.path.join(PROJECT_ROOT, f"backend")

def write_running_ports(django_port: int, nextjs_port: int) -> None:
    next_path = os.path.join(PROJECT_ROOT)
    env_file_path = os.path.join(next_path, ".env.local")

    # Update the .env.local file
    if not os.path.exists(env_file_path):
        with open(env_file_path, "w") as f:
            f.write(f"NEXT_PUBLIC_DJANGO_PORT={django_port}\n")
            f.write(f"NEXT_PUBLIC_NEXTJS_PORT={nextjs_port}\n")
    else:
        with open(env_file_path, "r") as f:
            lines = f.readlines()

        with open(env_file_path, "w") as f:
            updated = False
            for line in lines:
                if line.startswith("NEXT_PUBLIC_DJANGO_PORT="):
                    f.write(f"NEXT_PUBLIC_DJANGO_PORT={django_port}\n")
                    updated = True
                elif line.startswith("NEXT_PUBLIC_NEXTJS_PORT="):
                    f.write(f"NEXT_PUBLIC_NEXTJS_PORT={nextjs_port}\n")
                    updated = True
                else:
                    f.write(line)

            if not updated:
                f.write(f"NEXT_PUBLIC_DJANGO_PORT={django_port}\n")
                f.write(f"NEXT_PUBLIC_NEXTJS_PORT={nextjs_port}\n")

def find_module_base_path(app_name: str, module_name: Optional[str] = None, app_path: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """Locate the modules.txt file and determine the base path for modules, searching specified directories.

    Args:
        app_name (str): Name of the app to search within.
        module_name (str, optional): Specific module name to look for within the app. Defaults to None.
        app_path (str, optional): Path to the app directory. If not provided, defaults to APPS_PATH/app_name.

    Returns:
        tuple: Path to modules.txt and the base directory for modules, or (None, None) if not found.
    """
    # Determine the base path for the app, defaults to APPS_PATH/app_name
    base_path = os.path.join(APPS_PATH, app_name, app_name)

    # First, check for modules.txt directly in the base_path
    modules_file_path = os.path.join(base_path, "modules.txt")
    if module_name:
        modules_path = os.path.join(base_path, module_name)
        if os.path.isfile(modules_file_path):
            return modules_file_path, modules_path
    else:
        if os.path.isfile(modules_file_path):
            return modules_file_path, base_path    

    return None, None

PROJECT_ROOT = find_project_root(os.getcwd())
APPS_TXT_PATH = os.path.join(PROJECT_ROOT, "config", "apps.txt")
SITES_JSON_PATH = os.path.join(PROJECT_ROOT, "sites", "sites.json")
DOCS_JSON_PATH = os.path.join(PROJECT_ROOT, "sites", "doctypes.json")
PRINT_JSON_PATH = os.path.join(PROJECT_ROOT, "sites", "print_formats.json")
APPS_PATH = os.path.join(PROJECT_ROOT, "apps")
DJANGO_PATH =  os.path.join(PROJECT_ROOT, "backend")
DEFAULT_SITE = get_default_site_info(PROJECT_ROOT)
SITES_PATH = os.path.join(PROJECT_ROOT, "sites")
