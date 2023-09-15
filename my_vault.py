import os
from typing import Dict, Union
import requests
import sys

#
# Get env from server
#
def get_variables_from_vault_server() -> Dict[str, str]:
    return requests.get('http://localhost:8000/env.json').json()

#
# Search through env replacing the appropriate items
#
def replace_environment(req: Dict[str, str]) -> None:
    for key, value in os.environ.items():
        if value.startswith('vault:'):
            vault_key = value.replace('vault:', '')
            if vault_key in req:
                print(f">  Setting env[{key}]={req[vault_key]}", file=sys.stderr)
                os.environ[key] = req[vault_key]

#
# Run our program
#
def resolve_fully_qualified_path_of_program(program_name: str) -> Union[str, None]:
    if not program_name.startswith("/"):
        #
        # Search the path for a relevant executable
        #
        for directory in os.environ.get("PATH","").split(":"):
            possible_program = f"{directory}/{program_name}"
            if os.path.exists(possible_program):
                return possible_program
        


if __name__ == '__main__':

    variables = get_variables_from_vault_server()
    replace_environment(variables)
    program_name = sys.argv[1]
    program = resolve_fully_qualified_path_of_program(program_name)
    if not program:
        print(f"Couldn't resolve executable for {program_name}", file=sys.stderr)
        sys.exit()
        
    print(">  Going to run '{program_name}' with the new env", file=sys.stderr)

    # Execute the program, ie replace this program with the one specified
    os.execl(program, program_name) # Kind of more obvious now we are in bash
    print("You will never get here", file=sys.stderr)
