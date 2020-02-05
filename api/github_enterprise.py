import config
from network.request import request

MAX_PAGE_SIZE = 30

def create_org(org_name, admin):
	endpoint_url = '{0}/admin/organizations'.format(config.api_path)
	payload = {
		"login": org_name,
		"profile_name": org_name,
		"admin": admin
	}
	request(endpoint_url, 'post', payload)

def patch_org(org_name):
	endpoint_url = '{0}/orgs/{1}'.format(config.api_path, org_name)
	payload = {
		"default_repository_permission": "none",
		"members_can_create_repositories": "false",
		"members_allowed_repository_creation_type": "none"
	}
	request(endpoint_url, 'patch', payload)

def create_team(org_name, team_name, ldap_dn=''):
	endpoint_url = '{0}/orgs/{1}/teams'.format(config.api_path, org_name)
	payload = {
		"name": team_name
	}
	if ldap_dn != '':
		payload['ldap_dn'] = ldap_dn
	return request(endpoint_url, 'post', payload)

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
