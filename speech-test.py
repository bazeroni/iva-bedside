import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

# loads env variables file
load_dotenv()

# Create the speech config
AZURE_SPEECH_KEY = os.getenv("AZURE") #AZURE

stt_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# configs tts
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region="eastus")

# Create the speech recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=stt_config)

# Start continuous speech recognition
speech_recognition_result = speech_recognizer.start_continuous_recognition_async()

# Output the recognized text as it is recognized
while True:
    result = speech_recognition_result

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("Speech could not be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech recognition was canceled.")
        break