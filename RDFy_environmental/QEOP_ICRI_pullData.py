#This python script pulls data from the QEOP ICRI API into a CSV format data
#To be used in conjunction with Python Script QEOP_ICRI_rdfTransform.py
#IOTkit dashboard can be viewed here: https://dashboard.us.enableiot.com/ui/auth#/login
#The script is based on the pull.py script

import sys, requests, json, uuid, time
import pandas as pd

import urllib, csv, time, io, os
from rdflib import URIRef, Literal, Namespace, plugin, Graph
from rdflib.store import Store

from time import strftime

from json import dumps, loads, JSONEncoder, JSONDecoder

host = "dashboard.us.enableiot.com"
username= "agata.brok.13@ucl.ac.uk"
password= "Agatabrokagatabrok44$"
account_name= "QEOP"

device_id= "ICRI-QEOP-0001"
cid= "windspeed"
cid2= "barometer"
cid3= "rainrate"
cid4= "outside_temp"
cid5= "inside_humid"

api_root="/v1/api"
base_url= "https://{0}{1}".format(host, api_root)
device_name = "Device-{0}".format(device_id)

g_user_token=""

proxies={
}

verify = True

pathf = "/Users/patrick/3cixty/IN/intel/icriQEOPsensors/"


def check(resp, code):
	if resp.status_code != code:
        	print "Expected {0}. Got {1} {2}".format(code, resp.status_code, resp.text)
        	sys.exit(1)


def get_user_headers():
    headers = {
        'Authorization': 'Bearer ' + g_user_token,
        'content-type': 'application/json'
    }
    #print "Headers = " + str(headers)
    return headers

def get_token(username, password):
    url = "{0}/auth/token".format(base_url)
    headers = {'content-type': 'application/json'}
    payload = {"username": username,
               "password": password
               }
    data = json.dumps(payload)
    resp = requests.post(url, data=data, headers=headers, proxies=proxies, verify=verify)
    check(resp, 200)
    js = resp.json()
    token = js['token']
    return token

def get_user_id():
    url = "{0}/auth/tokenInfo".format(base_url)
    resp = requests.get(url, headers=get_user_headers(), proxies=proxies, verify=verify)
    check(resp, 200)
    js = resp.json()
    user_id = js["payload"]["sub"]

    return user_id

def get_account_id(user_id, account_name):
    url = "{0}/users/{1}".format(base_url, user_id)
    resp = requests.get(url, headers=get_user_headers(), proxies=proxies, verify=verify)
    check(resp, 200)
    js = resp.json()
    if "accounts" in js:
        accounts = js["accounts"]
        for k, v in accounts.iteritems():
            if 'name' in v and v["name"] == account_name:
                return k
    print "Account name {0} not found.".format(account_name)
    print "Available accounts are: {0}".format([v["name"] for k, v in accounts.iteritems()])
    return None

def get_observations(account_id, device_id,
                     cid,
                     cid2,
                     cid3,
                     cid4,
                     cid5):
    fromTime = -6000 #specify (epoch) time range from which the data is collected
    #endTime = ""
    url = "{0}/accounts/{1}/data/search".format(base_url, account_id)
    search = {"from": fromTime ,
            "targetFilter": {"deviceList":[device_id]},
                    "metrics":[{"id": cid},
                               {"id":cid2},
                               {"id":cid3},
                               {"id":cid4},
                               {"id":cid5}]
              ,"queryMeasureLocation": True
            }
    data = json.dumps(search)
    resp = requests.post(url, data=data, headers=get_user_headers(), proxies=proxies, verify=verify)
    x= resp.json()

    row = []

    for i in range(len(x['series'])):
        to = x['to']
        ffrom = x['from']

        for j in range(len(x['series'][i]['points'])):
            deviceName = x['series'][i]['deviceName']
            componentName = x['series'][i]['componentName']
            componentType = x['series'][i]['componentType']
            timeStamp = x['series'][i]['points'][j]['ts']
            value = x['series'][i]['points'][j]['value']

            row.append(to)
            row.append(ffrom)
            row.append(deviceName)
            row.append(componentName)
            row.append(componentType)
            row.append(timeStamp)
            row.append(value)

    lol = lambda lst, sz: [lst[i:i + sz] for i in range(0, len(lst), sz)]
    row= lol(row, 7)
    print row


    with open(pathf + device_id + "_"+ strftime("%Y%m%d")+".csv", "wb+") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(row)

    with open(pathf +"header" + "_" + strftime("%Y%m%d") + ".csv", "wb+") as outcsv:
        writer = csv.DictWriter(outcsv,
                                fieldnames=['to',
                                            'from',
                                            'deviceName',
                                            'componentName',
                                            'componentType',
                                            'timeStamp',
                                            'value'])
        writer.writeheader()

        with open(pathf + device_id + "_"+ strftime("%Y%m%d")+".csv", 'rb') as incsv:
            reader = csv.reader(incsv)
            writer.writerows({'to': row[0],
                              'from': row[1],
                              'deviceName': row[2],
                              'componentName': row[3],
                              'componentType': row[4],
                              'timeStamp': row[5],
                              'value': row[6]} for row in reader)

            return row

def print_observation_counts(row):  # js is result of /accounts/{account}/data/search
    if "series" in row:
        series = row["series"]
        series = sorted(series, key=lambda v: v["deviceName"])
        for v in series:
            print "Device: {0} Count: {1}".format(v["deviceName"], len(v["points"]))


def main():
        ####ICRI
        global g_user_token
        g_user_token = get_token(username, password)
        uid = get_user_id()
        print "USER ID: {0}".format(uid)

        aid = get_account_id(uid, account_name)
        print "AccountID: {0}".format(aid)

        o = get_observations(aid,
                             device_id,
                             cid,
                             cid2,
                             cid3,
                             cid4,
                             cid5)
        print_observation_counts(o)
        print o

if __name__ == "__main__":
    main();

