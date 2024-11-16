import os
import subprocess
import sys
import threading

# Lock for managing file writes safely in a multi-threaded environment
file_write_lock = threading.Lock()

def install_requirements():
    """
    Function to install the required Python packages.
    It checks if the necessary packages are installed and installs them if they are not found.
    """
    required_packages = {
        'requests': 'requests',
        'colorama': 'colorama',
        'ipaddress': 'ipaddress',
        'pyfiglet': 'pyfiglet',
        'socket': 'socket',
        'ssl': 'ssl',
        'beautifulsoup4': 'bs4',
        'dnspython': 'dns'
    }

    # Iterating through each required package and checking for installation
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)  # Check if the package is already installed
        except ImportError:
            # Install the missing package if not found
            print(f"\033[33m⏳ Package '{package}' is not installed. Installing...\033[0m")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"\033[32m✅ Package '{package}' installed successfully.\033[0m")

# Run the install_requirements function to ensure necessary packages are installed
install_requirements()

from colorama import Fore, Style, Back, init
import pyfiglet

# Initialize colorama to automatically reset styles after each print
init(autoreset=True)

def clear_screen():
    """
    Function to clear the terminal screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def text_to_ascii_banner(text, font="doom", color=Fore.WHITE):
    """
    Converts text to an ASCII art banner using the pyfiglet library and applies color formatting.
    Args:
        text (str): The text to convert into ASCII art.
        font (str): The font style for the ASCII art (default is "doom").
        color (str): The color for the ASCII art text (default is white).
    Returns:
        str: The colored ASCII art banner.
    """
    try:
        ascii_banner = pyfiglet.figlet_format(text, font=font)
        colored_banner = f"{color}{ascii_banner}{Style.RESET_ALL}"
        return colored_banner
    except pyfiglet.FontNotFound:
        return "Font not found. Please choose a valid font."

def get_input(prompt, default=None):
    """
    Utility function to get user input with a prompt.
    Returns default if user does not provide input.
    """
    response = input(prompt + Style.BRIGHT).strip()
    print(Style.RESET_ALL)
    return response if response else default or ""

def banner():
    """
    Displays the banner for the toolkit with ASCII art and basic information about the project.
    """
    clear_screen()
    # Display the ASCII banner with the tool name
    print(text_to_ascii_banner("BugScanX ", font="doom", color=Style.BRIGHT + Fore.MAGENTA))
    print(Fore.MAGENTA + "  ©️ Owner: " + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Ayan Rajpoot")
    print(Fore.BLUE + " 🔗 Support: " + Style.BRIGHT + Fore.LIGHTBLUE_EX + "https://t.me/BugScanX")
    print(Fore.LIGHTGREEN_EX +"\nThis is a test version. Report bugs on Telegram for quick fixes")
    print(Style.RESET_ALL)

def main_menu():
    """
    Main menu loop for the BugScanX toolkit, allowing users to select different scanning and OSINT options.
    Each option will run a specific scan or tool from the 'modules' directory.
    """
    while True:
        banner()
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Please select an option:"+ Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + " [1] ⚡  Host Scanner(only for pro)")
        print(Fore.YELLOW + " [2] 🖥️   Subdomains Scanner ")
        print(Fore.YELLOW + " [3] 📡  IP Addresses Scanner")
        print(Fore.YELLOW + " [4] 🌐  Subdomains Finder")
        print(Fore.YELLOW + " [5] 🔍  domains hosted on same ip")
        print(Fore.YELLOW + " [6] ✂️   TXT Toolkit")
        print(Fore.YELLOW + " [7] 🔓  Open Port Checker")
        print(Fore.YELLOW + " [8] 📜  DNS Records")
        print(Fore.YELLOW + " [9] 📖  Help")
        print(Fore.RED + " [10]⛔  Exit\n")

        # Get the user's choice
        choice = get_input(Fore.CYAN + " ➜  Enter your choice (1-10): ").strip()


        if choice == '1':
            clear_screen()
            print(text_to_ascii_banner("HOST Scanner", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            import modules.host_scanner as host_scanner
            host_scanner.advance_main()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")
        # Menu option handling
        if choice == "2":
            clear_screen()
            print(text_to_ascii_banner("HOST Scanner", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            import modules.sub_scan as sub_scan
            hosts, ports, output_file, threads, method = sub_scan.get1_scan_inputs()
            if hosts is None:
                continue
            sub_scan.perform1_scan(hosts, ports, output_file, threads, method)
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "3":
            clear_screen()
            print(text_to_ascii_banner("IP Scanner  ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            import modules.ip_scan as ip_scan
            hosts, ports, output_file, threads, http_method = ip_scan.get_scan_inputs()

            if not all([hosts, ports, output_file, threads, http_method]):
                print(Fore.YELLOW + "Returning to main menu...")
                continue

            ip_scan.perform_scan(hosts, ports, output_file, threads, http_method)
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "4":
            clear_screen()
            print(text_to_ascii_banner("Subfinder ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            import modules.sub_finder as sub_finder
            sub_finder.find_subdomains()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "5":
            clear_screen()
            print(text_to_ascii_banner("IP LookUP ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            import modules.ip_lookup as ip_lookup
            ip_lookup.Ip_lockup_menu()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "osint":
            clear_screen()
            print(text_to_ascii_banner("OSINT ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            import modules.osint as osint
            osint.osint_main()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice =="6":
            clear_screen()
            print(text_to_ascii_banner("TxT Toolkit ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            import modules.txt_toolkit as txt_toolkit
            txt_toolkit.txt_toolkit_main_menu()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "7":
            clear_screen()
            print(text_to_ascii_banner("Open Port ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            import modules.open_port as open_port
            open_port.open_port_checker()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "8":
            clear_screen()
            print(text_to_ascii_banner("DNS Records ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            domain = get_input(Fore.CYAN + " ➜  Enter a domain to perform NSLOOKUP: ").strip()
            import modules.dns_info as dns_info
            dns_info.nslookup(domain)
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "9":
            clear_screen()
            import modules.script_help as script_help
            script_help.show_help()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "10":
            print(Fore.RED + Style.BRIGHT + "\n🔴 Shutting down the toolkit. See you next time!")
            sys.exit()

        else:
            print(Fore.RED + Style.BRIGHT + "\n⚠️ Invalid choice. Please select a valid option.")
            input(Fore.YELLOW + Style.BRIGHT + "\n Press Enter to return to the main menu...")
            main_menu()  # Reload the menu for a new choice

# Run the menu
if __name__ == "__main__":
    main_menu()
