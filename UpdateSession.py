import re
import json
import hs_apis
import os

from hs_apis import HS_API

API_KEY = os.environ["API_KEY"]
auth_token = API_KEY
api = HS_API(auth_token)

sessionFile = open("session_info.txt", "r")
sessionID = sessionFile.read()

responseFile = open("geminiResponse.txt", "r")
response = responseFile.read()
# print(response)

match = re.search(r'```json(.*?)```', response, re.DOTALL)
if match:
    json_str = match.group(1).strip()
    data = json.loads(json_str) 
    for key in data:
        if key != "content":
            if data[key] != []:
                for instance in data[key]:
                    api.create_labels(sessionID, key, instance)

else: 
    print("No JSON block found.")
