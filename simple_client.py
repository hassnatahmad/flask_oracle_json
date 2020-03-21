import requests
import crypto as cr
from requests.auth import HTTPBasicAuth

url = 'http://gisvms70.gis.goodyear.com:5000/api/ping'
auth = HTTPBasicAuth('lda5148', cr.decrypt(cr.lda5148_api))
response = requests.get(url, auth=auth)
assert response.status_code == 200
assert response.json()['message'] == 'Hello!'

url = 'http://gisvms70.gis.goodyear.com:5000/api/upload'
files = {'file': open('C:/Temp/ctl_example_prepared.json', 'rb')}
response = requests.post(url, auth=auth, files=files)
if response.status_code != 201:
    print('An error has occurred: {0} (code {1})'.format(response.json()['message'], response.status_code))
