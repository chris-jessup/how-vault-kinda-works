import os
import requests
import sys

# Get env from server
req = requests.get('http://localhost:8000/env.json').json()

# Search through env replacing the appropriate items
for key, value in os.environ.items():
    if value.startswith('vault:'):
        vault_key = value.replace('vault:', '')
        if vault_key in req:
            print(f">  Setting env[{key}]={req[vault_key]}", file=sys.stderr)
            os.environ[key] = req[vault_key]

# Run our program
prog = sys.argv[1]
print(">  Going to run '{prog}' with the new env", file=sys.stderr)

# Note we are not using PATH here so you need to point to the
# fully qualified path of the program eg '/bin/bash' rather
# than just 'bash'
os.execl(prog, prog) # Kind of more obvious now we are in bash
