import config
import json
import time
from api import github_enterprise
from configparser import ConfigParser
from network.request import request
from util import helper

def setup_github_org():
	print('UtilityOperations:: setup_github_org - start')

	confirm_org_creation()

	print('UtilityOperations:: Creating Github Organization - start ')
	github_enterprise.create_org(config.github_org, 'steca')

	ldap_teams = {
		"staff": 'cn={0},ou=Groups,ou=Github,dc=students,dc=cs,dc=ubc,dc=ca'.format(config.staff_ldap),
		"admin": '', ## should be blank, as no LDAP group exists for admins
		"students": 'cn={0},ou=Groups,ou=Github,dc=students,dc=cs,dc=ubc,dc=ca'.format(config.students_ldap)
	}

	team_ids = []

	print('UtilityOperations:: Creating Organization Teams (admin, staff, students) - start ')
	for ldap_team in ldap_teams.keys():
		team_id = github_enterprise.create_team(config.github_org, ldap_team, ldap_teams[ldap_team])
		team_ids += team_id

	payload = {
		"default_repository_permission": "none",
		"members_can_create_repositories": False
	}

	print('UtilityOperations:: Patching Github Organization member permissions (admin, staff, students) - start ')
	github_enterprise.patch_org(config.github_org, payload)
	show_org_creation_results()

def confirm_org_creation():
	print('\n*********GITHUB ORG CREATION*********\n')
	print('Github Organization: ' + config.github_org)
	print('')
	print('Admin Team: none' )
	print('Staff Team: ' + config.staff_ldap)
	print('Students Team: ' + config.students_ldap)
	print('')

	answer = helper.prompt_question('Do you want to proceed? y/n: ')
	if answer == False:
		print('Aborting...')
		exit()
	
def show_org_creation_results():
	print('\n*********GITHUB ORG CREATION*********\n')
	print(config.github_org + ' has been created. \n')
	print('NECESSARY MANUAL STEPS: ' )
	print(' - Deselect "Repository Invitations"')
	print(' - Deselect "Team Creation Rules"')


def remove_all_repos_from_teams():
	print('TeamRepo:: remove_all_repos_from_teams() - start')

	num_repos_found = 0
	num_repos_removed = 0
	num_repos_ignored = 0
	num_teams = 0

	print('TeamRepo:: remove_all_repos_from_teams() -- Getting Organization Teams')
	teams = github_enterprise.get_all_org_teams()
	num_teams = len(teams)

	print('TeamRepo:: remove_all_repos_from_teams() - Getting Repos on Teams')
	all_repos_per_team = {}
	for team in teams: 
		team_name = team['name']
		team_id = team['id']
		all_repos_per_team[team_name] = github_enterprise.get_all_repos_on_team(team_name, team_id, [])

	for teamKey in all_repos_per_team.keys(): 
		num_repos_found += len(all_repos_per_team[teamKey])

	print('TeamRepo:: remove_all_repos_from_teams() - Setting Teams to Ignore')
	ignored_team_ids = get_team_id_from_team_name(teams, config.ignored_team_names)
	for ignored_team_name in config.ignored_team_names:
		num_repos_on_team = len(all_repos_per_team[ignored_team_name])
		num_repos_ignored += num_repos_on_team
		del all_repos_per_team[ignored_team_name]

	confirm_team_removal(num_teams, num_repos_found, num_repos_ignored)

	print('TeamRepo:: remove_all_repos_from_teams() - Starting Removal of Repos on Teams')
	num_repos_removed = 0

	for team in teams: 
		team_name = team['name']
		team_id = team['id']

		if team_name in all_repos_per_team:
			repos_removed = 0

			for repo_in_team in all_repos_per_team[team_name]:
				success = github_enterprise.remove_repo_from_team(team_id, repo_in_team['owner']['login'], repo_in_team['name'], team_name)
				if success == True: 
					repos_removed+=1 

			num_repos_removed+=repos_removed
	
	print('Procedure:: remove_all_repos_from_teams() - FINISHED')
	show_removal_results(num_teams, num_repos_found, num_repos_ignored, num_repos_removed)

def get_team_id_from_team_name(teams, team_names):
	team_ids = {}
	for team in teams: 
		for team_name in team_names:
			if team['name'] == team_name:
				team_ids[team_name] = team['id']
	return team_ids

def confirm_team_removal(num_teams, num_repos_found, num_repos_ignored): 
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
		print('Aborting...')
		exit()

def show_removal_results(num_teams, num_repos_found, num_repos_ignored, num_repos_removed): 
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
