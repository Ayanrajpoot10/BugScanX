import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import threading
import requests
from colorama import Fore, Style, Back, init
import ipaddress
init(autoreset=True)
file_write_lock = threading.Lock()
from sub_scan import clear_screen, file_manager, get_input


DEFAULT_TIMEOUT1 = 5  # Default timeout for HTTP requests
EXCLUDE_LOCATIONS = ["https://jio.com/BalanceExhaust", "http://filter.ncell.com.np/nc"]  # List of URLs to exclude from the scan



def get_cidrs_from_file(file_path):
    """Reads CIDR blocks from a file and returns a list of IPs."""
    invalid_attempts = 0  # Counter for invalid attempts
    while True:
        try:
            with open(file_path, 'r') as file:
                cidr_list = [line.strip() for line in file if line.strip()]
                ip_list = []
                for cidr in cidr_list:
                    try:
                        network = ipaddress.ip_network(cidr, strict=False)
                        ip_list.extend([str(ip) for ip in network.hosts()])
                    except ValueError as e:
                        print(Fore.RED + f"⚠️ Invalid CIDR '{cidr}': {e}")
                return ip_list
        except Exception as e:
            print(Fore.RED + f"⚠️ Error reading file: {e}")
            invalid_attempts += 1

        if invalid_attempts >= 3:
            print(Fore.RED + "\n⚠️ Too many invalid attempts. Returning to main menu.")
            time.sleep(1)  # Delay before returning to main menu
            return []


def get_cidrs_from_input():
    """Prompts the user to manually input CIDR blocks or IPs and returns a list of IPs."""
    invalid_attempts = 0
    while True:
        cidr_input = get_input(Fore.CYAN + "➜  Enter CIDR blocks or individual IPs (comma-separated): ").strip()
        if not cidr_input:
            print(Fore.RED + "⚠️ No input provided. Please enter valid CIDRs or IPs.")
            invalid_attempts += 1
        else:
            cidr_list = [cidr.strip() for cidr in cidr_input.split(',')]
            ip_list = []
            for cidr in cidr_list:
                try:
                    network = ipaddress.ip_network(cidr, strict=False)
                    ip_list.extend([str(ip) for ip in network.hosts()])
                except ValueError:
                    print(Fore.RED + f"⚠️ Invalid CIDR '{cidr}'. Skipping...")
            return ip_list

        if invalid_attempts >= 3:
            print(Fore.RED + "\n⚠️ Too many invalid attempts. Returning to main menu.")
            time.sleep(1)
            return []


def get_http_method():
    """Prompts for an HTTP method and validates it."""
    methods = ['GET', 'POST', 'PATCH', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'HEAD']
    print(Fore.CYAN + "🌐 Available HTTP methods: " + ", ".join(methods))
    method = input(Fore.CYAN + " ➜  Select an HTTP method (default: HEAD): ").strip().upper() or "HEAD"
    return method if method in methods else "HEAD"


def get2_scan_inputs():
    """Handles user input for CIDRs, ports, output file, and threads for scanning."""
    invalid_attempts = 0
    hosts = []

    # Prompt user to select input method (manual or from file)
    while True:
        input_choice = get_input(Fore.CYAN + " Would you like to input CIDRs manually or from a file? (M/F): ").strip().lower()
        
        if input_choice == 'f':
            # Use the file manager to select the file if 'F' is chosen
            selected_file = file_manager(Path.cwd(), max_up_levels=3)
            
            if selected_file:  # If a valid file is selected
                hosts = get_cidrs_from_file(selected_file)
                if hosts:
                    break  # Break out of the loop after valid file input
                else:
                    print(Fore.RED + "⚠️ No valid IPs found in the CIDR file. Please try again.")
                    invalid_attempts += 1
            else:
                invalid_attempts += 1
                print(Fore.RED + "⚠️ No file selected or too many invalid attempts.")

        elif input_choice == 'm':
            hosts = get_cidrs_from_input()
            if hosts:
                break  # Break out of the loop after manual input
            else:
                print(Fore.RED + "⚠️ No valid IPs provided in manual input.")
                invalid_attempts += 1

        else:
            print(Fore.RED + "⚠️ Invalid choice. Please select 'M' for manual or 'F' for file.")
            invalid_attempts += 1

        if invalid_attempts >= 3:
            print(Fore.RED + "⚠️ Too many invalid attempts. Returning to main menu.")
            time.sleep(1)
            return None, None, None, None, None

    # Get ports with default value
    ports_input = get_input(Fore.CYAN + " ➜  Enter port list (default: 80): ").strip()
    ports = ports_input.split(',') if ports_input else ["80"]

    # Get output file name with default value
    output_file = get_input(Fore.CYAN + " ➜  Enter output file name (default: scan_results.txt): ").strip()
    if not output_file:
        output_file = "scan_results.txt"

    # Get number of threads with error handling
    while True:
        threads_input = get_input(Fore.CYAN + " ➜  Enter number of threads (default: 50): ").strip()
        if not threads_input:  # If input is empty, use default
            threads = 50
            break
        try:
            threads = int(threads_input)
            if threads <= 0:
                print(Fore.RED + "⚠️ Please enter a positive integer for the number of threads.")
                continue
            break
        except ValueError:
            print(Fore.RED + "⚠️ Invalid input. Please enter a valid integer for the number of threads.")
            
    http_method = get_http_method()  

    return hosts, ports, output_file, threads, http_method,


def format_row(code, server, port, host, use_colors=True):
    """Formats a row of results for printing or saving to a file."""
    if use_colors:
        return (Fore.GREEN + f"{code:<4} " +
                Fore.CYAN + f"{server:<20} " +
                Fore.YELLOW + f"{port:<5} " +
                Fore.LIGHTBLUE_EX + f"{host}")
    else:
        return f"{code:<4} {server:<20} {port:<5} {host}"


def check_http_response(host, port, method):
    """Checks the HTTP response for a given host, port, and method."""
    protocol = "https" if port in ['443', '8443'] else "http"
    url = f"{protocol}://{host}:{port}"
    try:
        response = requests.request(method, url, timeout=DEFAULT_TIMEOUT1, allow_redirects=True)
        location = response.headers.get('Location', '')
        if any(exclude in location for exclude in EXCLUDE_LOCATIONS):
            return None
        server_header = response.headers.get('Server', 'N/A')
        return response.status_code, server_header, port, host
    except requests.exceptions.RequestException:
        return None


def perform2_scan(hosts, ports, output_file, threads, method):
    """Performs the scan on specified hosts and ports using multithreading."""
    clear_screen()
    print(Fore.GREEN + f"🔍 Scanning using HTTP method: {method}...")

    headers = (Fore.GREEN + "Code  " + Fore.CYAN + "Server               " +
               Fore.YELLOW + "Port   " + Fore.LIGHTBLUE_EX + "Host" + Style.RESET_ALL)
    separator = "----  ----------------   ----  -------------------------"

    # Check if the output file already exists, and append to it
    existing_lines = 0
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_lines = sum(1 for _ in file)

    with open(output_file, 'a') as file:
        if existing_lines == 0:
            file.write(headers + "\n")
            file.write(separator + "\n")

    print(headers)
    print(separator)

    # Initialize counters for scan progress
    total_hosts = len(hosts) * len(ports)
    scanned_hosts = 0
    responded_hosts = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for host in hosts:
            for port in ports:
                # Submit HTTP check tasks to the thread pool
                futures.append(executor.submit(check_http_response, host, port, method))

        for future in as_completed(futures):
            result = future.result()
            scanned_hosts += 1

            if result:
                responded_hosts += 1
                code, server, port, host = result
                result_row = format_row(code, server, port, host)

                # Print and save the result
                print(result_row)
                with open(output_file, 'a') as file:
                    file.write(format_row(code, server, port, host, use_colors=False) + "\n")

            # Display scan progress
            progress_line = (Fore.YELLOW +
                             f"Scanned {scanned_hosts}/{total_hosts} - Responded: {responded_hosts}")
            print(progress_line, end='\r')

    print(f"\n\n{Fore.GREEN}✅ Scan completed! Results saved to {output_file}.")
