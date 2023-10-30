import json

from rpc import sendRPC
import requests


def authenticateAonymousCountry(country):
    return sendRPC("WSAuth.authenticateAnonymousUser", [country])["result"]["token"]


def login(url, library, username, password, cookies):
    payload = {"action": "login", "barcode": username, "library": library, "pin": password}
    response = requests.post(url + "?_data=root", data=payload, verify=False, cookies=cookies)
    print(response.content)
    return response
