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
            print(f"\033[33m⬇️ Package '{package}' is not installed. Installing...\033[0m")
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


def get_input(prompt, default=None, min_value=None, max_value=None, validator=None, error_message="Invalid input, please try again."):
    """
    Enhanced utility function to get user input with validation support.

    Parameters:
    - prompt (str): The message to display to the user.
    - default (str, optional): Default value if the user does not provide input.
    - validator (function, optional): A function to validate the input. 
      It should return True if valid, otherwise False.
    - error_message (str, optional): Message to display for invalid inputs.

    Returns:
    - str: The validated user input or the default value.
    """
    while True:
        try:
            # Add the default value to the prompt if available
            full_prompt = f"{prompt} [{default}] " if default else f"{prompt} "
            response = input(full_prompt + Style.BRIGHT).strip()
            print(Style.RESET_ALL)  # Reset styles after user input
            
            # Use the default value if no input is provided
            if not response and default is not None:
                return default
            
            # Validate the input if a validator is provided
            if validator:
                if validator(response, min_value, max_value):
                    return response
                else:
                    print(error_message)
            else:
                return response
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")  # Handle Ctrl+C or Ctrl+D gracefully
            exit(0)



import pyfiglet
from colorama import Fore, Style
import shutil

def text_to_ascii_banner(
    text, 
    font="doom", 
    color=Fore.WHITE, 
    align="left", 
    width=None, 
    shift=0,  # New parameter for shifting the banner
    fallback_banner="Invalid input. Check text or font."
):
    """
    Converts text to an ASCII art banner with advanced features including alignment, shifting, and dynamic font listing.

    Args:
        text (str): The text to convert into ASCII art.
        font (str): The font style for the ASCII art (default is "doom").
        color (str): The color for the ASCII art text (default is white).
        align (str): Alignment of the banner: "left", "center", or "right" (default is "center").
        width (int, optional): Custom width for formatting. Defaults to terminal width.
        shift (int, optional): Number of spaces to shift the banner left (negative) or right (positive).
        fallback_banner (str): A fallback message if the banner generation fails.

    Returns:
        str: The colored and formatted ASCII art banner.
    """
    try:
        # Check terminal width
        if width is None:
            width = shutil.get_terminal_size((80, 20)).columns
        
        # Validate alignment
        align_options = {"left", "center", "right"}
        if align not in align_options:
            raise ValueError(f"Invalid alignment option. Choose from {align_options}.")

        # Generate ASCII banner
        ascii_banner = pyfiglet.figlet_format(text, font=font)

        # Split lines and apply alignment and shifting
        aligned_banner = []
        for line in ascii_banner.splitlines():
            # Apply horizontal shift
            shifted_line = (" " * shift) + line  # Shift the line by the specified amount
            
            # Apply alignment
            if align == "left":
                aligned_banner.append(shifted_line.ljust(width))
            elif align == "right":
                aligned_banner.append(shifted_line.rjust(width))
            elif align == "center":
                aligned_banner.append(shifted_line.center(width))

        formatted_banner = "\n".join(aligned_banner)

        # Add color
        colored_banner = f"{color}{formatted_banner}{Style.RESET_ALL}"
        return colored_banner
    except pyfiglet.FontNotFound:
        return f"{Fore.RED}Font not found: {font}. Please choose a valid font.{Style.RESET_ALL}"
    except Exception as e:
        # Catch-all for unexpected errors
        return f"{Fore.RED}{fallback_banner}\nError: {e}{Style.RESET_ALL}"

def list_available_fonts():
    """
    Lists all available fonts in the pyfiglet library.
    
    Returns:
        list: A list of font names.
    """
    return pyfiglet.getFonts()





def validate_input_range(value, min_value, max_value):
    """
    Validator function to check if the input is an integer within a specified range.

    Parameters:
    - value (str): The user input as a string.
    - min_value (int): The minimum valid value (default is 0).
    - max_value (int): The maximum valid value (default is 11).

    Returns:
    - bool: True if the input is a valid integer within the specified range, otherwise False.
    """
    if value.isdigit():
        num = int(value)
        return min_value <= num <= max_value
    return False




def banner():
    """
    Displays the banner for the toolkit with ASCII art and basic information about the project.
    """
    clear_screen()
    # Display the ASCII banner with the tool name
    print(text_to_ascii_banner("BugScanX ", align="left",shift=1, font="doom", color=Style.BRIGHT + Fore.MAGENTA))
    print(Fore.LIGHTMAGENTA_EX + " 🏷️  Version: " + Fore.WHITE + Style.BRIGHT + "1.0.5")
    print(Fore.MAGENTA + "  ©️ Owner: " + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Ayan Rajpoot ™")
    print(Fore.BLUE + " 🔗 Support: " + Style.BRIGHT + Fore.LIGHTBLUE_EX + "https://t.me/BugScanX")
    print(Fore.WHITE + Style.DIM +"\n This is a test version. Report bugs on Telegram for quick fixes")
    print(Style.RESET_ALL)



def main_menu():
    """
    Main menu loop for the BugScanX toolkit, allowing users to select different scanning and OSINT options.
    Each option has a unique text-based icon for better representation and alignment.
    """
    while True:
        banner()
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Please select an option:"+ Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n [1] ⚡  Host Scanner(pro mode)")
        print(Fore.LIGHTYELLOW_EX + " [2] 🌐  Subdomains Scanner ")
        print(Fore.LIGHTYELLOW_EX + " [3] 📡  CIDR Scanner")
        print(Fore.LIGHTYELLOW_EX + " [4] 🔍  Subdomains Finder")
        print(Fore.LIGHTYELLOW_EX + " [5] 🔎  IP to domains")
        print(Fore.LIGHTYELLOW_EX + " [6] ✂️   TXT Toolkit")
        print(Fore.LIGHTYELLOW_EX + " [7] 🔓  Open Port Checker")
        print(Fore.LIGHTYELLOW_EX + " [8] 📜  DNS Records")
        print(Fore.LIGHTYELLOW_EX + " [9] 💡  OSINT ")
        print(Fore.LIGHTYELLOW_EX + " [10]❓  Help")
        print(Fore.LIGHTRED_EX + Style.BRIGHT + " [11]⛔  Exit" + Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + " [0] 🔄️  Update\n" + Style.RESET_ALL)

        # Get the user's choice
        choice = get_input(Fore.CYAN + " »  Enter your choice (0-11): ",validator=validate_input_range, min_value=0, max_value=11,error_message=Fore.RED + "  ⚠  Please enter a valid number between 0 and 11.\n").strip()




        if choice == '1':
            clear_screen()
            print(text_to_ascii_banner("HOST Scanner", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import host_scanner as host_scanner
                host_scanner.bugscanner_main()
            except ImportError:
                import host_scanner
                host_scanner.bugscanner_main()
            
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

        elif choice == "2":
            clear_screen()
            print(text_to_ascii_banner("Sub Scanner", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import sub_scan as sub_scan
            except ImportError:
                import sub_scan
            hosts, ports, output_file, threads, method = sub_scan.get1_scan_inputs()
            if hosts is None:
                continue
            sub_scan.perform1_scan(hosts, ports, output_file, threads, method)
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

        elif choice == "3":
            clear_screen()
            print(text_to_ascii_banner("CIDR Scanner  ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import ip_scan as ip_scan
            except ImportError:
                import ip_scan
            hosts, ports, output_file, threads, method = ip_scan.get2_scan_inputs()

            if hosts is None:
                continue

            ip_scan.perform2_scan(hosts, ports, output_file, threads, method)
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

        elif choice == "4":
            clear_screen()
            print(text_to_ascii_banner("Subfinder ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import sub_finder as sub_finder
            except ImportError:
                import sub_finder
            sub_finder.find_subdomains()
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

        elif choice == "5":
            clear_screen()
            print(text_to_ascii_banner("IP LookUP ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import ip_lookup as ip_lookup
            except ImportError:
                import ip_lookup
            ip_lookup.Ip_lockup_menu()
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")


        elif choice =="6":
            clear_screen()
            print(text_to_ascii_banner("TxT Toolkit ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import txt_toolkit as txt_toolkit
            except ImportError:
                import txt_toolkit
            txt_toolkit.txt_toolkit_main_menu()
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

        elif choice == "7":
            clear_screen()
            print(text_to_ascii_banner("Open Port ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import open_port as open_port
            except ImportError:
                import open_port
            open_port.open_port_checker()
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

        elif choice == "8":
            clear_screen()
            print(text_to_ascii_banner("DNS Records ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import dns_info as dns_info
            except ImportError:
                import dns_info
            domain = get_input(Fore.CYAN + " »  Enter a domain to perform NSLOOKUP: ").strip()
            dns_info.nslookup(domain)
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

        elif choice == "9":
            clear_screen()
            print(text_to_ascii_banner("OSINT ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import osint as osint
            except ImportError:
                import osint
            osint.osint_main()
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

        elif choice == "10":
            clear_screen()
            print(text_to_ascii_banner("Help Menu", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            try:
                from bugscanx import script_help as script_help
            except ImportError:
                import script_help
            script_help.show_help()
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

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
            input(Fore.YELLOW + "\n🏠︎ Press Enter to return to the main menu...")

        else:
            print(Fore.RED + Style.BRIGHT + "\n⚠️ Invalid choice. Please select a valid option.")
            input(Fore.YELLOW + Style.BRIGHT + "\n Press Enter to return to the main menu...")
            main_menu() 



# Run the menu
if __name__ == "__main__":
    main_menu()
