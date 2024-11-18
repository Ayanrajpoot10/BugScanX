import subprocess
import sys
import importlib.metadata
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

def check_for_updates(package_name):
    """Checks if a newer version of the package is available on PyPI."""
    try:
        installed_version = importlib.metadata.version(package_name)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", f"{package_name}==random_version"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        latest_version = None
        for line in result.stdout.splitlines():
            if "from versions:" in line:
                latest_version = line.split("from versions:")[1].strip().split()[0]

        if latest_version and installed_version != latest_version:
            return latest_version
        return None
    except Exception as e:
        print(Fore.RED + f" Error checking for updates: {e}")
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
        print(Fore.LIGHTYELLOW_EX + "\n  1. Check for updates")
        print(Fore.RED + "\n  2. Exit")
        
        choice = input(Fore.CYAN + "\n ➜  Select an option: ").strip()

        if choice == "1":
            package_name = "bugscanx"

            latest_version = check_for_updates(package_name)
            if latest_version:
                print(Fore.YELLOW + f" A new version {latest_version} is available.")
                confirm = input(Fore.CYAN + " ➜  Do you want to update now? (yes/no): ").strip().lower()
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

if __name__ == "__main__":
    update_menu()