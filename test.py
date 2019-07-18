#!/usr/bin/python

# coding: utf-8


from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser

x="""dest="/etc/trololo" state=present regexp="{{ trololo }}.{{ trololo }}" insertafter="trololo" line="trolp olo" """

print(x)

m = ModuleArgsParser(dict(lineinfile=x ))
mod, args, to = m.parse()

for x in args:
    print(x + ": " + args[x])
