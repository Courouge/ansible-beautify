#!/usr/bin/python

# coding: utf-8
import os

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

for path, subdirs, files in os.walk(dir):
    for name in files:
        if fnmatch(name, pattern):
            ymlfiles.append(os.path.join(path, name))

### open all *.yml ###


for yml in ymlfiles:
    f = open(yml, "r")
    for x in f:
      print(x)

