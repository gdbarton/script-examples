#!/usr/bin/env python3

import requests
import sys


def main():
    if len(sys.argv) != 2:
        print("Only one argument accepted.")
        sys.exit(1)

    url = ""
    file = sys.argv[1]

    cookie = {
        '_ga': '',
        'ajs_anonymous_id': '',
        'ajs_group_id': '',
        'ajs_user_id': '',
        'session': ''
    }

    with open(file, 'r') as readfile:
        for mac in readfile:
            r = requests.get(url + mac.rstrip(), cookies=cookie)
            print(str(r.status_code))


main()
