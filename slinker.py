#!/usr/local/bin/python3.11
import pathlib
import os
import sys
import subprocess
import humanize
from datetime import datetime

####################################################################################
# Global variables
####################################################################################
START_TIME = datetime.now()
TORBASE = os.getenv('TORBASE')
LOCATIONS_FILE = os.path.join(TORBASE, 'Folder_Locations_v4.csv')
SYMLINK_BASE = os.path.join(TORBASE, 'zzzNew/')
MARKER_CHAR = '#'
SPACER = '   '
####################################################################################
# End Globals
####################################################################################


####################################################################################
def item_search(item):
    results_list = []
    grep_cmd = f'grep -i "{item}" {LOCATIONS_FILE} | cut -d$\'\t\' -f2'
    try:
        grep_result = subprocess.run(
            grep_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stdout.decode('utf-8').split('\n')
    except subprocess.CalledProcessError as e:
        # Handle the error if grep returns a non-zero exit status
        if e.returncode == 1:
            # No matches found
            return 0
        else:
            # Other errors (e.g., file not found, permission denied, etc.)
            return str(e.stderr.decode('utf-8'))

    # Search for item returned a non error value, so proceeding
    if not grep_result:
        # Nothing found
        return 0
    else:
        # Found item in index
        for result in grep_result:
            r = result.strip()
            if not r:
                # After stripping leading and trailing whitespace, there was nothing left
                continue
            else:
                results_list.append(r)

    if not results_list:
        return 0
    else:
        return results_list
####################################################################################


####################################################################################
def create_symlink(item_path):
    symlink_cmd = f'ln -s "{item_path}" {SYMLINK_BASE}'
    try:
        subprocess.run(
            symlink_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return str(e)

    return 1
####################################################################################


####################################################################################
def main():
    print(f'\n\n{MARKER_CHAR * 80}')
    if len(sys.argv) == 1:
        print(f'Execution requires search parameter. Not detected. Try again.....\n{SPACER} Exiting.....')
        print(f'{MARKER_CHAR * 80}\n\n')
        quit()

    for item in sys.argv[1:]:
        print('Search parameters:')
        print(f'   Index:\t {LOCATIONS_FILE}')
        print(f'  String:\t {item}')
        item_lookup = item_search(item)
        if isinstance(item_lookup, list):
            print(f'  Result:\t SUCCESS!!   Results count:\t {len(item_lookup)}')
            print(f'\nCreating symlinks for each result:')
            for i in item_lookup:
                v = i.split(',')[-1]
                val = pathlib.PurePosixPath(v).name
                print(f'{SPACER}   Name:\t "{val}"')
                symlink_result = create_symlink(v)
                if isinstance(symlink_result, int):
                    print(f'{SPACER} Result:\t SUCCESS!')
                else:
                    print(f'{SPACER}          \t {MARKER_CHAR * 40}')
                    print(f'{SPACER}   Result:\t __FAILED__')
                    print(f'{SPACER} Response:\t {symlink_result}')
                    print(f'{SPACER}          \t {MARKER_CHAR * 40}')
        if isinstance(item_lookup, int):
            print(f'Results for:\t "{item}" .... NOT FOUND!')
        if isinstance(item_lookup, str):
            print(f'\t\t Error encountered searching index. Result:\t __FAILED__')
            print(f'\t Response:\t {item_lookup}')

    print(f'\nExecution complete. Total runtime:\t\t {humanize.precisedelta(datetime.now() - START_TIME)}')
    print(f'{MARKER_CHAR * 80}\n\n')
####################################################################################


if __name__ == "__main__":
    main()
