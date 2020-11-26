#!/usr/bin/env python

import commands

users = commands.getoutput("cut -d: -f 1 /etc/passwd").splitlines()

for user in users:
    if user != 'root' and 'LK' not in commands.getoutput('passwd -S %s' % user):
        print user
        commands.getoutput('passwd -l %s' % user)
