from configparser import ConfigParser
from util import helper

config = ConfigParser()
config.read('config.ini')

API_TOKEN = 'api_token'
API_PATH = 'api_path'
GITHUB_ORG = 'github_org'
IGNORED_TEAM_NAMES = 'ignored_team_names'
STAFF_LDAP = 'staff_ldap'
STUDENTS_LDAP = 'students_ldap'

API_TOKEN_PROMPT = 'Enter an API key with access to the organization and owner permissions: '
API_PATH_PROMPT = 'What is the API path (ie. https://github-dev.students.cs.ubc.ca/api/v3)? '
COURSE_PROMPT = 'What is your course number (ie. 436v)? '
GITHUB_ORG_PROMPT = 'What Github organization would you like to work on? '
IGNORED_TEAM_NAMES_PROMPT = 'What teams would you like to ignore? Please enter comma seperated teams (ie. staff, admin, students, etc.) '
STAFF_LDAP_PROMPT = 'What is the "staff" team LDAP DN? '
STUDENTS_LDAP_PROMPT = 'What is the "students" team LDAP DN? '

def set_value(value, prompt):
    if value in config[course] and config[course][value] != '':
        return config[course][value]
    return helper.get_input(prompt).strip()

try: 
    course = helper.get_input(COURSE_PROMPT)
    github_org = set_value(GITHUB_ORG, GITHUB_ORG_PROMPT)
    api_token = set_value(API_TOKEN, API_TOKEN_PROMPT)
    api_path = set_value(API_PATH, API_PATH_PROMPT)
    ignored_team_names = set_value(IGNORED_TEAM_NAMES, IGNORED_TEAM_NAMES_PROMPT).split(',')
    staff_ldap = set_value(STAFF_LDAP, STAFF_LDAP_PROMPT)
    students_ldap = set_value(STUDENTS_LDAP, STUDENTS_LDAP_PROMPT)
except KeyError: 
    print('Config.py:: ERROR - Configuration values missing. Exiting...')
    exit()

