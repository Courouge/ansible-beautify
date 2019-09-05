#!/usr/bin/python

# coding: utf-8
import os
import argparse

from cStringIO import StringIO
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser
from fnmatch import fnmatch

from flask import Flask, jsonify, request, abort

app = Flask(__name__)
tasks =[]
def cleanAnsible(x):
  f = StringIO(x)
  ymlfiles=[]

  ## load all modules name in list ##
  listmodules = [line.rstrip('\n') for line in open("modules.txt")]

  ### open all *.yml ###
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
  return composefile



### list ansible modules ###
f = open("modules.txt", "r")
listmodules=[]
for x in f:
  listmodules.append(x[:-1])
f.close()

### get arg cmd form call ###
#parser = argparse.ArgumentParser()
#parser.add_argument("input", help="ansible text to clean")
#args = parser.parse_args()
#print cleanAnsible(args.input)


@app.route('/api', methods=['POST'])
def post_request():
    data = request.get_json()
    print(data)
    print('Hello world!')

    return "ok"

if __name__ == '__main__':
    app.run(debug=True)

