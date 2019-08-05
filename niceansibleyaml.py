#!/usr/bin/python

# coding: utf-8
import os
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser

### list ansible modules ###

f = open("modules.txt", "r")
listmodules=[]
for x in f:
  listmodules.append(x[:-1])
f.close()

### get *.yml form directory ###

from fnmatch import fnmatch

ymlfiles=[]
dir = os.getcwd() + "/roles"
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
    for x in f:


      for e in listmodules:
        if (e + ":") in x:
            v = x.split(':',1 )
            module = str(v[0]).strip()
            arguments = str(v[1])
            res = dict()
            res[module] = arguments

            m = ModuleArgsParser(res)
            mod, args, to = m.parse()
            print("  "+ module + ":")
            for x in args:
                print("    "+ x + ": " + args[x])

      else:
        print(x)