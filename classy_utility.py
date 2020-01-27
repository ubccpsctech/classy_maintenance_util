# This is a Classy helper utility. It helps automate particular Classy maintenance operations.

import json
from configparser import ConfigParser
from util import helper
from config import course, github_org, api_token, api_path, ignored_team_names
from pprint import pprint
import time
import re

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
	print('1. Remove all repositories from teams.')

	text_input = helper.get_input('\nChoose an option: ')
	selection = ''
	
	try:
		selection = int(re.findall('\d+', text_input)[0])
	except IndexError: 
		invalid_selection()

	print(selection)
	if selection == 1:
		print('1 sec')
	elif selection == 2:
		print('Exiting...')
		exit()
	else:
		invalid_selection()

main_menu()