#!/usr/bin/env python3
from pykeepass import PyKeePass
import getpass

# ask fo password
try:
    password = getpass.getpass(prompt='Password: ', stream=None)
except Exception as error:
    print('ERROR', error)

# load db
kp = PyKeePass('marx.kdbx', password)

# find any entry by its title
entry = kp.find_entries(title='SEALED_TEST_ENTRY', first=True)
print(entry.password)