import config
import json
from api import github_enterprise
from classy_utility import main_menu
from github.team import get_team_id_from_team_name

def remove_all_repos_from_teams_in_org():
	""" Removes every repository from Github teams in configured organization, except teams specified in ignored_team_names config."""

	num_repos_found = 0
	num_repos_removed = 0
	num_repos_ignored = 0
	num_teams = 0

	print('Procedures:: remove_all_repos_from_teams() - start')
	print('Procedures:: remove_all_repos_from_teams() -- Getting Organization Teams')
	teams = github_enterprise.get_all_org_teams()
	num_teams = len(teams)

	print('Procedures:: remove_all_repos_from_teams() - Getting Repos on Teams')
	all_repos_per_team = {}
	for team in teams: 
		team_name = team['name']
		team_id = team['id']
		all_repos_per_team[team_name] = github_enterprise.get_all_repos_on_team(team_name, team_id, [])

	for teamKey in all_repos_per_team.keys(): 
		num_repos_found += len(all_repos_per_team[teamKey])

	print('Procedures:: remove_all_repos_from_teams() - Setting Teams to Ignore')
	ignored_team_ids = team.get_team_id_from_team_name(teams, config.ignored_team_names)
	for ignored_team_name in config.ignored_team_names:
		num_repos_on_team = len(all_repos_per_team[ignored_team_name])
		num_repos_ignored += num_repos_on_team
		del all_repos_per_team[ignored_team_name]

	confirm_team_removal(num_teams, num_repos_found, num_repos_ignored)

	print('Procedures:: remove_all_repos_from_teams() - Starting Removal of Repos on Teams')
	num_repos_removed = remove_all_repos_from_teams(teams, all_repos_per_team)

	show_results(num_teams, num_repos_found, num_repos_ignored, num_repos_removed)

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
		classy_utility.main_menu()

def show_removal_results(num_teams, num_repos_found, num_repos_ignored, num_repos_removed, num_repos_removed): 
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