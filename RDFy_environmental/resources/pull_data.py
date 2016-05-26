import sys
import requests
import json
import uuid
import time
import random

host = "dashboard.us.enableiot.com"
username= <your EnableIoT username>
password= <your EnableIoT password>
account_name= <EnableIoT account name>

device_id= <your device ID>
cid= <the component ID>

api_root="/v1/api"
base_url= "https://{0}{1}".format(host,api_root)
device_name = "Device-{0}".format(device_id)

g_user_token=""

proxies={
}

verify = True

def main():

	global g_user_token
	g_user_token=get_token(username,password)
	uid=get_user_id()
	print "USER ID: {0}".format(uid)

	aid=get_account_id(uid,account_name)
	print "AccountID: {0}".format(aid)

	o= get_observations(aid,device_id,cid)
	print_observation_counts(o) 
	print o



def check(resp, code):                            
	if resp.status_code != code:                 
        	print "Expected {0}. Got {1} {2}".format(code, resp.status_code, resp.text)
        	sys.exit(1) 


def get_user_headers():
    headers = {
        'Authorization': 'Bearer ' + g_user_token,
        'content-type': 'application/json'
    }
#    print "Headers = " + str(headers)
    return headers	

def get_token(username, password):
    url = "{0}/auth/token".format(base_url)
    headers = {'content-type': 'application/json'}
    payload = {"username": username, "password": password}
    data = json.dumps(payload)
    resp = requests.post(url, data=data, headers=headers, proxies=proxies, verify=verify)
    check(resp, 200)
    js = resp.json()
#    print js
    token = js['token']
    return token

def get_user_id():
    url = "{0}/auth/tokenInfo".format(base_url)
    resp = requests.get(url, headers=get_user_headers(), proxies=proxies, verify=verify)
    check(resp, 200)
    js = resp.json()
#    print js
    user_id = js["payload"]["sub"]
    
    
    return user_id


def get_account_id(user_id, account_name):
    url = "{0}/users/{1}".format(base_url, user_id)
    resp = requests.get(url, headers=get_user_headers(), proxies=proxies, verify=verify)
    check(resp, 200)
    js = resp.json()
    if 'accounts' in js:
        accounts = js["accounts"]
        for k, v in accounts.iteritems():
            if 'name' in v and v["name"] == account_name:
                return k
    print "Account name {0} not found.".format(account_name)
    print "Available accounts are: {0}".format([v["name"] for k, v in accounts.iteritems()])
    return None

def get_observations(account_id, device_id, component_id):
    url = "{0}/accounts/{1}/data/search".format(base_url, account_id)
    search = {
        "from": 0,
        "targetFilter": {
            "deviceList": [device_id]
        },
        "metrics": [
            {
                "id": component_id
            }
        ]


    }
    data = json.dumps(search)
    resp = requests.post(url, data=data, headers=get_user_headers(), proxies=proxies, verify=verify)
    check(resp, 200)
    js = resp.json()
    return js

def print_observation_counts(js):  # js is result of /accounts/{account}/data/search
    if 'series' in js:
        series = js["series"]
        series = sorted(series, key=lambda v: v["deviceName"])
        for v in series:
            print "Device: {0} Count: {1}".format(v["deviceName"], len(v["points"]))



main()



