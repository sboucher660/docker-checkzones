#!/usr/bin/env python3

import os
import sys
import subprocess

badzones = []

for entry in os.scandir(sys.argv[1]):
	zonename = None

	if not entry.is_file():
		continue

	if entry.name.endswith('.db'):
		zonename = entry.name.rstrip('.db')

	if entry.name.endswith('.rev'):
		zonename = entry.name.lstrip('db.')
		zonename = zonename.rstrip('.rev')
		zonename = zonename.split('.')
		zonename.reverse()
		zonename.append('in-addr.arpa')
		zonename = ".".join(zonename)

	if zonename == None:
		continue

	s = subprocess.run (['/usr/sbin/named-checkzone',zonename,sys.argv[1] + '/' + entry.name], check=False)
	returncode = s.returncode

	if returncode:
		badzones.append (zonename)

print ('\n' + str(len(badzones)) + ' zone files failed validation')

sys.exit (len(badzones))
