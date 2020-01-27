import requests
import time
import config

def get_headers(api_token):
	return {'Content-Type': 'application/json',
			'User-Agent': 'Request-Promise',
			'Authorization': 'token {0}'.format(config.api_token)}

def request(endpoint_url, verb='get'):
	if verb == 'get':
		time.sleep(config.get_req_delay)
	if verb == 'delete': 
		time.sleep(config.del_req_delay)
    
	headers = get_headers(config.api_token)
	response = requests.request(verb, endpoint_url, headers=headers)

	if response.status_code >=200 and response.status_code <300:
		return response

	print('API ERROR: ' + str(response.status_code))
	raise SystemError('Could not connect to API. Status code: ' + response.status_code)
