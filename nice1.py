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

lol = ["  " + s + ":" for s in listmodules]

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
        flag == 1
        composefile.append("  "+ module + ":\n")
        res = dict()
        res[module] = arguments
        m = ModuleArgsParser(res)
        mod, args, to = m.parse()
        for x in args:
            if args[x].find('{{') != -1:
                composefile.append("    "+ x + ": " + '"' + args[x] + '"' + "\n")
                #print args[x]
            else:
               composefile.append("    "+ x + ": " + args[x] + "\n")

    if flag == 1: #or x.startswith('#') or x.startswith('-'):
        flag == 0
        composefile.append(x)

  f.close()
  print composefile
'''
  with open(yml, 'w') as f:
      for item in composefile:
          f.write("%s" % item)
  f.close()
'''