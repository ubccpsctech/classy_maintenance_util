from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

API_TOKEN = 'api_token'
API_PATH = 'api_path'
GITHUB_ORG = 'github_org'
IGNORED_TEAM_NAMES = 'ignored_team_names'

API_TOKEN_PROMPT = 'Enter an API key with access to the organization and owner permissions: '
API_PATH_PROMPT = 'What is the API path (ie. https://github-dev.students.cs.ubc.ca/api/v3)? '
COURSE_PROMPT = 'What is your course number (ie. 436v)? '
GITHUB_ORG_PROMPT = 'What Github organization would you like to work on? '
IGNORED_TEAM_NAMES_PROMPT = 'What teams would you like to ignore? Please enter comma seperated teams (ie. staff, admin, students, etc.) '

def get_input(text_prompt):
	return input(text_prompt)

def set_value(value, prompt):
    if value in config[course] and config[course][value] != '':
        return config[course][value]
    return get_input(prompt).strip()

try: 
    course = get_input(COURSE_PROMPT)
    github_org = set_value(GITHUB_ORG, GITHUB_ORG_PROMPT)
    api_token = set_value(API_TOKEN, API_TOKEN_PROMPT)
    api_path = set_value(API_PATH, API_PATH_PROMPT)
    ignored_team_names = set_value(IGNORED_TEAM_NAMES, IGNORED_TEAM_NAMES_PROMPT)
except KeyError: 
    print('Config.py:: ERROR - Configuration values missing. Exiting...')
    exit()

