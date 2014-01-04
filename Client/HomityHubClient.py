import requests
import json
import logging
"""
import httplib
httplib.HTTPConnection.debuglevel = 1

logging.basicConfig() 
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
"""
#logging.basicConfig(level=logging.DEBUG)


class HomityHubClientError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

class HomityHubClient:
	RESPONSE_CODES = {
		200: 'OK',
		201: 'Created',
		202: 'Accepted',
		304: 'Not Modified',
		400: 'Bad Request',
		401: 'Unauthorized',
		403: 'Forbidden',
		404: 'Not Found',
		500: 'Internal Server Error',
		501: 'Internal Server Error (not implemented)'
	}

	def __init__(self, hostname, username, password, use_ssl=True, verify_ssl=True, stateless=False, version=False):
		self.hostname = hostname
		self.protocol = "http"
		self.verify_ssl = verify_ssl
		self.username = username
		self.password = password
		self.stateless = stateless
		if version:
			self.version = "/v%s" % str(version)
		else:
			self.version = ""
		self.session = ""
		if use_ssl:
			self.protocol = "https"

		self.base_uri = "%s://%s%s" % (self.protocol, self.hostname, self.version)

	def send_get(self, location, params):
		if self.stateless:
			params.update({ 'username': self.username })
			params.update({ 'password': self.password })
		else:
			params.update({ 'session': self.session })
		url = "/".join([ self.base_uri, location ])
		headers = {'content-type': 'x-www-form-urlencoded'}

		r = requests.get(url, verify=self.verify_ssl, params=params)
		return self.decode_response(r)
	
	def send_delete(self, location, params):
		if self.stateless:
			params.update({ 'username': self.username })
			params.update({ 'password': self.password })
		else:
			params.update({ 'session': self.session })
		url = "/".join([ self.base_uri, location ])
		headers = {'content-type': 'x-www-form-urlencoded'}

		r = requests.delete(url, verify=self.verify_ssl, params=params)
		return self.decode_response(r)
	
	def send_put(self, location, params):
		if self.stateless:
			params.update({ 'username': self.username })
			params.update({ 'password': self.password })
		else:
			params.update({ 'session': self.session })
		url = "/".join([ self.base_uri, location ])
		headers = {'content-type': 'x-www-form-urlencoded'}

		r = requests.put(url, verify=self.verify_ssl, params=params)
		return self.decode_response(r)
	
	def send_post(self, location, params):
		if self.stateless:
			params.update({ 'username': self.username })
			params.update({ 'password': self.password })
		else:
			params.update({ 'session': self.session })
		url = "/".join([ self.base_uri, location ])
		headers = {'content-type': 'application/json'}
		
		r = requests.post(url, verify=self.verify_ssl, data=json.dumps(params), headers=headers)
		return self.decode_response(r)
	
	def decode_response(self, response):
		"""
		Handle the response object, and raise exceptions if errors are found.
		"""
		url = response.url
		if response.status_code not in (200, 201, 202, 304):
			http_status_code = response.status_code
			raise HomityHubClientError('Got HTTP response code %d - %s for %s, %s' % (http_status_code, self.RESPONSE_CODES.get(http_status_code, 'Unknown!'), url, response.text))

		try:
			json_data = json.loads(response.text)
			return json_data
		except:
			return ""

	def login(self, quick=False):
		if not self.stateless:
			location = "login"		
			url = "/".join([ self.base_uri, location ])
			headers = {'content-type': 'application/json'}
	
			response = requests.post(url, verify=self.verify_ssl, data=json.dumps({ 'username': self.username, 'password': self.password, 'quick': quick }), headers=headers)
			
			decoded_json_response = self.decode_response(response)
			self.session = decoded_json_response['session']
			
			return decoded_json_response

	def logout(self):
		if not self.stateless:
			location = "logout"
			decoded_json_response = self.send_post(location, params={ })
	
	def spoke_drivers(self):
		location = "spokedrivers"
		return self.send_get(location, params={ })
	
	def spoke(self, spoke_id=False, path=[], value=False):
		if spoke_id:
			path.insert(0,spoke_id)
		path.insert(0,"spoke")
		location = '/'.join(path)

		if value:
			decoded_json_response = self.send_put(location, params={"value":value})
		else:
			decoded_json_response = self.send_get(location, params={ })

		return decoded_json_response
	
	def spoke_create(self, name="", driver="", driver_info={}):
		location = "spoke"
		return self.send_post(location, params={"name":name, "driver":driver, "driver_info":driver_info})
	
	def spoke_delete(self, spoke_id=False, path=[]):
		if spoke_id:
			path.insert(0,spoke_id)
			path.insert(0,"spoke")
			location = '/'.join(path)
			return self.send_delete(location, params={ })
		'''
		if spoke_id:
			location = "spoke/%s" % (spoke_id)
			return self.send_delete(location, params={ })
		'''
	def pin_delete(self, pin_id=False, path=[]):
		if pin_id:
			path.insert(0,pin_id)
			path.insert(0,"pin")
			location = '/'.join(path)
			return self.send_delete(location, params={ })
		
	def pin_schedule(self, pin_id, new_entry={}, entry_index=False):
		if new_entry != {} and entry_index: #can't create & delete
			return False
		elif entry_index: #delete the entry
			return self.pin_delete(pin_id = pin_id,path=["schedule",entry_index])
		elif new_entry:
			if "minute" and "hour" and "days" and "action" in new_entry:
				new_entry_string = ':'.join([new_entry['minute'],new_entry['hour'],new_entry['days'],new_entry['action']])
				return self.pin(pin_id=pin_id, path=["schedule"], value=new_entry_string)
		return False
	
	def pin(self, pin_id=False, path=[], value=False):
		if pin_id:
			path.insert(0,pin_id)
		path.insert(0,"pin")
		location = '/'.join(path)
		
		if value:
			decoded_json_response = self.send_put(location, params={"value":value})
		else:
			decoded_json_response = self.send_get(location, params={ })

		return decoded_json_response

	def garage(self):
		location = "garage"
		decoded_json_response = self.send_get(location, params={ })

		return decoded_json_response

	def alarm(self):
		location = "alarm"
		decoded_json_response = self.send_get(location, params={ })
		return decoded_json_response
	
	def camera(self):
		location = "camera"
		decoded_json_response = self.send_get(location, params={ })
		return decoded_json_response
	
	def setCamera(self,cameraName,newStatus, delay = False):
		location = "camera"
		params = {"cameraName" : cameraName , "newStatus" : newStatus}
		if delay:
			params['delay'] = delay 
		decoded_json_response = self.send_post(location, params=params)
		return True
	
	def allStatus(self):
		location = "allStatus"
		decoded_json_response = self.send_get(location, params={ })
		return decoded_json_response
