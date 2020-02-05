import config
import json
import time
from api import github_enterprise
from configparser import ConfigParser
from network.request import request
from util import helper

def enter_course_num():
	helper.get_input('\n What is your course number? (ie. "311v") ').lower()

def create_default_teams():
	print('Team:: create_team() - start')

	staff_ldap = helper.get_input('\n Enter LDAP dn for the staff group? (ie. "cpsc210_2019W2_TAs")')
	student_ldap = helper.get_input('\n Enter LDAP dn for the staff group? (ie. "cpsc330_2019W2")')

	ldap_teams = {
		"staff": 'cn={0},ou=Groups,ou=Github,dc=students,dc=cs,dc=ubc,dc=ca'.format(staff_ldap),
		"admin": '', ## should be blank, as no LDAP group exists for admins
		"students": 'cn={1},ou=Groups,ou=Github,dc=students,dc=cs,dc=ubc,dc=ca'.format(student_ldap)
	}

	team_ids = []

	for ldap_team in ldap_teams.keys():
		team_id = github_enterprise.create_team('cpsc999-2019w-t1', ldap_team, ldap_team)
		team_ids += team_id

	github_enterprise.patch_org('cpsc999-2019w-t1')

	print(team_ids)

