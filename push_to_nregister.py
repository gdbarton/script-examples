#!/usr/bin/env python3

import requests

api_endpoint=""
API_USER=""
API_PASSWORD=""

with open("mac_and_uuid_table.csv") as f:
    lines = f.readlines()

for line in lines:
    split_line = line.split(',')
    mac_addr = split_line[0]
    uuid = split_line[6].strip()

    outstuff = {"action": "create", "ad_guid": uuid, "user_guid": uuid, "device_name": "N/A", "location": "N/A", "mac": mac_addr, "expiry": "2019-09-22"}

    print(outstuff)

    api_response = requests.post(api_endpoint, auth=(API_USER, API_PASSWORD), json=outstuff)
    if not api_response.ok:
        print("u dun messed up lol")

    print(api_response.text)

    

