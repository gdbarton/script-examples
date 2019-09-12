#!/usr/bin/env python3

# loadtest.py

import random
from os import getenv
from time import sleep

import asks
import trio
from dotenv import load_dotenv


async def creator(url, mac, cookie):
    form = {'device_type': 'Other', 'mac': mac}
    r = await asks.post(url, data=form, cookies=cookie)
    print("HTTP status code: {}".format(int(r.status_code)))


async def runner(mac_list, MACS_PER_SEC, url, cookie):
    while len(mac_list) > (MACS_PER_SEC - 1):
        mac_bunch = []
        for i in range(MACS_PER_SEC - 1):
            mac_bunch.append(mac_list.pop())

        async with trio.open_nursery() as n:
            for mac in mac_bunch:
                n.start_soon(creator, url, mac, cookie)

        sleep(1)

    # Send the last of the MAC addresses
    async with trio.open_nursery() as n:
        for mac in mac_list:
            n.start_soon(creator, url, mac, cookie)


def main():
    load_dotenv(verbose=True)

    TOTAL_MACS = int(getenv('TOTAL_MACS'))
    MACS_PER_SEC = int(getenv('MACS_PER_SEC'))
    FORM_URL = ""

    # Generate random MACs. Store them in a list and in a file.
    mac_list = []
    with open('mac_list.txt', 'w') as writefile:
        for i in list(range(TOTAL_MACS)):
            mac_list.append("02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                                         random.randint(0, 255),
                                                         random.randint(0, 255)))
            writefile.write(mac_list[i] + "\n")

    # Give the user a time estimate.
    est_length_in_seconds = TOTAL_MACS // MACS_PER_SEC
    if est_length_in_seconds > 60:
        minutes = est_length_in_seconds // 60
        seconds = est_length_in_seconds - (minutes * 60)
    else:
        minutes = 0
        seconds = est_length_in_seconds

    print("Starting endpoint creation. Estimated length of time: {} minute(s) and {} seconds".format(
        minutes, seconds))
    sleep(3)

    cookie = {
        '_ga': '',
        'ajs_anonymous_id': '',
        'ajs_group_id': '',
        'ajs_user_id': '',
        'session': ''
    }

    trio.run(runner, mac_list, MACS_PER_SEC, FORM_URL, cookie)


main()
