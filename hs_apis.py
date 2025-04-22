import time
import requests
import json

class HS_API():


    #INTIALIZATION OF APIs WITH HS API TOKEN
    def __init__(self, api_token, device_address=None):
        self.api_token = api_token
        self.url_root = 'https://api-dev.headspin.io/v0/'
        self.headers = {}
        self.headers["Authorization"] = "Bearer {}".format(api_token)
        self.device_address= device_address
        self.session_id = ""
    
    def setSessionID(self, session_id):
        self.session_id = session_id

    def start_capture(self, device_address):
        request_url = self.url_root + "sessions"
        payload = {}
        payload['device_address'] = device_address
        payload['session_type'] = "capture"
        payload['capture_network'] = False
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data = payload)
        json_data = json.loads(response.text)
        if response.status_code == 200:
            print("Complete")
            session_id = json_data['session_id']
            self.setSessionID(session_id)
        else:
            print("Error creating session....\n")

    def stop_capture(self):
        request_url = self.url_root + "sessions/" + self.session_id
        payload = {}
        payload['active'] = False
        payload = json.dumps(payload)
        response = requests.patch(request_url, headers=self.headers, data = payload)
        json_data = json.loads(response.text)
        if response.status_code == 200:
            print("Complete")
        else:
            print("Error stopping session....\n")

    def prepare_audio(self, hostname, audio_ids):
        request_url = self.url_root + "audio/prepare"
        payload = {}
        payload['hostname'] = hostname
        payload['audio_ids'] = audio_ids
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data = payload)
        json_data = json.loads(response.text)
        if response.status_code == 200:
            print("Complete")
        else:
            print("Error preparing audio....\n")
    
    def inject_audio(self, device_address, audio_id):
        request_url = self.url_root +  "audio/inject/start"
        payload = {}
        payload['device_address'] = device_address
        payload['audio_id'] = audio_id
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data = payload)
        json_data = json.loads(response.text)
        if response.status_code == 200:
            print("Complete")
            return json_data['worker_id']
        else:
            print("Error injecting audio....\n")
    
    def worker_wait(self, worker_id):
        request_url = self.url_root + f'inject/{worker_id}/wait'
        response = requests.get(request_url, headers=self.headers)
        json_data = json.loads(response.text)
        if response.status_code == 200:
            print("Complete")
        else:
            print("Error waiting for worker....\n")

    
    def get_timestamps(self, session_id):
        request_url = self.url_root + f'sessions/{session_id}/timestamps'
        response = requests.get(request_url, headers=self.headers)
        json_data = json.loads(response.text)
        if response.status_code == 200:
            print("Complete")
            return json_data['capture-started']
        else:
            print("Error injecting audio....\n")

    def create_labels(self, session_id, category, data):
        request_url = self.url_root + f'sessions/{session_id}/label/add'
        name = list(data.keys())
        payload = {}
        payload['name'] = name[0]
        payload['category'] = category
        payload['start_time'] = data[name[0]]['startTime']
        payload['end_time'] = data[name[0]]['endTime']
        payload = json.dumps(payload)
        print(payload)
        response = requests.post(request_url, headers=self.headers, data = payload)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            print("Label created for " + name[0])
        else:
            print(response)
            print("Error creating label for " +name[0])
    
    def run_audio_match(self, session_id, audio_ids, audio_start, audio_end):
        request_url = self.url_root + f'sessions/{session_id}/label/add'
        payload = {}
        session_data = {}
        session_data = [{"name": "audio match", "label_type": "audio-match-request", 
              "start_time": str(audio_start), "end_time": str(audio_end),
              "data": {"ref_audio_media_id": audio_ids}}]
        payload['labels'] = session_data
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data = payload)
        if response.status_code == 200:
            print("Complete")
        else:
            print("Error injecting audio....\n")