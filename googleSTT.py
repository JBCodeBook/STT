# pip install --upgrade google-cloud-speech

# imports
import io
import os
from google.cloud import speech_v1p1beta1 as speech


"""Google Cloud Speech-to-Text sample application using the gRPC for async
batch processing.
"""


# [START speech_transcribe_async_gcs]
def transcribe_gcs():
    import config
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.google_json

    speech_file = config.audio_file
    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
# [END speech_transcribe_async_gcs]