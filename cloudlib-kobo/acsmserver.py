import requests

def convert(url, acsm):
    headers = {"Content-Type": "application/vnd.adobe.adept+xml"}
    return requests.post(url, data=acsm.encode('utf-8'), headers=headers)