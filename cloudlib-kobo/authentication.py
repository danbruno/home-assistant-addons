from rpc import sendRPC
import requests

AUTH_ROOT_URL = 'https://ebook.yourcloudlibrary.com/'

def authenticateAonymousCountry(country):
    return sendRPC("WSAuth.authenticateAnonymousUser", [country])["result"]["token"]

def populateConfigProdCookie(library):
    return requests.get(AUTH_ROOT_URL + 'library/' + library + '/', allow_redirects=False)

def login(library, username, password, cookies):

    payload = {"action": "login", "barcode": username, "library": library, "pin": password}
    response = requests.post(AUTH_ROOT_URL + "?_data=root", data=payload, verify=False, cookies=cookies)
    print(response.content)
    return response
