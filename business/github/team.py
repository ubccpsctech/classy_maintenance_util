
from configparser import ConfigParser
from util import helper
from network.request import request
from api import github_enterprise
import time
import config
import json

STOP = 99999999

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
