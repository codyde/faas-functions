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
    i = get_rest_api_data('/rest/vcenter/vm')
    print(json.dumps(i.json(),indent=4))


def auth_vcenter_rest(url):
    username = os.environ['user']
    password = os.environ['pw']
    resp = requests.post('https://{}/rest/com/vmware/cis/session'.format(url),
                         auth=(username, password), verify=False)
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp.json()['value']


def get_rest_api_data(req_url):
    url = os.environ['vc_fqdn']
    sid = auth_vcenter_rest(url)
    resp = requests.get('https://{}{}'.format(url,req_url), verify=False,
                        headers={'vmware-api-session-id': sid})
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp


