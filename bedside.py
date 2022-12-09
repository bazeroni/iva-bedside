import keyboard
import os
import re
import datetime
import time
import json
import openai
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from playsound import playsound
from voice import tts_voice, stt_language

def get_chart():
    
    global chart_json
    
    # Open the JSON file
    with open('patient.json') as json_file:
        
        # Load the data from the JSON file
        chart_json = json.load(json_file)
    
    chart_json["CHART"]["LOCATION"]["datetime current"] = time_current
    
    chart_json["CHART"]["DEMOGRAPHICS"]["primary language"] = primary_language
        
    return chart_json

def concatenate_context():
    
    global messages
    global context
    
    if len(messages) == 3:
        messages.pop()
        
    #print(len(messages))
    
    context += "".join(messages)

# inputs and reads patient prompt
# responds with given style from TONE_GPT3()
# returns response
def chat_gpt3(zice):
    
    #start_time = time.time()
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt= "You are, "+bot+", a bedside medical assistant at Trinity University Hospital for a patient named "+patient+". Speak to "+patient+" only in "+primary_language+" colloquially with patience, compassion, empathy, and assurance. Keep the patient relaxed and informed. Explain things in understandable terms. When "+patient+" has a request or need that strictly falls under the COMMANDS list below, you alert the care team by inserting the exact command and it's parameter/reason between brackets within a message.\n\n----------------MEDICAL CHART JSON-------------------\n\n"+chart+command_prompt+"\n\n----------------START OF CHAT-------------------\n\n"+context+"\n"+patient+": "+zice+"\n"+bot+":",
        #prompt= "You are, "+bot+", a clinical bedside intelligent virtual assistant (IVA) at Trinity University Hospital for a patient named "+patient+". Speak to "+patient+" only in "+language_primary+" with patience, empathy, and assurance. Keep the patient company and have conversations with them. Kindly instruct the patient to press their nurse call button on their TV remote when needed.\n\n"+chart+context+"\n"+patient+": "+zice+"\n"+bot+":",
        temperature=0.7,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=2.0,
        presence_penalty=2.0,
        stop=[patient+":", bot+":"],
        echo=False,
        stream=True,
    )
    #response_time = time.time() - start_time
    
    # create variables to collect the stream of events
    collected_events = []
    completion_text = ""
    print(f"{bot}:", end="")
    
    # iterate through the stream of events
    for event in response:
        collected_events.append(event)  # save the event response
        event_text = event['choices'][0]['text']  # extract the text
        # Encode the string using the utf-8 codec
        completion_text += event_text  # append the text
        print(event_text, end="")  # print the delay and text
        
    print("\n")
    # print response time
    #print(f" [{response_time:.2f} S]\n")
        
    return completion_text

def parse_command(text):
    
    global current_requests
    
    # strips tts text of commands
    text_clean = re.sub(r'\[.*?\]', '', text)
    
    # compile regular expression pattern to match contents of brackets '[]'
    pattern = re.compile(r'\[(.*?)\]')
    
    # find all occurrences of pattern in string and save as list
    current_requests = pattern.findall(text)
    
    return text_clean

def run_command():
    
    global current_requests
    
    request_split = current_requests[0].split(":")
    current_requests = []
    
    command = request_split[0].upper()
    parameter = request_split[1].upper()
    
    match command:
        case "PATIENT REQUESTS NURSE":
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")
        case "BED ASSIST":
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")
        case "BATHROOM ASSIST":
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")
        case "DRESS ASSIST":
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")
        case "PAIN REQUEST":
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")
        case "FOOD REQUEST":
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")
        case "FLUID REQUEST":
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")
        case "CHANGE ROOM TEMPERATURE":
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")
        case "LIGHT":
            match parameter:
                case "NO":
                    playsound('call.wav', False)
                    print(f"\n[{time_current}] {command}: {parameter}\n")
                case "YES":
                    playsound('call.wav', False)
                    print(f"\n[{time_current}] {command}: {parameter}\n")
                case default:
                    playsound('call.wav', False)
                    print(f"\n[{time_current}] {command}: {parameter}\n")
                    
        case "PRIVACY FILTER":
            match parameter:
                case "NO":
                    playsound('call.wav', False)
                    print(f"\n[{time_current}] {command}: {parameter}\n")
                case "YES":
                    playsound('call.wav', False)
                    print(f"\n[{time_current}] {command}: {parameter}\n")
                case default:
                    playsound('call.wav', False)
                    print(f"\n[{time_current}] {command}: {parameter}\n")
        case default:
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")

def respond(prompt, response):
    
    global messages
    global silence_count
    
    # take out commands
    if "[" and "]" in response:
        response = parse_command(response)

    # SSML for TTS with response and style
    xml_string = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
    xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="'''+voice+'''">
    <prosody rate="'''+rate+'''">
    <mstts:express-as style="'''+style+'''" styledegree="2">
    '''+ response +'''
    </mstts:express-as>
    </prosody>
    </voice>
    </speak>'''
    
    global speech_synthesizer; speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None) # inits tts
    
    # synthesizes TTS with input SSML
    speech_synthesizer.speak_ssml_async(xml_string).get()
    
    messages.append("\n"+prompt+"\n"+bot+": "+response)
    
    # runs if commands are present
    if len(current_requests) == 1: run_command()

    # concats message to memory/history
    concatenate_context()

    # resets silence count to 0
    silence_count = 0

# given input stt
# generates style and response from GPT-3
# synthesizes response tts
def think(inp):
    
    global silence_count
    
    # checks if there is verbal input
    if inp != "":
        
        # parses and formats patient input
        prompt = patient+": "+inp
        print(prompt+"\n")
        
        # gets GPT text message response completion
        response = chat_gpt3(inp)
        
        respond(prompt, response)
        
        return
    
    # assumes there is no input
    # checks if has been silent for three rounds
    elif silence_count == 2:
        
        # imitates silent input
        prompt = patient+": ..."
        print("\n\n", end="\r")
        
        # gets GPT text message response completion
        response = chat_gpt3("...")
        
        respond(prompt, response)
        
        return
            
    # increases silence count
    silence_count += 1
    
def listeningAnimation():
    
    listening = "||||||||||||||||||||||||||||||||||||||||"
    
    for character in listening:
        time.sleep(0.005)
        print(character, end="")

    print("\r", end="\r")
    
    for letter in range(len(listening)):
        time.sleep(0.005)
        print(" ", end="")
        
    print("\r", end="\r")
    
def recognize():
    
    # gets azure stt
    done = False

    def stop_cb(evt):
        
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition_async()
        nonlocal done
        done = True
    
    speech_recognizer.recognizing.connect(lambda evt: print(evt.result.text, end="\r"))
    speech_recognizer.recognized.connect(lambda evt: think(evt.result.text))
    speech_recognizer.session_started.connect(lambda evt: listeningAnimation())
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition_async()
    while not done:
        time.sleep(.5)
    
def listen():
    
    # listens for speech
    while True:

        try:

            playsound('start.mp3', False)
            recognize()
        
        except SystemError:
            print("keystroke exit")
        
def wait_for_key(key):
    
    while True:  # making a loop
        if keyboard.is_pressed(key):  # if key is pressed
            break  # finishing the loop

def main():
    
    # loads env variables file
    load_dotenv()
    
    ### AUTH KEYS ###

    AZURE_SPEECH_KEY = os.getenv("AZURE") #AZURE
    OAI_API_KEY = os.getenv("YOUR_API_KEY") #OPENAI
    openai.api_key=OAI_API_KEY #OPEN AI INIT

    # configs tts
    global speech_config; speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region="eastus")

    # sets tts sample rate
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Raw48Khz16BitMonoPcm)
    
    global stt_language, tts_voice
    
    speech_config.speech_recognition_language=stt_language
    speech_config.speech_synthesis_voice_name=tts_voice

    # sets voice
    global voice; voice = speech_config.speech_synthesis_voice_name
    global primary_language; primary_language = speech_config.speech_recognition_language
    global languages; languages = ["en-US","zh-CN"]

    #language_config = speechsdk.AutoDetectSourceLanguageConfig(languages=languages)
    global stt_config; stt_config = speechsdk.audio.AudioConfig(use_default_microphone=True) # microphone device stt # stream from here?
    global tts_config; tts_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True) # speaker device tts
    
    #global speech_recognizer; speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=stt_config, auto_detect_source_language_config=language_config) # inits stt for auto multi detection languages
    global speech_recognizer; speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=stt_config, language=stt_language) # inits stt for one detection language
    
    global style; style = "hopeful" # ssml style for voice
    global rate; rate = "1.15" # speaking rate/speed
    # sets up identifiers for conversation
    global bot; bot = "Iva"
    global patient; patient = "Bash Gutierrez"
    # chart json
    global time_current; time_current = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    ### SETUP VARIABLES ###
    global context; context = "" # concatenates message history for re-insertion with every prompt
    global messages; messages = [] # stores separate messages in list to be concatenated
    global silence_count; silence_count = 0 # counts number of no prompt
    global current_requests; current_requests = [] # stores recognized commands
    global command_prompt; command_prompt = "\n\n----------------COMMANDS-------------------\n\nWhen "+patient+" has a request or need that falls strictly under the COMMANDS list below, you alert the care team by inserting the exact command and it's parameter/reason between brackets within a message.\n\n[PATIENT REQUESTS NURSE: PARAMETER REASON]\n[BED ASSIST: PARAMETER REASON]\n[BATHROOM ASSIST: PARAMETER REASON]\n[DRESS ASSIST: PARAMETER REASON]\n[PAIN REQUEST: PARAMETER REASON]\n[FOOD REQUEST: PARAMETER REASON]\n[FLUID REQUEST: PARAMETER REASON]\n\n[CHANGE ROOM TEMPERATURE: TEMPERATURE]\n[LIGHT: ON/OFF]\n[PRIVACY FILTER: ON/OFF]"
    global chart; chart = str(get_chart())
    
    print("\nvia-bedside\n\npress the space key to continue...\n")
    wait_for_key('space')

    listen()
    
if __name__ == '__main__':
    main()