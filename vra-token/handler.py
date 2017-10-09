import requests
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(
    InsecureRequestWarning)  # Disable SSL warning


def handle(req):
    """
    Builds an authentication token for the user. Takes input of the fqdn of vRA, username,
    password, and tenant
    """
    try:
        user = os.environ['user']
        password = os.environ['pw']
        tenant = os.environ['tenant']
        authurl = "{}/identity/api/tokens".format(req)
        payload = '{{"username":"{}","password":"{}","tenant":"{}"}}'.format(
            user, password, tenant)
        headers = {
            'accept': "application/json",
            'content-type': "application/json"
        }
        response = requests.request(
            "POST", authurl, data=payload, headers=headers, verify=False)
        j = response.json()['id']
        auth = "Bearer " + j
        token = {}
        token['bearer'] = auth
        print(json.dumps(token,indent=4))
    except:
        print("Unsuccessful Bearer Token Attempt")
