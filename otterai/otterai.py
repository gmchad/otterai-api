from requests_toolbelt.multipart.encoder import MultipartEncoder
import xml.etree.ElementTree as ET
import requests
import json

class OtterAIException(Exception):
    pass

class OtterAI:
    API_BASE_URL = 'https://otter.ai/forward/api/v1/'
    S3_BASE_URL = 'https://s3.us-west-2.amazonaws.com/'

    def __init__(self):
        self._session = requests.Session()
        self._userid = None
        self._cookies = None

    def _is_userid_invalid(self):
        if not self._userid:
            return True
        return False

    def _handle_response(self, response):
        try:
            return {'status': response.status_code, 'data': response.json()}
        except ValueError:
            return {'status': response.status_code, 'data': {}}

    def login(self, username, password):
        # API URL
        auth_url = OtterAI.API_BASE_URL + 'login'
        # Query Parameters
        payload = {'username': username}
        # Basic Authentication
        self._session.auth = (username, password)
        # GET
        response = self._session.get(auth_url, params=payload)
        # Check
        if response.status_code != requests.codes.ok:
            return self._handle_response(response)
        # Set userid & cookies
        self._userid = response.json()['userid']
        self._cookies = response.cookies.get_dict()

        return self._handle_response(response)

    def get_user(self):
        # API URL
        user_url = OtterAI.API_BASE_URL + 'user'
        # GET
        response = self._session.get(user_url)

        return self._handle_response(response)

    def get_speakers(self):
        # API URL
        speakers_url = OtterAI.API_BASE_URL + 'speakers'
        if self._is_userid_invalid():
            raise OtterAIException('userid is invalid')      
        # Query Parameters
        payload = {'userid': self._userid}
        # GET
        response = self._session.get(speakers_url, params=payload)

        return self._handle_response(response)
    
    def get_speeches(self, folder=0, page_size=45, source="owned"):
        # API URL
        speeches_url = OtterAI.API_BASE_URL + 'speeches'
        if self._is_userid_invalid():
            raise OtterAIException('userid is invalid')
        # Query Parameters 
        payload = {'userid': self._userid, 
                'folder': folder, 
                'page_size': page_size, 
                'source': source}
        # GET
        response = self._session.get(speeches_url, params=payload)

        return self._handle_response(response)

    def get_speech(self, speech_id):
        # API URL
        speech_url = OtterAI.API_BASE_URL + 'speech'
        if self._is_userid_invalid():
            raise OtterAIException('userid is invalid')
        # Query Params
        payload = {'userid': self._userid, 'otid': speech_id}
        # GET
        response = self._session.get(speech_url, params=payload)

        return self._handle_response(response)

    def query_speech(self, query, speech_id, size=500):
        # API URL
        query_speech_url = OtterAI.API_BASE_URL + 'advanced_search'
        # Query Params
        payload = {'query': query, "size": size, "otid": speech_id}
        # GET
        response = self._session.get(query_speech_url, params=payload)

        return self._handle_response(response)

    def upload_speech(self, file_name, content_type='audio/mp4'):
        # API URL
        speech_upload_params_url = OtterAI.API_BASE_URL + 'speech_upload_params'
        speech_upload_prod_url = OtterAI.S3_BASE_URL + 'speech-upload-prod'
        finish_speech_upload = OtterAI.API_BASE_URL + 'finish_speech_upload'

        if self._is_userid_invalid():
            raise OtterAIException('userid is invalid')

        # First grab upload params (aws data)
        payload = {'userid': self._userid}
        response = self._session.get(speech_upload_params_url, params=payload)

        if response.status_code != requests.codes.ok:
            return self._handle_response(response)

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
            return self._handle_response(response)
        
        # Post file to bucket
        # TODO: test for large files (this should stream)
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
            return self._handle_response(response)

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

        return self._handle_response(response)

    def move_to_trash_bin(self, speech_id):
        # API URL
        move_to_trash_bin_url = OtterAI.API_BASE_URL + 'move_to_trash_bin'
        if self._is_userid_invalid():
            raise OtterAIException('userid is invalid')
        # Query Params
        payload = {'userid': self._userid}
        # POST
        data = {'otid': speech_id}
        headers = {'x-csrftoken': self._cookies['csrftoken']}
        response = self._session.post(move_to_trash_bin_url, params=payload, headers=headers, data=data)

        return self._handle_response(response)

    def create_speaker(self, speaker_name):
        # API URL
        create_speaker_url = OtterAI.API_BASE_URL + 'create_speaker'
        if self._is_userid_invalid():
            raise OtterAIException('userid is invalid')
        # Query Parameters
        payload = {'userid': self._userid}
        # POST
        data = {'speaker_name': speaker_name}
        headers = {'x-csrftoken': self._cookies['csrftoken']}
        response = self._session.post(create_speaker_url, params=payload, headers=headers, data=data)

        return self._handle_response(response)

    def get_notification_settings(self):
        # API URL
        notification_settings_url = OtterAI.API_BASE_URL + 'get_notification_settings'
        response = self._session.get(notification_settings_url)
        
        return self._handle_response(response)

    def list_groups(self):
        # API URL
        list_groups_url = OtterAI.API_BASE_URL + 'list_groups'
        if self._is_userid_invalid():
            raise OtterAIException('userid is invalid')
        # Query Parameters
        payload = {'userid': self._userid}
        # GET
        response = self._session.get(list_groups_url, params=payload)

        return self._handle_response(response)

    def get_folders(self):
        # API URL
        folders_url = OtterAI.API_BASE_URL + 'folders'
        if self._is_userid_invalid():
            raise OtterAIException('userid is invalid')
        # Query Parameters
        payload = {'userid': self._userid}
        # GET
        response = self._session.get(folders_url, params=payload)

        return self._handle_response(response)

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
