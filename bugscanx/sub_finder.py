import sys
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import requests
from colorama import Fore, Style, Back, init
from bs4 import BeautifulSoup
init(autoreset=True)
from bugscanx.sub_scan import get_input
file_write_lock = threading.Lock()

# Session object for persistent HTTP requests
session = requests.Session()
DEFAULT_TIMEOUT2 = 10  # Default timeout for HTTP requests


def fetch_subdomains(source_func, domain):
    """Fetch subdomains using the provided source function."""
    try:
        subdomains = source_func(domain)  # Fetch subdomains using the source function
        return set(sub for sub in subdomains if isinstance(sub, str))  # Return unique subdomains
    except Exception as e:
        return set()  # Return empty set in case of an error


# Source: crt.sh (SSL Certificate Transparency logs)
def crtsh_subdomains(domain):
    """Fetch subdomains from crt.sh SSL Certificate Transparency logs."""
    subdomains = set()
    response = session.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200 and response.headers.get('Content-Type') == 'application/json':
        for entry in response.json():
            subdomains.update(entry['name_value'].splitlines())  # Update subdomains set
    return subdomains


# Source: HackerTarget (Passive DNS lookup)
def hackertarget_subdomains(domain):
    """Fetch subdomains from HackerTarget API."""
    subdomains = set()
    response = session.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200 and 'text' in response.headers.get('Content-Type', ''):
        subdomains.update([line.split(",")[0] for line in response.text.splitlines()])  # Parse the subdomains
    return subdomains


# Source: RapidDNS (Domain search)
def rapiddns_subdomains(domain):
    """Fetch subdomains from RapidDNS.io."""
    subdomains = set()
    response = session.get(f"https://rapiddns.io/subdomain/{domain}?full=1", timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML response
        for link in soup.find_all('td'):
            text = link.get_text(strip=True)
            if text.endswith(f".{domain}"):  # Check for valid subdomain
                subdomains.add(text)  # Add subdomain to set
    return subdomains


# Additional Source: AnubisDB (Passive DNS lookup)
def anubisdb_subdomains(domain):
    """Fetch subdomains from AnubisDB."""
    subdomains = set()
    response = session.get(f"https://jldc.me/anubis/subdomains/{domain}", timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200:
        subdomains.update(response.json())  # Add subdomains from JSON response
    return subdomains


# Additional Source: AlienVault OTX (Passive DNS lookup)
def alienvault_subdomains(domain):
    """Fetch subdomains from AlienVault OTX."""
    subdomains = set()
    response = session.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns", timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200:
        for entry in response.json().get("passive_dns", []):
            subdomains.add(entry.get("hostname"))  # Add subdomains from the response
    return subdomains


def urlscan_subdomains(domain):
    """Fetch subdomains from URLScan.io."""
    subdomains = set()
    url = f"https://urlscan.io/api/v1/search/?q=domain:{domain}"
    
    try:
        response = session.get(url, timeout=DEFAULT_TIMEOUT2)
        if response.status_code == 200:
            data = response.json()
            for result in data.get('results', []):
                page_url = result.get('page', {}).get('domain')
                if page_url and page_url.endswith(f".{domain}"):  # Check for subdomain
                    subdomains.add(page_url)  # Add subdomain to set
    except requests.RequestException:
        pass  # Handle connection issues gracefully
    return subdomains


# Caching mechanism to avoid refetching duplicate entries
recently_seen_subdomains = set()  # This set stores recently seen subdomains to avoid redundancy

def c99_subdomains(domain, days=10):  # Reduce days for fewer requests
    """Fetch subdomains from C99 Subdomain Finder with caching."""
    base_url = "https://subdomainfinder.c99.nl/scans"
    subdomains = set()

    # Generate URLs only for the most recent days
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
    urls = [f"{base_url}/{date}/{domain}" for date in dates]

    def fetch_url(url):
        """Fetch subdomains from a specific URL."""
        try:
            response = session.get(url, timeout=DEFAULT_TIMEOUT2)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    text = link.get_text(strip=True)
                    if text.endswith(f".{domain}") and text not in recently_seen_subdomains:
                        subdomains.add(text)  # Add unique subdomains to the set
                        recently_seen_subdomains.add(text)  # Cache the fetched subdomain
        except requests.RequestException:
            pass  # Avoid retries to reduce wait time

    # Thread pool optimized to a reasonable number of workers
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            future.result()  # Process each completed fetch

    return subdomains


def display_progress_bar(progress, total, length=30):
    """Display a progress bar while fetching subdomains."""
    filled_length = int(length * progress // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    percent = (progress / total) * 100
    sys.stdout.write(f'\r|{bar}| {percent:.2f}% Completed')  # Update progress bar in terminal
    sys.stdout.flush()
    if progress == total:
        sys.stdout.write('\n')  # Ensure a new line after completion


def process_domain(domain, output_file, sources):
    """Process a domain by fetching subdomains from multiple sources."""
    print(Fore.CYAN + f"🔍 Enumerating {domain}\n")
    
    subdomains = set()
    total_sources = len(sources)  # Total number of sources to query
    progress_counter = 0  # Track progress

    # Lock to control progress updates safely across threads
    progress_lock = threading.Lock()

    def fetch_and_update(source, domain):
        """Fetch subdomains from a source and update progress."""
        nonlocal progress_counter
        result = fetch_subdomains(source, domain)
        with progress_lock:
            subdomains.update(result)  # Add the new subdomains to the set
            progress_counter += 1
            display_progress_bar(progress_counter, total_sources)  # Update progress bar

    # Process each source concurrently and show progress
    with ThreadPoolExecutor(max_workers=min(total_sources, 10)) as source_executor:
        futures = {source_executor.submit(fetch_and_update, source, domain): source for source in sources}
        for future in as_completed(futures):
            future.result()  # Ensure each fetch is completed

    print(Fore.GREEN + f"\n✅ Completed {domain} - {len(subdomains)} subdomains found")
    
    # Write results to the output file
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"\n# Subdomains for {domain}\n")
        for subdomain in sorted(subdomains):
            file.write(f"{subdomain}\n")


def find_subdomains():
    """Main function to find subdomains either from a single domain or multiple from a file."""
    input_choice = get_input(Fore.CYAN + " \n ➜  Enter '1' for single domain or '2' for multiple from txt file: ").strip()
    
    if input_choice == '1':
        domain = get_input(Fore.CYAN + "\n ➜  Enter the domain to find subdomains for: ").strip()
        if not domain:
            print(Fore.RED + "\n⚠️ Domain cannot be empty.")
            return
        domains_to_process = [domain]
        sources = [
            crtsh_subdomains, hackertarget_subdomains, rapiddns_subdomains,
            anubisdb_subdomains, alienvault_subdomains,
            urlscan_subdomains, c99_subdomains
        ]
        default_filename = f"{domain}_subdomains.txt"
        
    elif input_choice == '2':
        file_path = get_input(Fore.CYAN + "\n ➜  Enter the path to the file containing domains: ").strip()
        try:
            with open(file_path, 'r') as file:
                domains_to_process = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(Fore.RED + "\n⚠️ File not found. Please check the path.")
            return

        sources = [
            crtsh_subdomains, hackertarget_subdomains, rapiddns_subdomains,
            anubisdb_subdomains, alienvault_subdomains,
            urlscan_subdomains
        ]

        # Default filename if user doesn't specify one, based on file name without path or extension
        default_filename = f"{file_path.split('/')[-1].split('.')[0]}_subdomains.txt"
    
    else:
        print(Fore.RED + "\n⚠️ Invalid choice.")
        return

    output_file = get_input(Fore.CYAN + "\n ➜ Enter the output file name (without extension): ").strip()
    # Use default filename if user input is empty
    output_file = output_file + "_subdomains.txt" if output_file else default_filename

    # Use a ThreadPoolExecutor with max_workers=3 for domain processing
    with ThreadPoolExecutor(max_workers=3) as domain_executor:
        futures = {domain_executor.submit(process_domain, domain, output_file, sources): domain for domain in domains_to_process}

        for future in as_completed(futures):
            future.result()  # Wait for each domain processing to complete

    print(Fore.GREEN + f"\n✅ All results saved to {output_file}")
