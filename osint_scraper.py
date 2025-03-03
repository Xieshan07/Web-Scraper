import requests
from bs4 import BeautifulSoup
import re
import whois
import shodan

# Shodan API Key (Get from https://account.shodan.io/register)
SHODAN_API_KEY = "nUreassn80WiQ8eNR42Ez2Mx77MRPn1i"

import requests

def get_website_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"⚠️ Failed to fetch content. HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None



def extract_links(html):
    """Extract all links from a webpage"""
    soup = BeautifulSoup(html, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True)]

def extract_emails(html):
    """Extract emails from webpage"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, html)

def extract_phone_numbers(html):
    """Extract phone numbers"""
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    return re.findall(phone_pattern, html)

def get_whois_info(domain):
    """Fetch WHOIS domain info"""
    try:
        domain_info = whois.whois(domain)
        return {
            "Registrar": domain_info.registrar,
            "Creation Date": domain_info.creation_date,
            "Expiration Date": domain_info.expiration_date,
            "Registrant Email": domain_info.emails
        }
    except Exception as e:
        print(f"❌ Error fetching WHOIS data: {e}")
        return None

def get_shodan_info(domain):
    """Fetch domain info from Shodan"""
    try:
        shodan_api = shodan.Shodan(SHODAN_API_KEY)
        result = shodan_api.search(domain)
        
        return [{"IP": s['ip_str'], "Port": s['port'], "Org": s.get('org', 'N/A'), "OS": s.get('os', 'N/A')} for s in result['matches']]
    except Exception as e:
        print(f"❌ Error fetching Shodan data: {e}")
        return None

def main():
    url = input("🔗 Enter website URL (e.g., https://example.com): ").strip()
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    
    print("\n🔍 Fetching website content...")
    html = get_website_content(url)
    if not html:
        return
    
    print("\n📎 Extracting links...")
    print(extract_links(html) or "❌ No links found.")
    
    print("\n📩 Extracting emails...")
    print(extract_emails(html) or "❌ No emails found.")
    
    print("\n📞 Extracting phone numbers...")
    print(extract_phone_numbers(html) or "❌ No phone numbers found.")
    
    print("\n🌍 Fetching WHOIS information...")
    print(get_whois_info(domain) or "❌ No WHOIS data found.")
    
    print("\n🔎 Fetching Shodan data...")
    print(get_shodan_info(domain) or "❌ No Shodan data found.")

if __name__ == "__main__":
    main()
