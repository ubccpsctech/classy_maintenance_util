from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

def get_input(text_prompt):
	return input(text_prompt)

def set_github_org(): 
	if 'github_org' in config[course] and config[course]['github_org'] != '':
		return config[course]['github_org']
	set_org_prompt = 'What Github organization would you like to work on? '
	return get_input(set_org_prompt).strip()

def set_api_token():
	if 'api_token' in config[course] and config[course]['api_token'] != '':
		return config[course]['api_token']
	set_api_token_prompt = 'Enter an API key with access to the organization and owner permissions: '
	return get_input(set_api_token_prompt).strip()

def set_api_path(): 
	if 'api_path' in config[course] and config[course]['api_path'] != '':
		return config[course]['api_path']
	set_api_path_prompt = 'What is the API path (ie. https://github-dev.students.cs.ubc.ca/api/v3)? '
	return get_input(set_api_path_prompt).strip()

def set_ignored_team_names(): 
	if 'ignored_team_names' in config[course] and config[course]['ignored_team_names'] != '':
		ignored_team_names = config[course]['ignored_team_names'].replace(' ', '').split(',')
		return ignored_team_names
	set_ignored_team_names_prompt = 'What teams would you like to ignore? Please enter comma seperated teams (ie. staff, admin, students, etc.) '
	return get_input(set_ignored_team_names_prompt).strip(' ').split(',')

def get_config_value(key):
	try:
		if 'course' in config['DEFAULT']:
			return config['DEFAULT'][key]
	except KeyError:
		print('Course {x} configuration was not found. Aborting... '.format(course))
		exit()

# def set_ignored_user_names(): 
# 	if 'ignored_user_names' in config[course]:
# 		ignored_user_names = config[course]['ignored_team_names'].replace(' ', '').split(',')
# 		return ignored_user_names
# 	set_ignored_user_names_prompt = 'What teams would you like to ignore? Please enter comma seperated teams (ie. staff, admin, students, etc.) '
# 	return get_input(set_ignored_user_names_prompt).strip(' ').split(',')

def setup_util():
	set_github_org()
	set_api_token()
	set_api_path()

course = get_input('What is your course number (ie. 436v)? ')
github_org = set_github_org()
api_token = set_api_token()
api_path = set_api_path()
ignored_team_names = set_ignored_team_names()
# ignored_user_names = set_ignored_user_names()
