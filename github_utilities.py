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
	set_github_org().strip()
	set_api_token().strip()

def set_github_org(): 
	if 'github_org' in config[course]:
		return config[course]['github_org']
	set_org_prompt = 'What Github organization would you like to work on? '
	return get_input(set_org_prompt).strip()

def set_api_token():
	if 'api_token' in config[course] and config[course]['api_token'] != '':
		return config[course]['api_token']
	set_api_prompt = 'Enter an API key with access to the organization and owner permissions: '
	return get_input(set_api_prompt).strip()

def set_api_path(): 
	if 'api_path' in config[course]:
		return config[course]['api_path']
	set_org_prompt = 'What is the API path (ie. https://github-dev.students.cs.ubc.ca/api/v3)? '
	return get_input(set_org_prompt).strip()

def request(endpoint_url, verb='get'):
	headers = get_headers(api_token)
	response = requests.request(verb, endpoint_url, headers=headers)
	if response.status_code >=200 and response.status_code <300:
		return response
	else: 
		print('API ERROR: ' + str(response.status_code))
		raise SystemError('Could not connect to API. Status code: ' + response.status_code)

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

def remove_repos_from_team(team_id, owner, repo_name):
	print('GithubUtilities:: remove_repos_from_team() - start')
	# endpoint_url = '{0}/teams/{1}/repos/{2}/{3}'.format(api_path, team_id, owner, repo_name) #delete method
	# print(endpoint_url)


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
print(api_token)
print(github_org)
print(api_path)
teams = get_org_teams()
all_repos_per_team = get_all_repos_per_team(teams)
remove_all_repos_from_teams(all_repos_per_team)
# print(all_repos_per_team)