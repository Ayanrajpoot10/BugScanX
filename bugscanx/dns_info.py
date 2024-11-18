from colorama import Fore, init
import dns.resolver
import dns.reversename
init(autoreset=True)

def resolve_a_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return [answer.to_text() for answer in answers]
    except Exception as e:
        print(Fore.RED + f"⚠️ Error fetching A record: {e}")
        return []

def resolve_cname_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        return [answer.to_text() for answer in answers]
    except Exception as e:
        print(Fore.RED + f"⚠️ Error fetching CNAME record: {e}")
        return []

def resolve_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return [f"{answer.exchange} (priority: {answer.preference})" for answer in answers]
    except Exception as e:
        print(Fore.RED + f"⚠️ Error fetching MX record: {e}")
        return []

def resolve_ns_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        return [answer.to_text() for answer in answers]
    except Exception as e:
        print(Fore.RED + f"⚠️ Error fetching NS record: {e}")
        return []

def resolve_txt_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        return [answer.to_text() for answer in answers]
    except Exception as e:
        print(Fore.RED + f"⚠️ Error fetching TXT record: {e}")
        return []

def nslookup(domain):
    print(Fore.CYAN + f"\n🔍 Performing NSLOOKUP for: {domain}")

    # Collecting essential DNS records
    records = {
        "A": resolve_a_record(domain),
        "CNAME": resolve_cname_record(domain),
        "MX": resolve_mx_record(domain),
        "NS": resolve_ns_record(domain),
        "TXT": resolve_txt_record(domain),
    }

    # Display results
    for record_type, values in records.items():
        if values:
            print(Fore.GREEN + f"\n📝 {record_type} Records:")
            for value in values:
                print(Fore.LIGHTCYAN_EX + f"- {value}")
        else:
            print(Fore.RED + f"\nNo {record_type} records found for {domain}.")


