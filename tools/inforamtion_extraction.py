#!/usr/bin/python3
import whois
from datetime import datetime
import requests
import whois
import ssl, socket
from urllib.parse import urlparse,urlencode

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

def getLength(domain):
    try:      
        domain_name = domain
        return len(domain_name)
    except:
        print("Cant get domain name")
        return None
 
def domainAge(domain):
    try:
        domain_name = domain
        creation_date = domain_name.creation_date
        expiration_date = domain_name.expiration_date
        if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
            try:
                creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
                expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
            except:
                return None
        if ((expiration_date is None) or (creation_date is None)):
            return None
        elif ((type(expiration_date) is list) or (type(creation_date) is list)):
            return None
        else:
            ageofdomain = abs((expiration_date - creation_date).days)

            return ageofdomain
    except:
        print("Cant get domain name")
        return None

def extract_ca(domain):
    
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain['domain_name']) as s:
            s.settimeout(5)
            s.connect((domain['domain_name'], 443))
            cert = s.getpeercert()

        subject = dict(x[0] for x in cert['subject'])
        issued_to = subject['commonName']
        issuer = dict(x[0] for x in cert['issuer'])
        issued_by = issuer['commonName']

        return issued_by
    except:
        print(f"DOMAIN {domain} ERROR")

def js_analysis(url):

    js_extract = {}
    response = requests.get(url)
    raw_html = response.text
    js_extract['number eval'] = raw_html.count("eval")
    js_extract['number iframe'] = raw_html.count("iframe")
    js_extract['number unescape'] = raw_html.count("unescape")
    js_extract['number escape'] = raw_html.count("escape")
    js_extract['number ActiveXObject'] = raw_html.count("ActiveXObject")
    js_extract['number concat'] = raw_html.count("concat")
    js_extract['number fromCharCode'] = raw_html.count("fromCharCode")
    js_extract['number atob'] = raw_html.count("atob")

    return js_extract
def extract(url):
    try:
        data = {}
        domain = whois.whois(urlparse(url).netloc)
        # if len(domain <= 6):
        #     return 1

        data['url length'] = getLength(domain)
        data['Domain Age'] = domainAge(domain)
        data['Authority Certificate'] = extract_ca(domain)
        data['js'] = js_analysis(url)
        
        return data
    except:
        return data
        # print(f"DOMAIN {domain} ERROR")

print(extract("https://www.facebook.com/"))