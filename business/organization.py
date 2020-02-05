import config
import json
import time
from api import github_enterprise
from configparser import ConfigParser
from network.request import request
from util import helper

def create_org():
	print('Organization:: create_org() - start')
	github_enterprise.create_org('cpsc999-2019w-t1', 'steca')
