#!/usr/bin/env python3

from uuid import UUID
import base64

with open("ldap_stuff.txt") as f:
    lines = f.readlines()

file = open("output.txt","w")

for line in lines:
    if "extensionAttribute" in line:
        file.write(line.split()[1] + ",")
    if "objectGUID" in line:
        file.write(str(UUID(bytes_le=base64.b64decode(line.split()[1]))) + "\n")

file.close()
print("Done.")

