import urllib.parse
import json
import http.client

import requests


def sendRPC(method, payload):
    # Requests doesn't work here, it mangles the JSON command
    params = json.dumps({"method": method, "params": payload})
    command = urllib.parse.quote(params, safe="{},:[]").replace("%20", "")
    conn = http.client.HTTPSConnection("service.yourcloudlibrary.com")
    payload = ''
    conn.request("POST", f"/json/rpc?json={command}", payload)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))


def get(cookies, url, path, route):
    _data = urllib.parse.quote(route, safe="")
    total = url + f"{path}_data={_data}"
    response = requests.get(total, cookies=cookies, verify=False)
    return response.json()


def post(cookies, url, path, route):
    _data = urllib.parse.quote(route, safe="")
    total = url + f"{path}_data={_data}"
    payload = {"format": "", "sort": "BorrowedDateDescending"}
    print(total + " " + json.dumps(payload))
    response = requests.post(total, cookies=cookies, verify=False, data=payload)
    print(str(response.status_code))
    return response.json()
