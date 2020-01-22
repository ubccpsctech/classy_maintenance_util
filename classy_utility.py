# This is a Classy helper utility. It helps automate particular Classy maintenance operations.

import json
import requests
from configparser import ConfigParser
from pprint import pprint
import time

STOP = 99999999
MAX_PAGE_SIZE = 30

config = ConfigParser()
config.read('config.ini')
num_repos_found = 0
num_repos_removed = 0
num_repos_ignored = 0
num_teams = 0

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
	print('GithubUtilities:: get_team_members() - start')
	endpoint_url = '{0}/teams/{1}/members'.format(api_path, team_id)
	team_members = request(endpoint_url).json()
	return team_members

def get_org_teams(accTeamData=[], page=1):
	print('GithubUtilities:: get_org_teams() - start')
	endpoint_url = '{0}/orgs/{1}/teams?page={2}'.format(api_path, github_org, page)
	teams = request(endpoint_url).json()
	accTeamData += teams

	if len(teams) < MAX_PAGE_SIZE: 
		print('GithubUtilities:: get_org_teams() - ' + str(len(accTeamData)) + ' teams found in ' + github_org)
		return accTeamData
	else: 
		return get_org_teams(accTeamData, page+1)

def get_all_repos_per_team(teams):
	print('GithubUtilities:: get_all_repos_per_team - start')
	all_repos_per_team = {}
	for team in teams: 
		team_name = team['name']
		team_id = team['id']
		endpoint_url = '{0}/teams/{1}/repos'.format(api_path, team_id)
		repos_per_team = request(endpoint_url).json()
		all_repos_per_team[team_name] = repos_per_team
	return all_repos_per_team

def del_key_from_dict(dictionary, key): 
	print("GithubUtilities:: del_key_from_dict - key not found")
	try:
		del dictionary[key]
		print('GithubUtilities:: del_key_from_dict - key ' + key + ' removed')
	except KeyError:
		print("GithubUtilities:: del_key_from_dict - key not found")

def get_team_id_from_team_name(teams, team_names):
	team_ids = {}
	for team in teams: 
		for team_name in team_names:
			if team['name'] == team_name:
				team_ids[team_name] = team['id']
	return team_ids

def remove_all_repos_from_teams(teams, all_repos_per_team):
	print('GithubUtilities:: remove_all_repos_from_teams() - start')
	num_repos_removed = 0

	for team in teams: 
		team_name = team['name']
		team_id = team['id']

		if team_name in all_repos_per_team:
			repos_removed = 0
			for repo_in_team in all_repos_per_team[team_name]:
				owner = repo_in_team['owner']['login']
				repo_name = repo_in_team['name']
				endpoint_url_test = '{0}/teams/{1}/repos/{2}/{3}'.format(api_path, team_id, owner, repo_name) #delete method
				print('DEBUG ' + endpoint_url_test)
				response = request(endpoint_url_test, 'delete')
				if response.status_code == 204: 
					print('GithubUtilities:: Removed ' + repo_name + ' from ' + team_name)
					repos_removed+=1 
				print('GithubUtilities:: Finished removing ' + str(repos_removed) + ' repo (' + repo_name + ') from team ' + team_name)
			num_repos_removed+=repos_removed
	return num_repos_removed

	# for key in all_repos_per_team.keys():
	# 	team_name = key
	# 	repos_removed = 0
	# 	for repo_in_team in all_repos_per_team[key]:
	# 		team_id = repo_in_team['id']
	# 		owner = repo_in_team['owner']['login']
	# 		repo_name = repo_in_team['name']
	# 		endpoint_url_test = '{0}/teams/{1}/repos/{2}/{3}'.format(api_path, team_id, owner, repo_name) #delete method
	# 		print('DEBUG ' + endpoint_url_test)
	# 		response = request(endpoint_url_test, 'delete')
	# 		if response.status_code == 204: 
	# 			print('GithubUtilities:: Removed ' + repo_name + ' from ' + team_name)
	# 			repos_removed+=1 
	# 		print('GithubUtilities:: Finished removing ' + str(repos_removed) + ' repo (' + repo_name + ') from team ' + team_name)
	# 	num_repos_removed+=repos_removed
	# return num_repos_removed

def add_team_users_to_ignore_list(ignored_team_names):
	for ignored_team_name in ignored_team_names: 
		ignored_team_id = ignored_team_ids[ignored_team_name]
		team_members = get_team_members(ignored_team_id)
		for team_member in team_members:
			ignored_user_names.append(team_member['login'])

def filter_ignored_teams(ignored_team_names, all_repos_per_team):
	num_repos_ignored = 0
	for ignored_team_name in ignored_team_names:
		num_repos_on_team = len(all_repos_per_team[ignored_team_name])
		num_repos_ignored += num_repos_on_team
		del all_repos_per_team[ignored_team_name]
		print('GithubUtilities:: filter_ignored_teams() - Filtered ignored team ' + ignored_team_name + ', ' + str(num_repos_on_team) + ' ignored')
	return num_repos_ignored

def net_num_repos_per_team(all_repos_per_team):
	num_repos_found = 0
	for teamKey in all_repos_per_team.keys(): 
		num_repos_found += len(all_repos_per_team[teamKey])
		print('GithubUtilities:: net_num_repos_per_team() - ' + teamKey + ':: ' + str(len(all_repos_per_team[teamKey])) + ' repos found')
	return num_repos_found

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
num_teams = len(teams)
all_repos_per_team = get_all_repos_per_team(teams)

num_repos_found = net_num_repos_per_team(all_repos_per_team)

## Remove the teams to ignore (ie. staff, admin) from dictionary so they do not become modified
ignored_team_ids = get_team_id_from_team_name(teams, ignored_team_names)

## Remove ignored teams from all_repo_per_team removal list and get count of filtered repos
num_repos_ignored = filter_ignored_teams(ignored_team_names, all_repos_per_team)

## Add users from ignore teams to ignore user list 
add_team_users_to_ignore_list(ignored_team_names)

## Getting to ignore team member names
print('This operation will bypass the removal of repos from the following ignored teams: ' + json.dumps(ignored_team_names))
print('The following users are on ignored teams that this operation will bypass: ' + json.dumps(ignored_user_names))
print('Would you like to proceed with the operation? y/n: ')

num_repos_removed = remove_all_repos_from_teams(teams, all_repos_per_team)
print('GithubUtilities:: Number of repos removed from team access: ' + str(num_repos_removed))

print('')
print('Teams: ')
print('Number of teams found: ' + str(num_teams))
print('')
print('Repositories: ')
print('Number of repos found: ' + str(num_repos_found))
print('Number of repos ignored: ' + str(num_repos_ignored))
print('Number of repos removed: ' + str(num_repos_removed))


# print(all_repos_per_team)