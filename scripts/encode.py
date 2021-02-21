#!/usr/bin/env python3
from pykeepass import PyKeePass
import getpass
import re
import subprocess
import argparse
import sys
from pathlib import Path

def main(argv):
  # read input filename
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", help="input file with placeholders")
  args=parser.parse_args()
  inputfile=args.i
  print("Reading from:", inputfile)

  # open source file
  f = open(inputfile,'r')
  # define output file name
  outputfile = Path(inputfile).stem + ".yaml"

  # ask for KeePass password
  try:
    password = getpass.getpass(prompt='Password: ', stream=None)
  except Exception as error:
    print('ERROR', error)
    exit()

  # load KeePass db
  kp = PyKeePass('marx.kdbx', password)

  # declare temporary file to save
  f2 = open('/tmp/somefile.txt', 'w')

  # define regex: ${VAR_NAME}
  pattern = re.compile('.*?\${(\w+)}.*?')
  # replace
  for line in f:
    # find in line
    match = pattern.findall(line)
    for g in match:
        # lookup password
        try:
          entry = kp.find_entries(title=g, first=True)
          line = line.replace(f'${{{g}}}', entry.password)
        except Exception as error:
          print('problem with placeholder ', g, error)
          exit()
    f2.write(line)
  f.close()
  f2.close()

  # seal (kubeseal <cloudflare-api-token-secret-org.yaml >cloudflare-api-token-secret.yaml --format yaml)
  print("Sealing to file:", outputfile)
  # open temporary file with real passwords
  myinput = open('/tmp/somefile.txt')
  myoutput = open(outputfile, 'w')
  subprocess.run(["kubeseal","-oyaml"], stdin=myinput, stdout=myoutput)
  myinput.close()
  myoutput.close()

if __name__ == "__main__":
   main(sys.argv[1:])