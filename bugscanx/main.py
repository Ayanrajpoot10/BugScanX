import os
import subprocess
import sys



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
        'ssl': 'ssl',
        'beautifulsoup4': 'bs4',
        'dnspython': 'dns',
        'multithreading': 'multithreading',
        'loguru': 'loguru'
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
    print(Fore.WHITE + Style.DIM +"\nThis is a test version. Report bugs on Telegram for quick fixes")
    print(Style.RESET_ALL)



def main_menu():
    """
    Main menu loop for the BugScanX toolkit, allowing users to select different scanning and OSINT options.
    Each option will run a specific scan or tool from the 'modules' directory.
    """
    while True:
        banner()
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Please select an option:"+ Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n [1] ⚡  Host Scanner(only for pro)")
        print(Fore.LIGHTYELLOW_EX + " [2] 🖥️   Subdomains Scanner ")
        print(Fore.LIGHTYELLOW_EX + " [3] 📡  IP Addresses Scanner")
        print(Fore.LIGHTYELLOW_EX + " [4] 🌐  Subdomains Finder")
        print(Fore.LIGHTYELLOW_EX + " [5] 🔍  domains hosted on same ip")
        print(Fore.LIGHTYELLOW_EX + " [6] ✂️   TXT Toolkit")
        print(Fore.LIGHTYELLOW_EX + " [7] 🔓  Open Port Checker")
        print(Fore.LIGHTYELLOW_EX + " [8] 📜  DNS Records")
        print(Fore.LIGHTYELLOW_EX + " [9] 💡  OSINT ")
        print(Fore.LIGHTYELLOW_EX + " [10] 📖  Help")
        print(Fore.LIGHTRED_EX + Style.BRIGHT + " [11]⛔  Exit" + Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + " [0] 🔄️  Update\n" + Style.RESET_ALL)

        # Get the user's choice
        choice = get_input(Fore.CYAN + " ➜  Enter your choice (0-11): ").strip()


        if choice == '1':
            clear_screen()
            print(text_to_ascii_banner("HOST Scanner", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import host_scanner as host_scanner
                host_scanner.bugscanner_main()
            except ImportError:
                import host_scanner
                host_scanner.bugscanner_main()
            
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "2":
            clear_screen()
            print(text_to_ascii_banner("HOST Scanner", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import sub_scan as sub_scan
            except ImportError:
                import sub_scan
            hosts, ports, output_file, threads, method = sub_scan.get1_scan_inputs()
            if hosts is None:
                continue
            sub_scan.perform1_scan(hosts, ports, output_file, threads, method)
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "3":
            clear_screen()
            print(text_to_ascii_banner("IP Scanner  ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import ip_scan as ip_scan
            except ImportError:
                import ip_scan
            hosts, ports, output_file, threads, method = ip_scan.get2_scan_inputs()

            if hosts is None:
                continue

            ip_scan.perform2_scan(hosts, ports, output_file, threads, method)
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "4":
            clear_screen()
            print(text_to_ascii_banner("Subfinder ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import sub_finder as sub_finder
            except ImportError:
                import sub_finder
            sub_finder.find_subdomains()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "5":
            clear_screen()
            print(text_to_ascii_banner("IP LookUP ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import ip_lookup as ip_lookup
            except ImportError:
                import ip_lookup
            ip_lookup.Ip_lockup_menu()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")


        elif choice =="6":
            clear_screen()
            print(text_to_ascii_banner("TxT Toolkit ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import txt_toolkit as txt_toolkit
            except ImportError:
                import txt_toolkit
            txt_toolkit.txt_toolkit_main_menu()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "7":
            clear_screen()
            print(text_to_ascii_banner("Open Port ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import open_port as open_port
            except ImportError:
                import open_port
            open_port.open_port_checker()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "8":
            clear_screen()
            print(text_to_ascii_banner("DNS Records ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import dns_info as dns_info
            except ImportError:
                import dns_info
            domain = get_input(Fore.CYAN + " ➜  Enter a domain to perform NSLOOKUP: ").strip()
            dns_info.nslookup(domain)
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "9":
            clear_screen()
            print(text_to_ascii_banner("OSINT ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import osint as osint
            except ImportError:
                import osint
            osint.osint_main()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "10":
            clear_screen()
            print(text_to_ascii_banner("Help ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import script_help as script_help
            except ImportError:
                import script_help
            script_help.show_help()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "11":
            print(Fore.RED + Style.BRIGHT + "\n🔴 Shutting down the toolkit. See you next time!")
            sys.exit()

        elif choice == "0":
            clear_screen()
            print(text_to_ascii_banner("Update Menu", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import check_update as check_update
            except ImportError:
                import check_update
            check_update.update_menu()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        else:
            print(Fore.RED + Style.BRIGHT + "\n⚠️ Invalid choice. Please select a valid option.")
            input(Fore.YELLOW + Style.BRIGHT + "\n Press Enter to return to the main menu...")
            main_menu() 



# Run the menu
if __name__ == "__main__":
    main_menu()
