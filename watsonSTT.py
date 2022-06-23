import json
import os
import sys
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected

""" Speech to Text converter

This script will take audio files from a directory and send the file to IBM Watson's for processing through its 
speech to text API First the API and URL keys are authenticated. The script searchs the ./audio file to locate any 
folders and requests input for which folder to process. The files should be less than 100 MB or else it will be 
rejected by the service. JSON data is returned from service which is processed further and converted into HTML so it 
can be copied into a web format. 

"""

testing = True

def get_files():
    """ Prints out a menu to user and asks which folder they would like to process. Directory is return from
    list_folders()

    :returns
    file_list
        a list of files in the ./audio directory
    """

    files_list = []

    # Sets that will hold the files from the selected directory. Only certain file types allowed
    files_mp3 = []
    files_flac =  []
    files_wav = []

    #Create a dictionary that only allows certain types of files
    filedictionary = {'.wav': files_wav, '.mp3': files_mp3, '.flac': files_flac}



    transcript_file = list_folders()
    files_in_dir = os.listdir(transcript_file)

    # If the file exists and its suffix is a keyin the dictionary, add it to the dictionary
    for files in files_in_dir:
        if os.path.splitext(files)[1] in filedictionary:
            filedictionary[os.path.splitext(files)[1]].append(files)


    # Request input to select the format of the files to process
    while True:
        try:
            # Request which file types the user would like to transcribe
            count = 1
            file_opts = []
            print("\nFile Types Selection\n")
            print("\n\tWhat type of file would you like to process : \n")

            for dictkey in filedictionary:
                if len(filedictionary[dictkey]) > 0:
                    print("\t\t" + str(count) + dictkey)
                    file_opts.append((dictkey))
                    count += 1

            # using the file_opts, return the set of files in the dictionary that match the selected suffix
            if(not testing):
                select = int(input("\nSelect number: "))
                if count > select > 0:
                    print("\n\tselected: ", file_opts[select - 1])
                    return {file_opts[0]: filedictionary[file_opts[0]]}

                else:
                    print("Try again")
            else:
                return {file_opts[0]: filedictionary[file_opts[0]]}

        except ValueError:
            print("Value not accepted")

def process_json():
    """ Locates the JSON file returned by API call and builds a more simplier JSON file to work with"""

    tmp = os.listdir('./output')

    # Locates the JSON file in the .\output folder and loads it for processing
    for file in tmp:
        with open('.\\output\\' + file, "r") as read_file:
            json_object = json.load(read_file)

        transcript_dict = {}
        count = 1

        # 'speaker', 'timestamp' and 'transcript' fields are pulled from. New JSON file is created with that data
        for i in json_object['results']:
            time_start = i['alternatives'][0]['timestamps'][0][1]
            for j in json_object['speaker_labels']:
                if time_start == (j['from']):
                    transcript_dict[count] = {'speaker': j['speaker'], 'confidence': i['alternatives'][0]['confidence'],
                                              'transcript': i['alternatives'][0]['transcript']}
                    count += 1

            with open(os.getcwd() + '.\\intermediary_transcripts\\' + f'{file[0:-4]}_transcript.txt', 'w') as outFile:
                json.dump(transcript_dict, outFile, indent=4)

def print_to_html():
    """ Converts the information from the new transcript file into HTML so it can be copied into a webpage"""

    prev_speaker = None
    path_to_transcript = os.getcwd()
    print(path_to_transcript)

    # Deletes any previous transcript file in order to append to a new one
    if os.path.isfile(path_to_transcript + 'trasncript_HTML.txt'):
        os.remove(os.path.basename('transcript_HTML.txt'))
    else:
        print("file does not exist yet")

    # Creates a file with speaker, timestamp and transcript enclosed with HTML <h3> and <p> tags
    with open(path_to_transcript + "\\finished_transcripts\\" "transcript_HTML.txt", 'a+') as outFile:
        print("Printing finished transcript to: ", path_to_transcript + "\\finished_transcripts\\" "transcript_HTML.txt")
        for f in os.listdir(path_to_transcript + '\\intermediary_transcripts\\'):
            print("Writing transcript to: " + path_to_transcript + '\\intermediary_transcripts\\' + f)
            with open(path_to_transcript + '\\intermediary_transcripts\\' + f, "r") as read_file:
                json_obj = json.load(read_file)

            for key in json_obj:

                cur_speaker = json_obj[key]['speaker']
                transcript = json_obj[key]['transcript']

                if prev_speaker == cur_speaker:
                    line = " " * 5 + "<p>" + transcript + "</p>"
                    outFile.write(line + '\n')

                elif prev_speaker is None or prev_speaker != cur_speaker:
                    line = f"<h3>Speaker {cur_speaker}</h3>"
                    outFile.write(line + '\n')
                    line = " " * 5 + "<p>" + transcript + "</p>"
                    outFile.write(line + '\n')

            prev_speaker = json_obj[key]['speaker']


def list_folders():
    """ Lists all the folders in the ./audio directory """

    filenames = os.listdir("./audio")
    filepath = os.path.join(os.path.abspath(".") + '\\audio\\')

    result = []
    ignore = ['.git', '.idea', '__pycache__']

    for filename in filenames:

        if filename in ignore:
            print(f"ignoring file : {filename} \n")
            continue

        if os.path.isdir(filepath + filename):
            print(f'{filename} added to the list \n')
            result.append(filename)

    result.sort()

    # Menu prints the folders available to process and accepts input for which folder to select
    while True:
        try:

            cprint(figlet_format('Menu!', font='starwars'),
                   'yellow', 'on_red', attrs=['bold'])

            print("Please select Folder\n")

            for i in range(0, len(result)):
                print('\t\t[' + str((i + 1)) + ']', result[i])

            if not testing:
                select = int(input("\nWhich folder would you like to process : "))

                if len(result) + 1 > select > 0:
                    file_name = result[select - 1]
                    break
                else:
                    print("Try again")
            else:
                file_name = result[1 - 1]
                break

        except ValueError:
            print("Value not accepted")

    return os.path.abspath(filepath + file_name)


def clean_folders():
    """ Removes any files before starting from ./output and ./transcripts """

    output_path = '.\\output'
    transcript_path = '.\\intermediary_transcripts'

    if len(output_path) > 0:
        for f in os.listdir(output_path):
            print(f"Removing {os.path.join(output_path, f)}")
            os.remove(os.path.join(output_path, f))

    if len(transcript_path) > 0:
        for f in os.listdir(transcript_path):
            print(f"Removing {os.path.join(transcript_path, f)}")
            os.remove(os.path.join(transcript_path, f))


def watson_start(API, URL):
    """
    Starts the process of transcibing the audio files.
    Authenticates keys through API. Builds and sends the
    request. Calls the methods to process the JSON files.
    """

    output_path = os.path.abspath('output')
    output_files = []
    clean_folders()

    # Creates list of files to process
    audio_dictionary = get_files()
    suffix, audio_files = list(audio_dictionary.items())[0]


    print("Authenticating service...")

    # Setup Service
    authenticator = IAMAuthenticator(API)
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url(URL)
    print("Service Authenticated.")

    models = service.list_models().get_result()

    # Sends audio files one by one through the recognize API call
    for file in audio_files:
        file_basename = os.path.basename(file)
        output_file = output_path + '\\' + os.path.basename(os.path.splitext(file)[0]) + ".txt"

        output_files.append(output_file)
        file_basename = os.getcwd() + "\\audio\\test\\" + file_basename
        print(f"Transcribing {file_basename}")
        ctype = 'audio/' + suffix[1:]
        with open(file_basename, 'rb') as f:
            res = service.recognize(
                audio=f,
                content_type=ctype,
                timestamps=True,
                speaker_labels=True
            ).get_result()

            with open(output_file, 'w+') as out:
                print(f"Printing Json dump to file {output_file}")
                json.dump(res, out)

    # Simplify JSON data into something that is easier to work with
    process_json()

    # Convert the JSON data into a web
    print_to_html()
