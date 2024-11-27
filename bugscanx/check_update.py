import requests
import subprocess
import sys
from colorama import Fore,Style
from bugscanx.import_modules import get_input

# Function to get the latest version of a package from PyPI
def get_latest_version(package_name):
    """Gets the latest version of a package from PyPI."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        latest_version = response.json()["info"]["version"]
        return latest_version
    except Exception as e:
        print(Fore.RED + f" Error getting the latest version: {e}")
        return None

def update_package(package_name):
    """Updates the package to the latest version using pip."""
    try:
        print(Fore.CYAN + f" Updating {package_name} to the latest version...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
        print(Fore.GREEN + f" Successfully updated {package_name} to the latest version.")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f" Failed to update {package_name}. Error: {e}")
    except Exception as e:
        print(Fore.RED + f" An unexpected error occurred: {e}")

def update_menu():
    """Display the main menu and handle user input."""
    while True:
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Please select an option:" + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + "\n  [1] Check for updates")
        print(Fore.RED + "\n  [2] Exit")
        
        choice = get_input(Fore.CYAN + "\n » Select an option: " ,error_message=Fore.RED + "  ⚠  Please enter a valid number between 1 and 2.\n").strip()

        if choice == "1":
            package_name = "bugscanx"

            latest_version = get_latest_version(package_name)
            if latest_version:
                print(Fore.YELLOW + f" A new version {latest_version} is available.")
                confirm = get_input(Fore.CYAN + "  Do you want to update now? (yes/no): ").strip().lower()
                if confirm == "yes":
                    update_package(package_name)
                    break
                else:
                    print(Fore.RED + " Update canceled.")
            else:
                print(Fore.GREEN + " You already have the latest version.")
                break
        
        elif choice == "2":
            print(Fore.GREEN + " Exiting the program.")
            break
        
        else:
            print(Fore.RED + " Invalid option. Please try again.")
