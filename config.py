from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

def get_input(text_prompt):
	return input(text_prompt)

def set_value(value, prompt):
    if value in config[course] and config[course][value] != '':
        return config[course][value]
    return get_input(prompt).strip()

def get_config_value(key):
	try:
		if 'course' in config['DEFAULT']:
			return config['DEFAULT'][key]
	except KeyError:
		print('Course {x} configuration was not found. Aborting... '.format(course))
		exit()

course = get_input('What is your course number (ie. 436v)? ')
github_org = set_value('github_org', 'What Github organization would you like to work on? ')
api_token = set_value('api_token', 'Enter an API key with access to the organization and owner permissions: ')
api_path = set_value('api_path', 'What is the API path (ie. https://github-dev.students.cs.ubc.ca/api/v3)? ')
ignored_team_names = set_value('ignored_team_names', 'What teams would you like to ignore? Please enter comma seperated teams (ie. staff, admin, students, etc.) ')
