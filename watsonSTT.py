import json
import os
import config
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import subprocess

def watson_Compreess():

    print("Compressing files")
    command = 'ffmpeg -i 1.wav -vn -ar 44100 -ac 2 -b:a 192k audio.mp3'
    subprocess.call(command, shell=True)
    command = 'ffmpeg -i audio.mp3 -f segment -segment_time 360 -c copy %03d.mp3'
    subprocess.call(command, shell=True)
    print("Finished Compressing files")

def watsonStart():
    url = config.watson_url
    apikey = config.watson_api

    path = 'C:\\Users\\j2017\\Documents\\Audacity\\New folder'

    # Setup Service
    authenticator = IAMAuthenticator(apikey)
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url(url)

    models = service.list_models().get_result()



    files = []
    for filename in os.listdir('.'):
        if filename.endswith(".wav") and filename != 'audio.mp3':
            files.append(filename)
    files.sort()

    print("Starting to process audio")

    # print(json.dumps(
    #     service.recognize(
    #         audio=path,
    #         content_type='audio/flac',
    #         timestamps=True,
    #         word_confidence=True).get_result(),
    #     indent=2))

    results = []
    # for filename in files:
    with open(config.audio_file, 'rb') as f:
        print(f)
        res = service.recognize(
            audio=f,
            content_type='audio/mp3',
            interim_results=True,
            timestamps=True,
            speaker_labels=True
        ).get_result()

        test = json.dumps(res, indent=1)

        # text = res['results'][0]['alternatives'][0]['transcript']

        with open('output.txt', 'w+')as out:

            out.writelines(test)
