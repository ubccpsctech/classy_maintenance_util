# This is a Classy helper utility. It helps automate particular Classy maintenance operations.

import json
import requests
from configparser import ConfigParser
from pprint import pprint
import time

config = ConfigParser()
config.read('config.ini')

def get_config_value(key):
	try:
		if 'course' in config['DEFAULT']:
			return config['DEFAULT'][key]
	except KeyError:
		print('Course {x} configuration was not found. Aborting... '.format(course))
		exit()

def get_headers(api_token):
	return {'Content-Type': 'application/json',
			'User-Agent': 'Request-Promise',
			'Authorization': 'token {0}'.format(api_token)}

def get_input(text_prompt):
	return input(text_prompt)

def setup_util():
	set_github_org()
	set_api_token()
	set_api_path()
	

def set_github_org(): 
	if 'github_org' in config[course]:
		return config[course]['github_org']
	set_org_prompt = 'What Github organization would you like to work on? '
	return get_input(set_org_prompt).strip()

def set_api_token():
	if 'api_token' in config[course] and config[course]['api_token'] != '':
		return config[course]['api_token']
	set_api_token_prompt = 'Enter an API key with access to the organization and owner permissions: '
	return get_input(set_api_token_prompt).strip()

def set_api_path(): 
	if 'api_path' in config[course]:
		return config[course]['api_path']
	set_api_path_prompt = 'What is the API path (ie. https://github-dev.students.cs.ubc.ca/api/v3)? '
	return get_input(set_api_path_prompt).strip()

def set_ignored_team_names(): 
	if 'ignored_team_names' in config[course]:
		ignored_team_names = config[course]['ignored_team_names'].replace(' ', '').split(',')
		return ignored_team_names
	set_ignored_team_names_prompt = 'What teams would you like to ignore? Please enter comma seperated teams (ie. staff, admin, students, etc.) '
	return get_input(set_ignored_team_names_prompt).strip(' ').split(',')

def set_ignored_user_names(): 
	if 'ignored_user_names' in config[course]:
		ignored_user_names = config[course]['ignored_team_names'].replace(' ', '').split(',')
		return ignored_user_names
	set_ignored_user_names_prompt = 'What teams would you like to ignore? Please enter comma seperated teams (ie. staff, admin, students, etc.) '
	return get_input(set_ignored_user_names_prompt).strip(' ').split(',')


def request(endpoint_url, verb='get'):
	headers = get_headers(api_token)
	response = requests.request(verb, endpoint_url, headers=headers)
	if response.status_code >=200 and response.status_code <300:
		return response
	else: 
		print('API ERROR: ' + str(response.status_code))
		raise SystemError('Could not connect to API. Status code: ' + response.status_code)

def get_team_members(team_id): 
	print('debug' + ' team id ')
	print(team_id)
	print('GithubUtilities:: get_team_members() - start')
	endpoint_url = '{0}/teams/{1}/members'.format(api_path, team_id)
	team_members = request(endpoint_url).json()
	return team_members

def get_org_teams():
	print('GithubUtilities:: get_org_teams() - start')
	endpoint_url = '{0}/orgs/{1}/teams'.format(api_path, github_org)
	teams = request(endpoint_url).json()
	print('GithubUtilities:: get_org_teams() - ' + str(len(teams)) + ' teams found in ' + github_org)
	return teams

def get_all_repos_per_team(teams):
	print('GithubUtilities:: get_all_repos_per_team - start')
	all_repos_per_team = {}
	for team in teams: 
		team_name = team['name']
		team_id = team['id']
		endpoint_url = '{0}/teams/{1}/repos'.format(api_path, team_id)
		repos_per_team = request(endpoint_url).json()
		all_repos_per_team[team_name] = repos_per_team
		print('GithubUtilities:: get_all_repos_per_team() - ' + team_name + ':: ' + str(len(repos_per_team)) + ' repos found')
	return all_repos_per_team

def del_key_from_dict(dictionary, key): 
	print(key)
	print("GithubUtilities:: del_key_from_dict - key not found")
	try:
		del dictionary[key]
		print('GithubUtilities:: del_key_from_dict - key ' + key + ' removed')
	except KeyError:
		print("GithubUtilities:: del_key_from_dict - key not found")

def remove_repos_from_team(team_id, owner, repo_name):
	print('GithubUtilities:: remove_repos_from_team() - start')
	# endpoint_url = '{0}/teams/{1}/repos/{2}/{3}'.format(api_path, team_id, owner, repo_name) #delete method
	# print(endpoint_url)

def get_team_id_from_team_name(teams, team_names):
	team_ids = {}
	for team in teams: 
		for team_name in team_names:
			if team['name'] == team_name:
				team_ids[team_name] = team['id']
	return team_ids

def remove_all_repos_from_teams(all_repos_per_team):
	print('GithubUtilities:: remove_all_repos_from_teams() - start')
	total_repos_removed = 0
	for key in all_repos_per_team.keys():
		team_name = key
		repos_removed = 0
		for repo_in_team in all_repos_per_team[key]:
			team_id = repo_in_team['id']
			owner = repo_in_team['owner']['login']
			repo_name = repo_in_team['name']
			if ignored_user_names.index(repo_name):
				print('GithubUtilities:: Found ignored user. Skipping team removal for repo ' + repo_name)
			else: 
				endpoint_url_test = '{0}/teams/{1}/repos/{2}/{3}'.format(api_path, '2390', 'cpsc210-2019w-t1', 'test_repo') #delete method
				response = request(endpoint_url_test, 'delete')
				if response.status_code == 204: 
					# print('GithubUtilities:: Removed ' + repo_name + ' from ' + team_name)
					repos_removed+=1 
				print('GithubUtilities:: Finished removing ' + str(repos_removed) + ' from team ' + team_name)
		total_repos_removed+=repos_removed
	print('GithubUtilities:: Total Repos Removed from Teams: ' + str(total_repos_removed))

course = get_input('What is your course number (ie. 436v)? ')	
github_org = set_github_org()
api_token = set_api_token()
api_path = set_api_path()
ignored_team_names = set_ignored_team_names()
ignored_user_names = set_ignored_user_names()
print(api_token)
print(github_org)
print(api_path)
print(ignored_team_names)

teams = get_org_teams()
all_repos_per_team = get_all_repos_per_team(teams)

## Remove the teams to ignore (ie. staff, admin) from dictionary so they do not become modified
ignored_user_names = []
ignored_team_ids = get_team_id_from_team_name(teams, ignored_team_names)

for ignored_team_name in ignored_team_names: 
	team_id = all_repos_per_team[ignored_team_name]
	ignored_team_id = ignored_team_ids[ignored_team_name]

	ignored_team_members = get_team_members(ignored_team_id)
	print(ignored_team_name)
	print(ignored_team_members)
	# for team_member in team_members:
	# 	ignored_user_names.append(team_member.login)
	# del_key_from_dict(all_repos_per_team, ignored_team_id)

remove_all_repos_from_teams(all_repos_per_team)
# print(all_repos_per_team)