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

def request(endpoint_url):
	headers = get_headers(api_token)
	response = requests.get(endpoint_url, headers)
	if response.status_code >=200 and response.status_code <300:
		print(response.content)
		data = json.loads(response.content)
		return data
	else: 
		print(response.status_code)
		raise SystemError('Could not connect to API. Status code: ' + response.status_code)
	return data

def get_organization_teams():
	endpoint_url = '{0}/orgs/{1}/teams'.format(api_path, github_org)
	print(endpoint_url)
	headers = get_headers(api_token)
	response = requests.get(endpoint_url, headers=headers)
	teamNames = []
	if response.status_code >=200 and response.status_code <300:
		print(response.content)
		teams = json.loads(response.content)
		for team in teams:
			teamNames.append(team['name'])
	else:
		print(response.status_code)
	return teamNames

def get_all_repos_per_team(teams):
	allReposPerTeam = []
	for team in teams: 
		endpoint_url = '{0}/organizations/{1}/team/{2}/repos/orgs/teams'.format(team.api_path, team.github_org, team.team_id)
		reposPerTeam = request(endpoint_url)
	allReposPerTeam.append(reposPerTeam)

def remove_repos_from_team(team, repos): 
	for repos in team.repos:
		team_id = team.id
		repo = 

		data = request(endpoint_url)
		print(data)

course = get_input('What is your course number (ie. 436v)? ')
github_org = set_github_org()
api_token = set_api_token()
api_path = set_api_path()
print(api_token)
print(github_org)
print(api_path)
print(get_organization_teams())
teams = get_organization_teams()
allReposPerTeam = get_all_repos_per_team(teams)
removeAllReposPerTeam = remove_all_repos_per_team(allReposPerTeam)
# repos = get_organization_repos()


# def delete_organization_repos(org_name, repoNames):
# 	for repoName in repoNames:
# 		endpoint_url = url_base + '/repos/{0}/{1}'.format(org_name, repoName)
# 		print(endpoint_url)
# 		response = requests.delete(endpoint_url, headers=headers)
# 		if response.status_code >=200 and response.status_code <300:
# 			print('successfully deleted ' + repoName)
# 		else:
# 			print('could not delete ' + repoName + ' - status code: ' + str(response.status_code))

# repoNames = get_organization_repos(ORG_NAME)
# delete_organization_repos(ORG_NAME, repoNames)
# print('done deleting repos')