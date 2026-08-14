#!/usr/bin/env python3
from pykeepass import PyKeePass
import getpass
import re
import subprocess
import sys
import os

def main(argv):
  f = open('./tmpl/cluster-secrets.yaml', 'r')
  template = f.read()
  f.close()

  try:
    password = getpass.getpass(prompt='Password: ', stream=None)
  except Exception as error:
    print('ERROR', error)
    exit(1)

  kp = PyKeePass(os.environ['HOME']+'/marx.kdbx', password)

  pattern = re.compile(r'\$\{(\w+)\}')
  placeholders = sorted(set(pattern.findall(template)))

  values = {}
  for g in placeholders:
    entry = next((e for e in kp.find_entries(title=g) if e.group.name != 'Recycle Bin'), None)
    if entry is None:
      print(f'ERROR: KeePass entry not found: {g}')
      exit(1)
    val = entry.password
    if val is None:
      print(f'ERROR: KeePass entry has no password: {g}')
      exit(1)
    if '\n' in val:
      print(f'ERROR: value for {g} is multiline ({val.count(chr(10))+1} lines) — must be a single line')
      exit(1)
    print(f'Setting:  {g} ({len(val)} chars)')
    values[g] = val

  print('templating')
  result = pattern.sub(lambda m: values[m.group(1)], template)

  # validate result is parseable YAML before writing
  try:
    import yaml
    yaml.safe_load(result)
  except yaml.YAMLError as e:
    print(f'ERROR: substituted file is not valid YAML: {e}')
    # show offending lines
    lines = result.splitlines()
    if hasattr(e, 'problem_mark') and e.problem_mark:
      ln = e.problem_mark.line
      for i in range(max(0, ln-2), min(len(lines), ln+3)):
        print(f'  {i+1:4d}: {lines[i][:120]}')
    exit(1)

  with open('./cluster/flux/vars/cluster-secrets.sops.yaml', 'w') as out:
    out.write(result)

  print('encoding')
  subprocess.run(["sops", "--encrypt", "--in-place", "./cluster/flux/vars/cluster-secrets.sops.yaml"], check=True)

  print('finished successfully')

if __name__ == "__main__":
  main(sys.argv[1:])
