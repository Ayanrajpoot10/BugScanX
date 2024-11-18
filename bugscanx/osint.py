import threading
import requests
from colorama import Fore, Style, Back, init
import socket
import ssl
from requests.exceptions import RequestException
import concurrent

# Initialize colorama for colored terminal output
init(autoreset=True)

from bugscanx.sub_scan import get_input

# Lock for file writing (not currently used in this snippet)
file_write_lock = threading.Lock()

# List of HTTP methods to test
HTTP_METHODS = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH"]

# Function to check the response of a specific HTTP method for a URL
def check_http_method(url, method):
    try:
        # Make a request with the given method
        response = requests.request(method, url, timeout=5)
        # Print the status code and headers of the response
        print(Fore.LIGHTCYAN_EX + f"{method} response code: {response.status_code}")
        print(Fore.LIGHTMAGENTA_EX + f"{method} headers:\n{response.headers}")
    except RequestException as e:
        # Handle request failure (timeout, connection issues, etc.)
        print(Fore.RED + f"{method} request failed: {e}")

# Function to execute HTTP method checks concurrently for a given URL
def check_http_methods(url):
    print(Fore.GREEN + f"\nChecking HTTP methods for {url}...")
    # Create a thread pool to run the method checks concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a future for each HTTP method to be checked
        futures = [executor.submit(check_http_method, url, method) for method in HTTP_METHODS]
        # Wait for all futures to complete
        concurrent.futures.wait(futures)

# Function to retrieve Server Name Indication (SNI) information for a given host
def get_sni_info(host):
    print(Fore.GREEN + f"\nRetrieving SNI info for {host}...")
    try:
        # Create an SSL context to initiate secure connection
        context = ssl.create_default_context()
        # Connect to the host over SSL (port 443) to retrieve the certificate
        with socket.create_connection((host, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssl_sock:
                # Extract the server's SSL certificate details
                cert = ssl_sock.getpeercert()
                # Prepare a dictionary of relevant certificate details
                sni_info = {
                    "subject": dict(x[0] for x in cert["subject"]),
                    "issuer": dict(x[0] for x in cert["issuer"]),
                    "serialNumber": cert.get("serialNumber"),
                }
                # Print the SNI information
                print(Fore.LIGHTCYAN_EX + f"SNI Information: {sni_info}")
    except Exception as e:
        # Handle any SSL connection or certificate retrieval failures
        print(Fore.RED + f"Failed to retrieve SNI info: {e}")

# Main function to run all the checks concurrently for a given host
def osint_main():
    # Prompt the user for the host to analyze
    host = get_input(Fore.CYAN + " ➜  Enter the host (without 'http' or 'https'): ").strip()
    # Prepare the full URL for the host
    url = f"https://{host}"

    # Run HTTP methods check and SNI information retrieval concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute both tasks concurrently using threads
        executor.submit(check_http_methods, url)
        executor.submit(get_sni_info, host)

    # Reset style after the tasks are completed
    print(Style.RESET_ALL)
