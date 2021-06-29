#!/usr/bin/python3
import requests

BASE = 'https://render-tron.appspot.com/screenshot/'

def webscreenshot(url):
    path = '../images/'+url.split("/")[2]+'.jpg'
    response = requests.get(BASE + url, stream=True)
    if response.status_code == 200:
        print("WEB OK")
        with open(path, 'wb') as file:
            for chunk in response:
                file.write(chunk)

# webscreenshot("https://towardsdatascience.com/find-similar-images-using-autoencoders-315f374029ea")