#!/usr/bin/python

# coding: utf-8
import os
import sys
import argparse
import json
from flask_cors import CORS
from cStringIO import StringIO
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser
from fnmatch import fnmatch

from flask import Flask, jsonify, request, abort

app = Flask(__name__)
CORS(app)

def cleanAnsible(x):
  f = StringIO(x)
  ymlfiles=[]

  ## load all modules name in list ##
  listmodules = [line.rstrip('\n') for line in open("modules.txt")]

  ### open all *.yml ###
  composefile = []
  flag = 0
  try:
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
                    tmp = args[x].replace("\n", "\\n")
                    if tmp.find('{{') != -1 and tmp.find('}}') != -1 :
                        composefile.append("    "+ x + ": " + '"' + tmp + '"' + "\n")
                    else:
                        composefile.append("    "+ x + ": " + tmp + "\n")
            break
        composefile.append(x)
        if flag == 1:
            flag = 0
            composefile.pop(len(composefile)-1)

  except (AnsibleParserError):
      composefile = "Error Ansible Syntax"
  return composefile



### list ansible modules ###
f = open("modules.txt", "r")
listmodules=[]
for x in f:
  listmodules.append(x[:-1])
f.close()

@app.route('/api/', methods=['GET','POST'])
def api_post():
    data = request.json
    res = cleanAnsible((str(data['in'])))
    return '{ "out":' + json.dumps(''.join(res)) + '}'
if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
