import os
import sys
import requests
import subprocess
from threading import Thread

def get_latest_version(package_name):
    """Gets the latest version of a package from PyPI."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
        response.raise_for_status()
        return response.json()["info"]["version"]
    except:
        return None

def update_package(package_name):
    """Updates the package to the latest version using pip."""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", package_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        pass

def restart_tool():
    """Restarts the current script."""
    os.execl(sys.executable, sys.executable, *sys.argv)

def check_and_update(package_name):
    """Checks for updates and updates the package if a new version is available."""
    latest_version = get_latest_version(package_name)
    if not latest_version:
        return  # Skip if unable to fetch the latest version

    try:
        # Get the current installed version
        current_version = subprocess.check_output(
            [sys.executable, "-m", "pip", "show", package_name],
            text=True
        ).splitlines()
        installed_version = [
            line.split(": ")[1] for line in current_version if line.startswith("Version:")
        ][0]

        # Compare versions and update if needed
        if installed_version != latest_version:
            update_package(package_name)
            restart_tool()
    except:
        pass

def start_background_update(package_name):
    """Starts the update check in a background thread."""
    Thread(target=check_and_update, args=(package_name,), daemon=True).start()
