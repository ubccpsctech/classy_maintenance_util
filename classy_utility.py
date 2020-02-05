# This is a Classy helper utility. It helps automate particular Classy maintenance operations.

import json
import time
import re
from configparser import ConfigParser
from config import course, github_org, api_token, api_path, ignored_team_names
from pprint import pprint
from util import helper
from business import utility_operations

INVALID_SELECTION = '\n**Invalid selection**'

def invalid_selection():
	print(INVALID_SELECTION)
	main_menu()

def main_menu():
	print('\n*********CLASSY UTILITY*********\n')
	print('This utility integrates with Github.com and Github Enterprise to perform basic')
	print('Github operations that are necessary for the administration of Classy courses.')
	print('')
	print('Configured Github Organization: ' + github_org + '\n')
	print('Main Menu: \n')
	print('1. Display current configuration.')
	print('2. Remove all repositories from teams.')
	print('3. Creating testing organization.')
	print('4. Create new Github organization.')

	text_input = helper.get_input('\nChoose an option: ')
	selection = 99999999999
	
	try:
		selection = int(re.findall('\d+', text_input)[0])
	except IndexError: 
		invalid_selection()

	print(selection)
	if selection == 1:
		show_configuration()
	elif selection == 2:
		utility_operations.remove_all_repos_from_teams()
	elif selection == 4:
		utility_operations.setup_github_org()
	else:
		invalid_selection()

def show_configuration(): 
	print('\n*********CURRENT CONFIGURATION*********\n')
	print('Github Organization: ' + github_org)
	print('API Token: ' + api_token)
	print('API Path: ' + api_path)
	print('Ignored Team Names ' + ignored_team_names)

main_menu()