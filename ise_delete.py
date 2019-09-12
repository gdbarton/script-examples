#!/usr/bin/env python3

# Grant Barton August 2019
# ise_delete.py

# delete stuff from ise

# arg1 is command (search, bulk_search, delete, or bulk_delete)
# arg2 is mac addr (if search) or unique location (if delete) or filename (if bulk_search or bulk_delete)

import requests
import sys
import csv
from os import getenv
from dotenv import load_dotenv


def help_info():
    print("Read the README. What's wrong with you?")
    sys.exit(1)


def delete_from_ise(front, location, auth):
    headers = {"ACCEPT": "Application/JSON"}
    r = requests.delete(front + location, auth=auth, headers=headers)

    if r.status_code == 204:
        print("Deleted location " + location)

    elif r.status_code == 401 or r.status_code == 403:
        print("HTTP status " + str(r.status_code) + ": unauthorized")
        sys.exit(1)
    elif r.status_code == 404:
        print("HTTP status 404: location not found: " + location)
    else:
        print("HTTP status " + str(r.status_code))
        sys.exit(1)


def search_ise(url, mac_addr, auth):
    headers = {"ACCEPT": "Application/JSON"}
    r = requests.get(url + "?filter=mac.EQ." + mac_addr, auth=auth, headers=headers)

    if r.status_code == 200:
        # no good if results != 1:
        if r.json()["SearchResult"]["total"] == 0:
            return 1, mac_addr + " not found"
        elif r.json()["SearchResult"]["total"] > 1:
            return 1, "Found more than one result in ISE for MAC " + mac_addr + "; this should never happen"
        else:
            link = r.json()["SearchResult"]["resources"][0]["link"]["href"]

            # Since MAC was in ISE, search for it's group's name:
            r = requests.get(link, auth=auth, headers=headers)
            if r.status_code == 200:
                group_id = r.json()["ERSEndPoint"]["groupId"]

                r = requests.get("" + group_id, auth=auth, headers=headers)
                if r.status_code == 200:
                    group = r.json()["EndPointGroup"]["name"]
                else:
                    return 1, mac_addr + " found, but group not identified. HTTP code " + str(r.status_code) + " when pulling group."
            else:
                return 1, mac_addr + " found, but group not identified. HTTP code " + str(r.status_code) + " when pulling device."

            location = link.split("/")[-1]
            return 0, location, group

    # If we don't get a 200, throw an error and quit because there's a network or permissions problem:
    elif r.status_code == 400:
        print(str(mac_addr) + " got HTTP status 400: missing or invalid information")
    elif r.status_code == 401 or r.status_code == 403:
        print(str(mac_addr) + " got HTTP status " + str(r.status_code) + ": unauthorized")
    else:
        print(str(mac_addr) + " got HTTP status " + str(r.status_code))

    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        help_info()

    if len(sys.argv) > 3:
        print("Too many arguments provided")
        sys.exit(1)

    command = sys.argv[1].lower()
    arg = sys.argv[2]
    url = ""

    load_dotenv(getenv('SECRET_ENV_FILE', '.env.private'), verbose=True)
    auth = getenv('API_USER'), getenv('API_PASSWORD')

    if command == "search":
        outcome = search_ise(url, arg, auth)
        print(outcome[1])
        if outcome[0] == 0:
            print("Group: " + outcome[2])

    elif command == "bulk_search":
        try:
            mac_file = open(arg, 'r')
        except FileNotFoundError:
            print("File not found, did you pass a correct path?")
            sys.exit(1)

        addrs = mac_file.readlines()

        with open('macs_and_locations.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for addr in addrs:
                location = search_ise(url, addr.rstrip(), auth)
                if location[0] == 0:
                    writer.writerow([addr.rstrip(), location[1], location[2]])
                else:
                    print(location[1])

    elif command == "delete":
        delete_from_ise(url, arg, auth)

    elif command == "bulk_delete":
        try:
            location_file = open(arg, 'r')
        except FileNotFoundError:
            print("File not found, did you pass a correct path?")
            sys.exit(1)

        locations = location_file.readlines()

        for location in locations:
            prepped_location = location.split(',')[1].rstrip()
            delete_from_ise(url, prepped_location, auth)

    else:
        help_info()


main()

