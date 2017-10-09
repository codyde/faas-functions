import requests
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warning

def handle(req):
    """
    Builds an authentication token for the user. Takes input of the fqdn of vRA, username,
    password, and tenant
    """
    vrafqdn = os.environ['cloud_fqdn']
    user = os.environ['user']
    password = os.environ['pw']
    tenant = os.environ['tenant']
    url = "https://{}/identity/api/tokens".format(vrafqdn)
    payload = '{{"username":"{}","password":"{}","tenant":"{}"}}'.format(user, password, tenant)
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        }
    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    j = response.json()['id']
    auth = "Bearer "+j
    vraheaders = {
        'accept': "application/json",
        'authorization': auth
        }
    vraApiUrl = "https://{}/catalog-service/api/consumer/resources".format(vrafqdn)
    reqs = requests.request("GET", vraApiUrl, headers=vraheaders, verify=False).json()['content']
    print(json.dumps(reqs,indent=4))
