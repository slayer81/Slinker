#!/usr/local/bin/python3.11
import pathlib
import os
import sys
import subprocess
import humanize as hm
import datetime as dt
from collections import Counter
from prettytable import PrettyTable

#############################################################################################################
# Global variables
#############################################################################################################
SCRIPT_NAME = os.path.basename(__file__)
START_TIME = dt.datetime.now()
TORBASE = os.getenv('TORBASE')
LOCATIONS_FILE = os.path.join(TORBASE, 'Folder_Locations_v4.csv')
SYMLINK_BASE = os.path.join(TORBASE, 'zzzNew/')
# MARKER_CHAR = '#'
SPACER = '   '


SEARCH_PARAM_TROW_DIVIDER = f'+{"-" * 15}+{"-" * 62}+'
SYMLINK_TROW_DIVIDER = f'+{"-" * 79}+{"-" * 14}+'
#############################################################################################################
# End Globals
#############################################################################################################


#############################################################################################################
def item_search(string):
    results_list = []
    grep_cmd = f'grep -i "{string}" {LOCATIONS_FILE} | cut -d$\'\t\' -f2'
    try:
        grep_result = subprocess.run(
            grep_cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).stdout.decode('utf-8').split('\n')
    except subprocess.CalledProcessError as e:  # Handle the error if grep returns a non-zero exit status
        if e.returncode == 1: # No matches found
            return 0
        else:  # Other errors (e.g., file not found, permission denied, etc.)
            return str(e.stderr.decode('utf-8'))

    # Search returned a non-error value, so proceeding
    if not grep_result:  # Nothing found
        return 0
    else:  # Found item in index
        for result in grep_result:
            r = result.strip()
            if not r:  # After stripping leading and trailing whitespace, there was nothing left
                continue
            else:
                results_list.append(r)
    if not results_list:
        return 0
    else:
        # print(f'Function "item_search" returns a data_type of: {type(results_list)}')
        # print(f'Function "item_search" returns item count of: {len(results_list)}\n\n')
        return results_list
#############################################################################################################


#############################################################################################################
def create_symlink(item_path):
    symlink_cmd = f'ln -s "{item_path}" {SYMLINK_BASE}'
    try:
        subprocess.run(
            symlink_cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).stdout.decode('utf-8')
        return 1
    except subprocess.CalledProcessError as e:
        return str(e)
#############################################################################################################


#############################################################################################################
def main():
    print(f'\n{"#" * 100}')
    print(f'Starting execution of {SCRIPT_NAME}\n')

    if not len(sys.argv) >= 2:
        print(f'Execution requires search parameter, but none detected. Try again.....')
        print('{:<70} {:>20}'.format('Total runtime:', hm.precisedelta(dt.datetime.now() - START_TIME)))
        print(f'{"#" * 100}\n\n')
        quit(0)

    # Search Index for each passed parameter
    print(f'+{"-" * 78}+')
    print(f'| {"Search Parameters":^76} |')
    print(SEARCH_PARAM_TROW_DIVIDER)
    print('| {:>13} | {:^60} |'.format("Index:", os.path.basename(LOCATIONS_FILE)))
    print('| {:>13} | {:^60} |'.format("Item Count:", param_count))
    print(f'+{"-" * 15}+{"-" * 62}+')

    for item in sys.argv[1:]:
        print('Search parameters:')
        print(f'   Index:\t {LOCATIONS_FILE}')
        print(f'  String:\t {item}')
        item_lookup = item_search(item)
        if isinstance(item_lookup, list):
            print(f'  Result:\t SUCCESS!!   Results count:\t {len(item_lookup)}')
            print(f'\nCreating symlinks for each result:')
            for item in item_lookup:
                v = item.split(',')[1]
                val = pathlib.PurePosixPath(v).name
                print(f'{SPACER}   Name:\t "{val}"')
                symlink_result = create_symlink(v)
                if isinstance(symlink_result, int):
                    print(f'{SPACER} Result:\t SUCCESS!')
                else:
                    print(f'{SPACER}          \t {MARKER}')
                    print(f'{SPACER}   Result:\t __FAILED__')
                    print(f'{SPACER} Response:\t {symlink_result}')
                    print(f'{SPACER}          \t {MARKER}')
        if isinstance(item_lookup, int):
            print(f'Results for:\t "{item}" .... NOT FOUND!')
        if isinstance(item_lookup, str):
            print(f'\t\t Error encountered searching index. Result:\t __FAILED__')
            print(f'\t Response:\t {item_lookup}')

    print(f'\nExecution complete. Total runtime:\t\t {humanize.precisedelta(datetime.now() - START_TIME)}')
    print(f'{MARKER}{MARKER}\n\n')
#############################################################################################################


#############################################################################################################
def main2():
    print(f'\n{"#" * 100}')
    print(f'Starting execution of {SCRIPT_NAME}\n')

    if not len(sys.argv) >= 2:
        print(f'Execution requires search parameter, but none detected. Try again.....')
        print('{:<70} {:>20}'.format('Total runtime:', hm.precisedelta(dt.datetime.now() - START_TIME)))
        print(f'{"#" * 100}\n\n')
        quit(0)

    # Create de-duped list from passed parameters
    param_list = list(dict.fromkeys(sys.argv[1:]))
    param_count = len(param_list)

    # Search Index for each passed parameter
    print(f'+{"-" * 78}+')
    print(f'| {"Search Parameters":^76} |')
    print(SEARCH_PARAM_TROW_DIVIDER)
    print('| {:>13} | {:^60} |'.format("Index:", LOCATIONS_FILE))
    print('| {:>13} | {:^60} |'.format("Item Count:", param_count))
    print(f'+{"-" * 15}+{"-" * 62}+')

    param_dict = {}
    counter = 1
    for param in param_list:
        # print('| {:^16} | {:^57} |'.format("Result:", param_dict['string']))
        # print('| {:^16} | {:^57} |'.format(f'Item {counter}:', param_dict['string']))
        print('| {:>13} | {:^60} |'.format(f'Item {counter}:', param))
        result = item_search(param)
        if not result:
            print('| {:>13} | {:^60} |'.format("Result:", 'NOT FOUND!!!'))
        if not isinstance(result, list):
            param_dict[param] = {
                'type': 'list',
                'string': 'NOT FOUND!!!'
            }
        else:
            param_dict[param] = {
                'type': 'list',
                'string': 'SUCCESS!!!'
            }

        print(param_dict)
        print('\n\n| {:^12} | {:^61} |'.format("Search Result:", param_dict['string']))
        counter += 1

    print('{:<71} {:>20}'.format('Execution complete. Total runtime:', hm.precisedelta(dt.datetime.now() - START_TIME)))
    print(f'{"#" * 100}\n\n')
#############################################################################################################


if __name__ == "__main__":
    main()
