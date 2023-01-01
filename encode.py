#!/usr/bin/env python3
from pykeepass import PyKeePass
import getpass
import re
import subprocess
import argparse
import sys
import os
from pathlib import Path

def main(argv):
  # open source file
  f = open('./tmpl/cluster-secrets.yaml','r')

  # ask for KeePass password
  try:
    password = getpass.getpass(prompt='Password: ', stream=None)
  except Exception as error:
    print('ERROR', error)
    exit()

  # load KeePass db
  kp = PyKeePass(os.environ['HOME']+'/marx.kdbx', password)


  # define regex: ${VAR_NAME}
  pattern = re.compile('.*?\${(\w+)}.*?')
  # set envs
  for line in f:
    # find in line
    match = pattern.findall(line)
    for g in match:
        # lookup password
        try:
          entry = kp.find_entries(title=g, first=True)
          print ('Setting: ', g)
          os.environ[g] = entry.password
        except Exception as error:
          print('problem with placeholder ', g, error)
          exit()
  f.close()

  print('templating')
  myinput = open('./tmpl/cluster-secrets.yaml')
  myoutput = open('./cluster/config/cluster-secrets.yaml', 'w')
  subprocess.run(["envsubst"], stdin=myinput, stdout=myoutput)
  myinput.close()
  myoutput.close()

  print('encoding')
  subprocess.run(["sops","--encrypt","--in-place", "./cluster/config/cluster-secrets.yaml"])

  print('finished succesfully')

if __name__ == "__main__":
   main(sys.argv[1:])
