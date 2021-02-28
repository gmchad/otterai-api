from requests_toolbelt.multipart.encoder import MultipartEncoder
import xml.etree.ElementTree as ET
import requests
import json

class OtterAI:
	API_BASE_URL = 'https://otter.ai/forward/api/v1/'
	S3_BASE_URL = 'https://s3.us-west-2.amazonaws.com/'

	def __init__(self):
		self._session = requests.Session()
		self._userid = None

	def _is_userid_invalid(self):
		if not self._userid:
			return True
		return False

	def login(self, username, password):
		# API URL
		auth_url = OtterAI.API_BASE_URL + 'login'
		# Query Parameters
		payload = {'username': username}
		# Basic Authentication
		self._session.auth = (username, password)
		# GET
		response = self._session.get(auth_url, params=payload)
		# Set userid
		response_json = response.json()
		self._userid = response_json['userid']

		if response.status_code == requests.codes.ok:
			return response_json
		else:
			return {}

	def user(self):
		# API URL
		user_url = OtterAI.API_BASE_URL + 'user'
		# GET
		response = self._session.get(user_url)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return {}

	def speakers(self):
		# API URL
		speakers_url = OtterAI.API_BASE_URL + 'speakers'
		# Query Parameters
		if self._is_userid_invalid():
			return {}
		payload = {'userid': self._userid}
		# GET
		response = self._session.get(speakers_url, params=payload)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return {}

	def speeches(self, folder=0, page_size=45, source="owned"):
		# API URL
		speeches_url = OtterAI.API_BASE_URL + 'speeches'
		# Query Parameters 
		if self._is_userid_invalid():
			return {}
		payload = {'userid': self._userid, 
				'folder': folder, 
				'page_size': page_size, 
				'source': owned}
		# GET
		response = self._session.get(speeches_url, params=payload)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return {}

	def get_speech(self, speech_id):
		pass

	def query_speech(self, query, speed_id):
		pass

	def move_to_trash(self, speed_id):
		pass

	def upload_speech(self, file_name, content_type='audio/mp4'):
		# API URL
		speech_upload_params_url = OtterAI.API_BASE_URL + 'speech_upload_params'
		speech_upload_prod_url = OtterAI.S3_BASE_URL + 'speech-upload-prod'
		finish_speech_upload = OtterAI.API_BASE_URL + 'finish_speech_upload'

		# First grab upload params (aws data)
		if self._is_userid_invalid():
			return {}
		payload = {'userid': self._userid}
		response = self._session.get(speech_upload_params_url, params=payload)

		if response.status_code != requests.codes.ok:
			return {}

		response_json = response.json()
		params_data = response_json['data']

		# Send options (precondition) request
		prep_req = requests.Request('OPTIONS', speech_upload_prod_url).prepare()
		prep_req.headers['Accept'] = '*/*'
		prep_req.headers['Connection'] = 'keep-alive'
		prep_req.headers['Origin'] = 'https://otter.ai'
		prep_req.headers['Referer'] = 'https://otter.ai/'
		prep_req.headers['Access-Control-Request-Method'] = 'POST'
		# POST
		response = self._session.send(prep_req)

		if response.status_code != requests.codes.ok:
			return {}
		
		# Post file to bucket
		# TODO: test for large files
		fields = {}
		params_data['success_action_status'] = str(params_data['success_action_status'])
		del params_data['form_action']
		fields.update(params_data)
		fields['file'] = (file_name, open(file_name, mode='rb'), content_type)
		multipart_data = MultipartEncoder(fields=fields)
		# POST
		response = requests.post(speech_upload_prod_url, data=multipart_data,
			headers={'Content-Type': multipart_data.content_type})

		if response.status_code != 201:
			return {}

		# Pase xml response
		xmltree = ET.ElementTree(ET.fromstring(response.text))
		xmlroot = xmltree.getroot()
		# TODO: clean this up
		location = xmlroot[0].text
		bucket = xmlroot[1].text
		key = xmlroot[2].text

		# Call finish api
		payload = {'bucket': bucket, 'key': key, 'language': 'en', 'country': 'us', 'userid': self._userid}
		response = self._session.get(finish_speech_upload, params=payload)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return {}

	def notification_settings(self):
		# API URL
		notification_settings_url = OtterAI.API_BASE_URL + 'get_notification_settings'

	def list_groups(self):
		# API URL
		list_groups_url = OtterAI.API_BASE_URL + 'list_groups'

	def folders(self):
		# API URL
		folders_url = OtterAI.API_BASE_URL + 'folders'

	def speech_start(self):
		# API URL
		speech_start_uel = OtterAI.API_BASE_URL + 'speech_start'
		### TODO
		# In the browser a websocket session is opened
		# wss://ws.aisense.com/api/v2/client/speech?token=ey...
		# The speech_start endpoint returns the JWT token

	def stop_speech(self):
		# API URL
		speech_finish_url = OtterAI.API_BASE_URL + 'speech_finish'
