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
#dir = "/home/courouge/workspace/cagip/awx-fco/ansible-fd-kafka/roles"
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
  for x in f:
    if x.startswith('#', 0) == False:
      '''
      for e in listmodules:
        if x.startswith("  " + e + ": ") == True:
      '''
      if (x.startswith("  " + e + ": ")  for e in listmodules) == True:
      '''
          module = x.split(':',1 )[0].strip()
          arguments = x.split(':',1 )[1]
          res = dict()
          res[module] = arguments
          m = ModuleArgsParser(res)
          mod, args, to = m.parse()
          composefile.append("  "+ module + ":\n")
          for x in args:
              if args[x].find('{{') != -1:
                  composefile.append("    "+ x + ": " + '"' + args[x] + '"' + "\n")
                  #print args[x]
              else:
                  composefile.append("    "+ x + ": " + args[x] + "\n")
        else:
          composefile.append(x)
    else:
      composefile.append(x)

  print composefile

    with open(yml, 'w') as f:
        for item in composefile:
            f.write("%s" % item)
    f.close()
