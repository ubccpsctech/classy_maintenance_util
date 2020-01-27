# This is a Classy helper utility. It helps automate particular Classy maintenance operations.

import json
import requests
from configparser import ConfigParser
from config import course, github_org, api_token, api_path, ignored_team_names
from pprint import pprint
import time

def main_menu():
	print('\n*********CLASSY UTILITY*********\n')
	print('This utility integrates with Github.com and Github Enterprise to perform basic')
	print('Github operations that are necessary for the administration of Classy courses.')
	print('')
	print('Configured Github Organization: ' + github_org + '\n')
	print('Main Menu: ')
	print('1. Remove all repositories from teams')

	selection = int(input('\nChoose an option: ').strip())

	if selection == "1":
		print('1 sec')
	elif selection == "2":
		print('Exiting...')
		exit()
	else:
		print('**Invalid selection**')
		main_menu()

main_menu()