import json
import os

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import subprocess

url = 'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/452cd992-1539-4886-9e3d-6d94bd5e2e83'

path = 'C:\\Users\\j2017\\Documents\\Audacity\\jre_30min.flac'

# Setup Service
# authenticator = IAMAuthenticator(apikey)
# service = SpeechToTextV1(authenticator=authenticator)
# service.set_service_url(url)
#
# models = service.list_models().get_result()


command =  'ffmpeg -i JRE1719_MichaelShellenberger.flac -vn -ar 44100 -ac 2 -b:a 192k audio.mp3'
subprocess.call(command, shell=True)
command = 'ffmpeg -i audio.mp3 -f segment -segment_time 360 -c copy %03d.mp3'
subprocess.call(command, shell=True)


files = []
for filename in os.listdir('.'):
    if filename.endswith(".mp3") and filename !='audio.mps':
        files.append(filename)
files.sort()

# print(json.dumps(
#     service.recognize(
#         audio=fullPath,
#         content_type='audio/wav',
#         timestamps=True,
#         word_confidence=True).get_result(),
#     indent=2))
#
# with open('output.txt', 'w+') as out:
#
#     with open(path, 'rb') as f:
#         res = service.recognize(audio=f, content_type='audio/wav', timestamps=True, word_confidence=True).get_result()
#
#         text = res= ['results'][0]['alternatives'][0]['transcript']
#         confidence = ['results'][0]['alternatives'][0]['confidence']
#         out.writelines(text + '\n')

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data)