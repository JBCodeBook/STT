import json
import os
from dotenv import load_dotenv
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import subprocess


def getFiles():
    listof_files = []
    typeof_files = ['.wav', '.mp3']
    transcript_file = listfolders()

    while True:
        try:
            count = 0
            for opt in typeof_files:
                print(str(count + 1) + opt)
                count += 1

            select = int(input("What type of file would you like to process : \n"))
            if len(typeof_files) + 1 > select > 0:
                file_name = typeof_files[select - 1]
                print("\nselected : ", file_name, '\n')
                break
            else:
                select = 0
                print("Try again")

        except ValueError:
            print("Value not accepted")

    for files in os.listdir(transcript_file):
        if os.path.splitext(files)[1] == file_name:
            listof_files.append(files)

    return listof_files


def json_time(json_Object):
    flag = 0
    for i in json_Object['results']:
        if (flag != 1):
            time_start = (i['alternatives'][0]['timestamps'][0][1])
            flag = 1
        else:
            time_end = (i['alternatives'][0]['timestamps'][0][1])


def process_JSON(json_file):
    print("Processing JSON file...")
    with open(json_file, "r") as read_file:

        json_object = json.load(read_file)

    transcript_dict = {}
    count = 1

    for i in json_object['results']:
        time_start = i['alternatives'][0]['timestamps'][0][1]
        for j in json_object['speaker_labels']:
            if time_start == (j['from']):
                transcript_dict[count] = {'speaker': j['speaker'], 'confidence': i['alternatives'][0]['confidence'],
                                          'transcript': i['alternatives'][0]['transcript']}
                count += 1

    with open('newTranscript', 'w') as outFile:
        json.dump(transcript_dict, outFile, indent=4)


def print_to_html(json_file):
    prev_speaker = None
    cur_speaker = None

    if (os.path.basename('trasncript_HTML')):
        os.remove(os.path.basename('transcript_HTML'))

    with open(json_file, "r") as read_file:
        json_Object = json.load(read_file)

    for key in json_Object:

        cur_speaker = json_Object[key]['speaker']
        transcript = json_Object[key]['transcript']

        with open("transcript_HTML", 'a+') as outFile:
            if prev_speaker == cur_speaker:
                line = " " * 5 + "<p>" + transcript + "</p>"
                outFile.write(line + '\n')

            elif prev_speaker == None or prev_speaker != cur_speaker:
                line = "<h3>speaker 1</h3>"
                outFile.write(line + '\n')
                line = " " * 5 + "<p>" + transcript + "</p>"
                outFile.write(line + '\n')

        prev_speaker = json_Object[key]['speaker']


def watson_Compreess():
    print("Compressing files")
    command = 'ffmpeg -i 1.wav -vn -ar 44100 -ac 2 -b:a 192k audio.mp3'
    subprocess.call(command, shell=True)
    command = 'ffmpeg -i audio.mp3 -f segment -segment_time 360 -c copy %03d.mp3'
    subprocess.call(command, shell=True)
    print("Finished Compressing files")


def listfolders():
    filenames = os.listdir(".")  # get all files' and folders' names in the current directory

    result = []
    ignore = ['.git', '.idea', '__pycache__']
    for filename in filenames:  # loop through all the files and folders
        if (filename in ignore):
            continue
        if os.path.isdir(
                os.path.join(os.path.abspath("."), filename)):  # check whether the current object is a folder or not
            result.append(filename)

    result.sort()
    print("test")

    select = 0
    acceptable_values = list(range(1, len(result)))
    file_name = None

    for i in range(0, len(result)):
        print('[' + str((i + 1)) + ']', result[i])

    while True:
        try:
            select = int(input("Which folder would you like to process : "))
            if len(result) + 1 > select > 0:
                file_name = result[select - 1]
                break
            else:
                select = 0
                print("Try again")

        except ValueError:
            print("Value not accepted")

    return os.path.abspath(file_name)


# return error and repeat input


def watsonStart(API, URL, fileto_convert):

    print(fileto_convert)

    # Setup Service
    # authenticator = IAMAuthenticator(API)
    # service = SpeechToTextV1(authenticator=authenticator)
    # service.set_service_url(URL)
    #
    # models = service.list_models().get_result()
    #
    # files = []
    # for filename in os.listdir(path):
    #     print(filename)
    #     if filename.endswith(".wav") and filename != 'audio.mp3':
    #         files.append(filename)
    # files.sort()
    #
    # print("Starting to process audio")
    #
    # results = []
    # fileName = path + "/" + files[0]
    #
    # # for filename in files:
    # with open(fileName, 'rb') as f:
    #     print(f)
    #     res = service.recognize(
    #         audio=f,
    #         content_type='audio/wav',
    #         timestamps=True,
    #         speaker_labels=True
    #     ).get_result()
    #
    #     with open('output.txt', 'w+') as out:
    #         json.dumps(res, out)
