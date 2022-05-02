 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 
# STT
Speech to text application using Watson and Google STT

Description

This script will take audio files from a directory and send the file to IBM Watson's for processing through its 
speech to text API First the API and URL keys are authenticated. The script searchs the ./audio file to locate any 
folders and requests input for which folder to process. The files should be less than 100 MB or else it will be 
rejected by the service. JSON data is returned from service which is processed further and converted into HTML so it 
can be copied into a web format. 

## Getting Started
Dependencies

 - json
 - os
 - sys
 - colorama 
 - termcolor
 - pyfiglet
 - ibm_watson 
 - ibm_cloud_sdk_core.authenticators
 
 Additionally an API key will be required to use the project. The API key can be obtained from https://www.ibm.com/watson/developer

## Installing
 
 Clone Repository into directory of your choice. Create the following directories in the root folder.
  - audio
  - output
  - transcripts
  - 

Place audio files that are to be converted into their own directory inside ./audio so structure looks like so
```
├───.idea
│   └───inspectionProfiles
├───audio
│   └───Barry Manilow
├───output
├───transcripts
└───__pycache__
```
Create a .env file in the root directory and place API key and URL in this .env file like so
```
API_KEY={API KEY}
URL={API URL}
```

## Executing program

  From root directory:
    
  ```
  python main.py
  ```

## Help

This program was build using Watson API. Watson does place restrictions on the file size that can be uploaded synchronously. This is resolved by breaking the audio file into smaller files, usually 100MB works well. I have had success using Audacity to pre-process files. 


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

