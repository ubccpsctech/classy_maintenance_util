
from configparser import ConfigParser
from util import helper
from network.request import request
from api import github_enterprise
import time
import config
import json

def get_team_id_from_team_name(teams, team_names):
	team_ids = {}
	for team in teams: 
		for team_name in team_names:
			if team['name'] == team_name:
				team_ids[team_name] = team['id']
	return team_ids
