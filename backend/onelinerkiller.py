#!/usr/bin/python

# coding: utf-8
import os
import argparse

from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser
from fnmatch import fnmatch

### list ansible modules ###
f = open(os.getcwd() + "/" + "modules.txt", "r")
listmodules=[]
for x in f:
  listmodules.append(x[:-1])
f.close()


### get *.yml form role directory ###
ymlfiles=[]
parser = argparse.ArgumentParser()
parser.add_argument("path", help="Clean Ansible OneLiner in given path")
args = parser.parse_args()
# dir = os.getcwd() + "/roles"
dir = args.path
pattern = "*.yml"

## load all modules name in list ##
listmodules = [line.rstrip('\n') for line in open("modules.txt")]

for path, subdirs, files in os.walk(dir):
    for name in files:
        if fnmatch(name, pattern):
            ymlfiles.append(os.path.join(path, name))

### open all *.yml ###
for yml in ymlfiles:
  f = open(yml, "r")
  composefile = []
  flag = 0
  for x in f:
    for e in listmodules:
      if x.startswith("  " + e + ":") == True and len(x.strip()) > len(e + ":"):
        module = x.split(':',1 )[0].strip()
        arguments = x.split(':',1 )[1]
        composefile.append("  "+ module + ":\n")
        res = dict()
        flag = 1
        res[module] = arguments
        m = ModuleArgsParser(res)
        mod, args, to = m.parse()
        for x in args:
            if x == "_raw_params" :
                del composefile[-1]
                composefile.append("  " + module + ": " + args[x] + "\n")
            else:
                if args[x].find('{{') != -1 and args[x].find('}}') != -1 :
                    composefile.append("    "+ x + ": " + '"' + args[x] + '"' + "\n")
                else:
                    composefile.append("    "+ x + ": " + args[x] + "\n")
        break
    composefile.append(x)
    if flag == 1:
        flag = 0
        composefile.pop(len(composefile)-1)
  f.close()
  with open(yml, 'w') as f:
      for item in composefile:
          f.write("%s" % item)
  f.close()
print("done")