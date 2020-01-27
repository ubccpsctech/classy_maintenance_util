import config
from network.request import request

MAX_PAGE_SIZE = 30

def get_all_org_teams(accData=[], page=1):
	endpoint_url = '{0}/orgs/{1}/teams?page={2}'.format(config.api_path, config.github_org, page)
	teams = request(endpoint_url).json()
	accData += teams

	if len(teams) < MAX_PAGE_SIZE: 
		print('GithubEnterprise:: get_all_org_teams() - ' + str(len(accData)) + ' teams found in ' + config.github_org)
		return accData

	print('GithubEnterprise:: get_all_org_teams() - ' + str(len(accData)) + ' teams found in ' + config.github_org)

	return get_all_org_teams(accData, page+1)

def get_all_repos_on_team(team_name, team_id, acc_data=[], page=1):	
	endpoint_url = '{0}/teams/{1}/repos?page={2}'.format(config.api_path, team_id, page)
	team_repos_page = request(endpoint_url).json()
	acc_data += team_repos_page

	print(endpoint_url)

	if len(team_repos_page) < MAX_PAGE_SIZE: 
		print('GithubEnterprise:: get_all_repos_on_team() - ' + str(len(acc_data)) + ' repos found in ' + team_name)
		return acc_data
	return get_all_repos_on_team(team_name, team_id, acc_data, page+1)

def remove_repo_from_team(team_id, owner, repo_name, team_name):
	endpoint_url_test = '{0}/teams/{1}/repos/{2}/{3}'.format(config.api_path, team_id, owner, repo_name) #delete method
	print('GithubEnterprise:: remove_repo_from_team() ' + endpoint_url_test)
	response = request(endpoint_url_test, 'delete')
	if response.status_code == 204: 
		print('GithubEnterprise:: remove_repo_from_team() - Removed ' + repo_name + ' from ' + team_name)
		return True
	return False
