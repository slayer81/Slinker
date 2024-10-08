#!/usr/local/bin/python3.11
import pathlib
import os
import sys
import subprocess
import humanize
from datetime import datetime
from prettytable import PrettyTable

#############################################################################################################
# Global variables
#############################################################################################################
START_TIME = datetime.now()
TORBASE = os.getenv('TORBASE')
LOCATIONS_FILE = os.path.join(TORBASE, 'Folder_Locations_v4.csv')
SYMLINK_BASE = os.path.join(TORBASE, 'zzzNew/')
MARKER_CHAR = '#'
SPACER = '   '
#############################################################################################################
# End Globals
#############################################################################################################


#############################################################################################################
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
#############################################################################################################


#############################################################################################################
def create_symlink(item_path):
    symlink_cmd = f'ln -s "{item_path}" {SYMLINK_BASE}'
    try:
        subprocess.run(
            symlink_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return str(e)

    return 1
#############################################################################################################


#############################################################################################################
def main():
    print(f'\n\n{MARKER_CHAR * 100}')
    if len(sys.argv) == 1:
        print(f'Execution requires search parameter, but none detected. Try again.....')
        # print(f'Exiting..... Total runtime:\t\t {humanize.precisedelta(datetime.now() - START_TIME)}')
        print('{:<70} {:>20}'.format('Exiting..... Total runtime:', humanize.precisedelta(datetime.now() - START_TIME)))
        print(f'{MARKER_CHAR * 100}\n\n')
        quit(0)

    param_list = sys.argv[1:]
    param_dict = {}
    for item in sys.argv[1:]:
        result = item_search(item)
        if isinstance(result, list):
            param_dict[item] = {
                'type': 'list',
                'string': 'SUCCESS!!!'
            }
        elif isinstance(result, int):
            param_dict[item] = {
                'type': 'int',
                'string': 'NOT FOUND!!!'
            }
        else:
            param_dict[item] = {
                'type': 'string',
                'string': f'ERROR!!!\n{result}'
            }

    for item in param_list:
        param_table = PrettyTable()
        param_table.field_names = ['Search Parameters', '']
        param_table.add_row(['Index:', LOCATIONS_FILE])
        param_table.add_row(['Param count:', len(param_list)])
        param_table.add_row(['String:', item])
        item_lookup = item_search(item)
        if isinstance(item_lookup, list):
            param_table.add_row(['Result:', 'SUCCESS!!'])
            param_table.add_row(['Results count:', len(item_lookup)])
            print('{:^80} \t{:^15}'.format('Name          ', 'Result'))
            for i in item_lookup:
                result_table = PrettyTable()
                result_table.fieldnames = ['Name', 'Result']
                v = i.split(',')[-1]
                val = pathlib.PurePosixPath(v).name
                symlink_result = create_symlink(v)
                if isinstance(symlink_result, int):
                    result_table.add_row([val, 'SUCCESS!!'])
                else:
                    result_table.add_row([val, '__FAILED__'])
        if isinstance(item_lookup, int):
            param_table.add_row(['Result:', 'NOT FOUND!!!'])
        if isinstance(item_lookup, str):
            param_table.add_row(['Result:', 'ERROR!!!' + f'\n{item_lookup}'])
        print(param_table)
        print(f'\nCreating symlinks for each result:')
        result_table.align["Name"] = "l"
        print(result_table)
    print('{:<71} {:>20}'.format('Execution complete. Total runtime:', humanize.precisedelta(datetime.now() - START_TIME)))
    print(f'{MARKER_CHAR * 100}\n\n')
#############################################################################################################


if __name__ == "__main__":
    main()
