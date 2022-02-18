import json
import os
import sys
from colorama import init
import subprocess
from termcolor import cprint
from pyfiglet import figlet_format
from dotenv import load_dotenv
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected


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

            select = int(input("\nWhat type of file would you like to process : \n"))
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
            f = transcript_file + '\\' + files
            listof_files.append(f)

    return listof_files


def process_JSON(json_files):
    tmp = os.listdir('./output')

    for file in tmp:
        # print(f"Processing {file} file...")
        with open('.\\output\\' + file, "r") as read_file:
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

            with open('.\\transcripts\\' + f'{file}_transcript.txt', 'w') as outFile:
                json.dump(transcript_dict, outFile, indent=4)


def print_to_html():
    prev_speaker = None
    cur_speaker = None

    if (os.path.isfile('trasncript_HTML.txt')):
        os.remove(os.path.basename('transcript_HTML.txt'))
    else:
        print("file does not exist yet")

    with open("transcript_HTML.txt", 'a+') as outFile:
        for file in os.listdir('.\\transcripts\\'):
            print("processing")
            with open('.\\transcripts\\' + file, "r") as read_file:
                json_Object = json.load(read_file)

            for key in json_Object:

                cur_speaker = json_Object[key]['speaker']
                transcript = json_Object[key]['transcript']

                if prev_speaker == cur_speaker:
                    line = " " * 5 + "<p>" + transcript + "</p>"
                    outFile.write(line + '\n')

                elif prev_speaker == None or prev_speaker != cur_speaker:
                    line = "<h3>speaker 1</h3>"
                    outFile.write(line + '\n')
                    line = " " * 5 + "<p>" + transcript + "</p>"
                    outFile.write(line + '\n')

            prev_speaker = json_Object[key]['speaker']


def listfolders():
    filenames = os.listdir("./audio")  # get all files' and folders' names in the current directory
    filepath = os.path.join(os.path.abspath(".") + '\\audio\\')

    result = []
    ignore = ['.git', '.idea', '__pycache__']
    for filename in filenames:  # loop through all the files and folders

        if filename in ignore:
            print(f"ignoring file : {filename} \n")
            continue

        if os.path.isdir(filepath + filename):
            print(f'{filename} added to the list \n')
            result.append(filename)

    result.sort()

    while True:
        try:

            cprint(figlet_format('Menu!', font='starwars'),
                   'yellow', 'on_red', attrs=['bold'])

            print("Please select Folder\n")

            for i in range(0, len(result)):
                print('[' + str((i + 1)) + ']', result[i])

            select = int(input("\nWhich folder would you like to process : "))
            if len(result) + 1 > select > 0:
                file_name = result[select - 1]
                break
            else:
                select = 0
                print("Try again")

        except ValueError:
            print("Value not accepted")

    return os.path.abspath(filepath + file_name)


def clean_folders():
    pathToOutput = '.\\output'
    pathToTranscripts = '.\\transcripts'

    if(len(pathToOutput) > 0):
        for f in os.listdir(pathToOutput):
            print(f"Removing {os.path.join(pathToOutput, f)}")
            os.remove(os.path.join(pathToOutput, f))

    if(len(pathToTranscripts) > 0):
        for f in os.listdir(pathToTranscripts):
            print(f"Removing {os.path.join(pathToTranscripts, f)}")
            os.remove(os.path.join(pathToTranscripts, f))


def watsonStart(API, URL):
    output_path = os.path.abspath('output')
    output_files = []
    clean_folders()

    filesto_convert = getFiles()

    print("Authenticating service...")

    # Setup Service
    try:
        authenticator = IAMAuthenticator(API)
        service = SpeechToTextV1(authenticator=authenticator)
        service.set_service_url(URL)
        print("Service Authenticated.")
    except:
        print("Could not Authenticate service")

    models = service.list_models().get_result()

    for file in filesto_convert:
        file_basename = os.path.basename(file)
        output_file = output_path + '\\' + os.path.basename(os.path.splitext(file)[0]) + ".txt"

        output_files.append(output_file)
        print(f"Transcribing {file_basename}")

        with open(file, 'rb') as f:
            res = service.recognize(
                audio=f,
                content_type='audio/wav',
                timestamps=True,
                speaker_labels=True
            ).get_result()

            with open(output_file, 'w+') as out:
                print(f"Printing Json dump to file {output_file}")
                json.dump(res, out)

    process_JSON(output_files)
    print_to_html()
