#!/usr/bin/env python3
from pykeepass import PyKeePass
import getpass
import re

# open YAML file
filein="test.yaml"
f = open(filein,'r')

# ask for KeePass password
try:
    password = getpass.getpass(prompt='Password: ', stream=None)
except Exception as error:
    print('ERROR', error)

# load KeePass db
kp = PyKeePass('marx.kdbx', password)

# define regex: ${VAR_NAME}
pattern = re.compile('.*?\${(\w+)}.*?')
# replace
for line in f:
    # find in line
    match = pattern.findall(line)
    for g in match:
        # lookup password
        entry = kp.find_entries(title=g, first=True)
        line = line.replace(f'${{{g}}}', entry.password)
        #print(g)
    print(line)
f.close()

