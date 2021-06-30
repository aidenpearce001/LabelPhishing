#!/usr/bin/python3
import whois
from datetime import datetime
import requests

ca = ['cPanel,',
 'Microsoft',
 'HydrantID',
 'AlphaSSL',
 'GTS',
 'RapidSSL',
 'DFN-Verein',
 'Cloudflare',
 'GeoTrust',
 'QuoVadis',
 'Certum',
 'Amazon',
 'Gandi',
 'COMODO',
 'Go',
 'Cybertrust',
 'GlobalSign',
 'Yandex',
 'R3',
 'Network',
 'DigiCert',
 'GoGetSSL',
 'Thawte',
 'Apple',
 'Starfield',
 'RU-CENTER',
 'Trustwave',
 'Entrust',
 'InCommon',
 'Sectigo',
 'Secure']

def getLength(url):
    try:      
        domain_name = whois.whois(urlparse(url).netloc)   
        return len(domain_name)
    except:
        print("Cant get domain name")
        return None
 
def domainAge(url):
    try:
        domain_name = whois.whois(urlparse(url).netloc)
        creation_date = domain_name.creation_date
        expiration_date = domain_name.expiration_date
        if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
            try:
                creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
                expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
            except:
                return 1
        if ((expiration_date is None) or (creation_date is None)):
            return 1
        elif ((type(expiration_date) is list) or (type(creation_date) is list)):
            return 1
        else:
            ageofdomain = abs((expiration_date - creation_date).days)

            return ageofdomain
    except:
        print("Cant get domain name")
        return None

def extract_ca(url):
    
    try:
        hostname = whois.whois(urlparse(url).netloc)
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, 443))
            cert = s.getpeercert()

        subject = dict(x[0] for x in cert['subject'])
        issued_to = subject['commonName']
        issuer = dict(x[0] for x in cert['issuer'])
        issued_by = issuer['commonName']

        return issued_by
    except:
        print(f"DOMAIN {domain} ERROR")