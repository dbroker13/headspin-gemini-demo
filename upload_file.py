from google import genai
import requests
import time
import os

GEMINI_KEY = os.environ["GEMINI_KEY"]
client = genai.Client(api_key=GEMINI_KEY)
API_KEY = os.environ["API_KEY"]
api_token = API_KEY

MAX_RETRIES = 5
WAIT_SECONDS = 30

sessionFile = open("session_info.txt", "r")
sessionID = sessionFile.read()

#just wait for video to be available replace with better wait method
time.sleep(15)
downloadURL = f'https://api-dev.headspin.io/v0/sessions/{sessionID}.mp4'

headers = {"Authorization": "Bearer " + api_token}
response = requests.get(downloadURL, headers=headers)
if response.status_code != 200:
    print(response.status_code)

with open(f'{sessionID}.mp4', 'wb') as videoFile:
    videoFile.write(response.content)

# name = "\"" + sessionID + ".mp4\""
name =  f'{sessionID}.mp4'
print(name)
# print("Uploading file...")
# config = {}
# config['diplay_name'] = sessionID
geminiFile = client.files.upload(file=name)
# print(f"Completed upload: {video_file.uri}")
# f  = client.files.list()
fileName = geminiFile.name
for attempt in range(1, MAX_RETRIES + 1):
    myfile = client.files.get(name=fileName)
    print(f"Attempt {attempt}...")
    state = myfile.state
    if str(state) == "FileState.ACTIVE":
        print("Success! State reached.")
        break
    else:
        print(f"State is '{state}', waiting...")

    if attempt < MAX_RETRIES:
        time.sleep(WAIT_SECONDS)
else:
    print("Failed to reach desired state after retries.")
# Pass the video file reference like any other media part.
# geminiFile = client.files.get(name=f'{sessonID}.mp4')

promptFile = open("prompt.txt", "r")
prompt = promptFile.read()

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        geminiFile,
        prompt])
# Print the response, rendering any Markdown
#Markdown(response.text)
print(response.text)
responseFile = open("geminiResponse.txt", "w")
with open("geminiResponse.txt", "w") as file:
    responseFile.write(response.text)
client.files.delete(name=fileName)
