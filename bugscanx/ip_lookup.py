import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import random
import threading
import requests
from colorama import Fore, Style, Back, init
import ipaddress
from bs4 import BeautifulSoup
from bugscanx.sub_scan import get_input

# Initialize colorama for colored terminal output
init(autoreset=True)

# Lock for writing to the file to avoid race conditions
file_write_lock = threading.Lock()

# List of common user-agent strings to simulate browser requests

USER_AGENTS = [ 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/114.0.1823.67",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 12; Mobile; rv:115.0) Gecko/115.0 Firefox/115.0",
    "Mozilla/5.0 (Android 13; Tablet; rv:112.0) Gecko/112.0 Firefox/112.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro Build/SQ3A.220605.009) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; .NET CLR 4.0.30319; .NET4.6; .NET4.5; .NET4.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; .NET4.0; .NET4.6; .NET4.5; .NET4.7) like Gecko"
]

EXTRA_HEADERS = { 
    "X-Originating-IP": "127.0.0.1",
    "X-Forwarded-For": "127.0.0.1",
    "X-Remote-IP": "127.0.0.1",
    "X-Remote-Addr": "127.0.0.1",
    "X-Client-IP": "127.0.0.1",
    "X-Host": "127.0.0.1",
    "X-Forwarded-Host": "127.0.0.1"
}

def fetch_rapiddns(ip):
    base_url = f"https://rapiddns.io/sameip/{ip}"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        **EXTRA_HEADERS
    }
    time.sleep(random.uniform(1, 3))  # Delay before request
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return [row.find_all('td')[0].text.strip() for row in soup.find_all('tr') if row.find_all('td')]
    except requests.RequestException:
        return []


def fetch_yougetsignal(ip):
    url = "https://domains.yougetsignal.com/domains.php"
    data = {
        'remoteAddress': ip,
        'key': '',
        '_': ''
    }
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        response.raise_for_status()
        return [domain[0] for domain in response.json().get("domainArray", [])]
    except requests.RequestException:
        return []


def fetch_bing(ip):
    base_url = f"https://www.bing.com/search?q=ip%3A{ip}"
    time.sleep(random.uniform(1, 3))  # Delay before request
    try:
        response = requests.get(base_url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        return [title['href'].split('/')[2] for row in soup.find_all('li', class_='b_algo') if (title := row.find('a'))]
    except requests.RequestException:
        return []




def extract_domains_for_ip(ip):
    domains = []
    print(Fore.CYAN + f"🔎 Searching domains for IP: {ip}")
    
    # Fetch from all sources
    domains += fetch_rapiddns(ip)
    domains += fetch_yougetsignal(ip)
    domains += fetch_bing(ip)

    # Remove duplicates using set
    domains = sorted(set(domains))
    
    # Display only the number of domains found
    print(Fore.GREEN + f"✔️ Domains found for IP {ip}: {len(domains)}")
    
    return (ip, domains)

def save_results_to_file(results, output_file):
    total_domains_found = 0  # Track the total number of domains found
    with open(output_file, 'a') as f:
        for ip, domains in results:
            total_found = len(domains)
            total_domains_found += total_found
            f.write(f"Domains found for IP {ip}: {total_found}\n")
            for domain in domains:
                f.write(f"{domain}\n")
    print(Fore.GREEN + f"\n✅ Saved! Current total domains found across processed IPs: {total_domains_found}")

def process_cidr(cidr, ip_queue):
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        for ip in network.hosts():
            ip_queue.put(str(ip))
    except ValueError as e:
        print(f"Invalid CIDR block {cidr}: {e}")

def Ip_lockup_menu():
    cidr_or_filename = get_input(Fore.CYAN + " ➜  Enter an IP or CIDR or file containing IPs/CIDRs: ")
    output_file = get_input(Fore.CYAN + " ➜  Enter the output file path: ")

    ip_queue = Queue()

    if '/' in cidr_or_filename:  # Check if input is CIDR
        try:
            ipaddress.ip_network(cidr_or_filename, strict=False)
            process_cidr(cidr_or_filename, ip_queue)
        except ValueError:
            print(Fore.RED + f"❌ Invalid CIDR: {cidr_or_filename}")
            return
    else:
        try:
            ip = ipaddress.ip_address(cidr_or_filename)
            ip_queue.put(str(ip))
        except ValueError:
            try:
                with open(cidr_or_filename, 'r') as f:
                    for line in f:
                        entry = line.strip()
                        if entry:
                            try:
                                ip = ipaddress.ip_address(entry)
                                ip_queue.put(str(ip))
                            except ValueError:
                                print(Fore.RED + f"❌ Invalid IP address: {entry}")
            except FileNotFoundError:
                print(Fore.RED + f"❌ File not found: {cidr_or_filename}")
                return
            except Exception as e:
                print(Fore.RED + f"❌ An error occurred: {e}")
                return

    total_ips = ip_queue.qsize()
    if total_ips == 0:
        print(Fore.RED + "⚠️ No valid IPs/CIDRs to process.")
        return

    # Get number of threads from the user
    while True:
        threads_input = get_input(Fore.CYAN + " ➜  Enter the number of threads to use (1-5): ").strip()
        if threads_input.isdigit():
            threads = int(threads_input)
            if 1 <= threads <= 5:
                break
            else:
                print(Fore.RED + "⚠️ Please enter a number between 1 and 5.")
        else:
            print(Fore.RED + "⚠️ Invalid input. Please enter a valid integer.")

    results = []
    progress = 0  # Initialize progress counter

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(extract_domains_for_ip, ip_queue.get()) for _ in range(total_ips)]
        
        for i, future in enumerate(futures, start=1):
            results.append(future.result())
            progress += 1

            # Update progress and save results to file every 5 IPs
            if i % 5 == 0 or i == total_ips:
                percent_complete = (progress / total_ips) * 100
                print(Fore.YELLOW + f"\r⏳ Progress: {progress}/{total_ips} IPs processed ({percent_complete:.2f}%)", end="")
                save_results_to_file(results[-5:], output_file)  # Save only the last 5 results to the file
    
    print()  # Move to the next line after the final progress bar update
    print(Fore.GREEN + "\n🎉 All IPs processed!")
