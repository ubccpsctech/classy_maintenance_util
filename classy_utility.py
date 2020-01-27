# This is a Classy helper utility. It helps automate particular Classy maintenance operations.

import json
import time
import re
from configparser import ConfigParser
from config import course, github_org, api_token, api_path, ignored_team_names
from pprint import pprint
from util import helper
from business import team_repo

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
		team_repo.remove_all_repos_from_teams()
	else:
		invalid_selection()

def show_configuration(): 
	print('\nCurrent Configuration: ')
	print(github_org)

main_menu()