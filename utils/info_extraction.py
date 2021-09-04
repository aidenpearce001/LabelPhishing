#!/usr/bin/python3
import whois
from datetime import datetime
import requests
import ssl, socket
from urllib.parse import urlparse
import urllib.request
from bs4 import BeautifulSoup

def getLength(url):
    return len(url)
 
def domainAge(domain):
    try:
        domain_name = domain
        creation_date = domain_name.creation_date
        expiration_date = domain_name.expiration_date

        if len(creation_date) > 1:
            creation_date= creation_date[-1]
        if len(expiration_date) > 1:
            expiration_date= expiration_date[-1]
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
        print(f"Cant get domain name {}")
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
        return None
        print(f"DOMAIN {domain['domain_name']} ERROR")

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

def web_traffic(url):
    """
    get alexa web traffic
    """
    try:
    #Filling the whitespaces in the URL if any
        url = urllib.parse.quote(url)
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        rank = int(rank)
    except TypeError:
        return 1

    if rank <100000:
        return 0
    else:
        return 1

def extract(url):
    try:
        data = {}
        domain = whois.whois(urlparse(url).netloc)

        if domain['domain_name'] == None:
            data['url'] = url
            data['url length'] = getLength(url)
            data['Domain Age'] = None
            data['Authority Certificate'] = None
            data['js'] = None
            data['alexa_rank'] = web_traffic(url)

            return data
        else:
            data['url'] = url
            data['url length'] = getLength(url)
            data['Domain Age'] = domainAge(domain)
            data['Authority Certificate'] = extract_ca(domain)
            data['js'] = js_analysis(url)
            data['alexa_rank'] = web_traffic(url)

            return data

    except:
        data['url'] = url
        data['url length'] = getLength(url)
        data['Domain Age'] = None
        data['Authority Certificate'] = None
        data['js'] = None
        data['alexa_rank'] = web_traffic(url)
        
        return data
