#!/usr/bin/python3
import whois
from datetime import datetime
import requests

CA = [
    "Comodo",
    "Sectigo",
    "DigiCert",
    "Symantec",
    "RapidSSL",
    "GeoTrust",
    "Thawte"]

dns = 0
try:
    domain_name = whois.whois(urlparse(url).netloc)
# print(domain_name)
except:
    print("Cant get domain name")
    dns = 1
def domainAge(domain_name):
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
        print("Domain Age: ", ageofdomain)
        if ((ageofdomain/30) < 6):
            age = 1
        else:
            age = 0
        return age