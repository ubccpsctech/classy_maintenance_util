
from configparser import ConfigParser
from util import helper
from network.request import request
from api import github_enterprise
import time
import config
import json

STOP = 99999999

num_repos_found = 0
num_repos_removed = 0
num_repos_ignored = 0
num_teams = 0

# def get_team_members(team_id): 
# 	print('GithubUtilities:: get_team_members() - start')
# 	endpoint_url = '{0}/teams/{1}/members'.format(api_path, team_id)
# 	team_members = request(endpoint_url).json()
# 	return team_members

def get_all_team_repos(teams):
	all_repos_per_team = {}
	for team in teams: 
		team_name = team['name']
		team_id = team['id']
		all_repos_per_team[team_name] = github_enterprise.get_team_repos(team_name, team_id, [])
	return all_repos_per_team

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
				endpoint_url_test = '{0}/teams/{1}/repos/{2}/{3}'.format(config.api_path, team_id, repo_in_team['owner']['login'], repo_in_team['name']) #delete method
				print('DEBUG ' + endpoint_url_test)
				response = request(endpoint_url_test, 'delete')
				if response.status_code == 204: 
					print('GithubUtilities:: Removed ' + repo_in_team['name'] + ' from ' + team_name)
					repos_removed+=1 
					print('GithubUtilities:: Finished removing ' + str(repos_removed) + ' repo (' + repo_in_team['name'] + ') from team ' + team_name)
			num_repos_removed+=repos_removed

	return num_repos_removed

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

print('GithubUtilities:: get_org_teams() - start')
teams = github_enterprise.get_org_teams()
num_teams = len(teams)

print('GithubUtilities:: get_all_repos_per_team - start')
all_repos_per_team = get_all_team_repos(teams)

print('GithubUtilities:: net_num_repos_per_team - start')
num_repos_found = net_num_repos_per_team(all_repos_per_team)

## Remove the teams to ignore (ie. staff, admin) from dictionary so they do not become modified
print('GithubUtilities:: get_team_id_from_team_name - start')
ignored_team_ids = get_team_id_from_team_name(teams, config.ignored_team_names)

## Remove ignored teams from all_repo_per_team removal list and get count of filtered repos
num_repos_ignored = filter_ignored_teams(config.ignored_team_names, all_repos_per_team)

## Add users from ignore teams to ignore user list 
# add_team_users_to_ignore_list(ignored_team_names)

print('\n*********OPERATION ANALYTICS*********\n')
print('Github Organization: ' + config.github_org)
print('')
print('Number of Teams: ' + str(num_teams))
print('Ignored Teams: ' + json.dumps(config.ignored_team_names))
print('')
print('Number of Repos on Teams: ' + str(num_repos_found))
print('Number of Repos Ignored: ' + str(num_repos_ignored))
print('Number of Repos to be Removed: ' + str(num_repos_found - num_repos_ignored))
print('')
print('This operation will remove all repos from teams while ignoring the removal of repos on the ignored teams list.')
print('')

answer = helper.prompt_question('Do you want to proceed? y/n: ')
if answer == False:
	print('Exiting...')
	exit()

num_repos_removed = remove_all_repos_from_teams(teams, all_repos_per_team)
print('')
print('GithubUtilities:: Number of repos removed from team access: ' + str(num_repos_removed))

print('\n*********OPERATION EXPECTATIONS*********\n')
print('Number of Teams: ' + str(num_teams))
print('Ignored Teams: ' + json.dumps(config.ignored_team_names))
print('')
print('Number of Repos on Teams: ' + str(num_repos_found))
print('Number of Repos Ignored: ' + str(num_repos_ignored))
print('Number of Repos to be Removed: ' + str(num_repos_found - num_repos_ignored))
print('\n*********OPERATION RESULTS*********\n')
print('Number of Repos Removed: ' + str(num_repos_removed))
print('')
print('Operation Complete. Exiting...')
exit()