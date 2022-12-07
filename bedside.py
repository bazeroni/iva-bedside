import keyboard
import os
import re
import time
import json
import openai
import azure.cognitiveservices.speech as speechsdk
from pprint import pformat
from dotenv import load_dotenv
from playsound import playsound

# loads env variables file
load_dotenv()

### AUTH KEYS ###

AZURE_SPEECH_KEY = os.getenv("AZURE") #AZURE
OAI_API_KEY = os.getenv("YOUR_API_KEY") #OPENAI
openai.api_key=OAI_API_KEY #OPEN AI INIT

# configs tts
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region="eastus")

## STT LANGUAGES ##

speech_config.speech_recognition_language="en-US"

#speech_config.speech_recognition_language="es-US"
#speech_config.speech_recognition_language="es-MX"
#speech_config.speech_recognition_language="es-PR"
#speech_config.speech_recognition_language="es-DO"
#speech_config.speech_recognition_language="es-SV"
#speech_config.speech_recognition_language="es-CU"

#speech_config.speech_recognition_language="yue-CN"
#speech_config.speech_recognition_language="zh-CN"

#speech_config.speech_recognition_language="vi-VN"

#speech_config.speech_recognition_language="ru-RU"

#speech_config.speech_recognition_language="ar-EG"
#speech_config.speech_recognition_language="ar-SY"
#speech_config.speech_recognition_language="ar-MA"

#speech_config.speech_recognition_language="fr-FR"

#speech_config.speech_recognition_language="km-KH"

#speech_config.speech_recognition_language="it-IT"

#speech_config.speech_recognition_language="fil-PH"

#speech_config.speech_recognition_language="ja-JP"

## TTS LANGUAGES ##
# other than Aria, style compatible (-empathetic) with Davis, Guy, Jane, Jason, Jenny, Nancy, Tony

# ENGLISH #
#speech_config.speech_synthesis_voice_name='en-US-NancyNeural'
#speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
speech_config.speech_synthesis_voice_name='en-US-AriaNeural'
#speech_config.speech_synthesis_voice_name='en-US-JennyMultilingualNeural'

# SPANISH #
#speech_config.speech_synthesis_voice_name='es-US-PalomaNeural' # united states
#speech_config.speech_synthesis_voice_name='es-MX-CarlotaNeural' # mexican
#speech_config.speech_synthesis_voice_name='es-PR-KarinaNeural' # puerto rican
#speech_config.speech_synthesis_voice_name='es-DO-RamonaNeural' # dominican
#speech_config.speech_synthesis_voice_name='es-SV-LorenaNeural' # salvadorean
#speech_config.speech_synthesis_voice_name='es-CU-BelkysNeural' # cuban

# CHINESE #
#speech_config.speech_synthesis_voice_name='yue-CN-XiaoMinNeural' # cantonese
#speech_config.speech_synthesis_voice_name='zh-CN-XiaochenNeural' # mandarin

# VIETNAMESE #
#speech_config.speech_synthesis_voice_name='vi-VN-HoaiMyNeural'

# RUSSIAN #
#speech_config.speech_synthesis_voice_name='ru-RU-DariyaNeural'

# ARABIC #
#speech_config.speech_synthesis_voice_name='ar-EG-SalmaNeural' # egyptian
#speech_config.speech_synthesis_voice_name='ar-SY-AmanyNeural' # syrian
#speech_config.speech_synthesis_voice_name='ar-MA-MounaNeural' # moroccan

# FRENCH #
#speech_config.speech_synthesis_voice_name='fr-FR-BrigitteNeural'

# KHMER #
#speech_config.speech_synthesis_voice_name='km-KH-SreymomNeural'

# ITALIAN #
#speech_config.speech_synthesis_voice_name='it-IT-ElsaNeural'

# TAGALOG #
#speech_config.speech_synthesis_voice_name='fil-PH-BlessicaNeural'

# JAPANESE #
#speech_config.speech_synthesis_voice_name='ja-JP-MayuNeural'

# sets voice
voice = speech_config.speech_synthesis_voice_name

# sets tts sample rate
speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Raw48Khz16BitMonoPcm)

stt_config = speechsdk.audio.AudioConfig(use_default_microphone=True) # microphone device stt
tts_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True) # speaker device tts

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=stt_config) # inits stt
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=tts_config) # inits tts

style = "hopeful" # ssml style for voice
rate = "1.25" # speaking rate/speed

# sets up identifiers for conversation
bot = "Iva"
patient = "Bash Gutierrez"

### bedside variables ###

## basic info
dob = "03-22-95"
age = "27"
weight = "63 kg"
height = "180.3 cm"
address_street = "2744 Mifflin St"
address_city = "Philadelphia"
address_state = "PA"
zipcode = "19145"
phone = "215-301-1665"
language_primary = speech_config.speech_recognition_language

## case info
#date_current = "11-30-22"
#time_current = "12:23 AM"
zone = "Tioga Pavilion (Zone A)"
floor = "3 West"
room_number = "A-315"
#room_temperature = "73.4 F (Only patient/nurse adjustable through button on TV remote)"
date_admitted = "11-22-22"
date_discharge = "12-10-22"

## vitals
blood_pressure = "125/90 mmHg"
pulse = "77 bpm"
temperature = "97.9 F"
respiratory_rate = "16 breaths/min"
oxygen_saturation = "96%"

## precautions
last_pain_med = "11-29-22 07:15 AM"
next_pain_med = "11-30-22 07:15 AM"
restrict_mobility = "Yes, bed rest"
restrict_fluid = "Yes, fluid restriction, please see nurse"
restrict_diet = "Yes, nothing by mouth after midnight (NPO)"
fall_risk = "Yes, call for assistance"
isolation = "Yes, visitors must follow isolation instructions"
covid = "Negative"

## previous medical history
conditions = ""
surgeries = ""
hospitalizations = ""

## allergies
allergies = "-Peanut\n-Shellfish\n-Penicillin"

## medications
medications = "-Amoxicillin\n-Ibuprofen"

## test results
blood_work = ""
imaging_scans = ""
diagnostic_tests = ""

## reason for admission
admission_reason = "-Suspected pneumonia"

## assessment
assessment = "-Chest X-ray shows infiltrates in the lower lobes of the lungs\n-Cough with yellow sputum production\n-Shortness of breath"

## treatment plan
treatment_plan = "-Administer intravenous antibiotics\n-Administer oxygen therapy\n-Monitor vital signs and oxygen saturation levels\n-Encourage deep breathing and coughing exercises"

## follow-up
follow_up = "-Repeat chest X-ray in 48 hours\n-Consult with pulmonologist for further management"

## discharge plan
discharge_plan = "-Prescribe oral antibiotics for 7-10 days\n-Follow up with primary care physician in 1 week\n-Recommend influenza vaccine to prevent future respiratory infections"

## care team
attending_provider = "Dr. Jacksonville"
pulmonologist = "Dr. Washington"
respiratory_therapist = "Sandra"
physical_therapist = "Mary"
nurse_practitioner = "Dietra"
registered_nurse = "Maureen"
nurse_assistant = "David"

## agenda
goals = "-Rest\n-Coughing Exercises\n-Family Meeting AM"
events = "Morning: Radiology\nAfternoon: Pulmonologist"
consults = "-West Chester Radiology"
daily_message = "-\"Hey this is RN Jane. Great job today! See you tomorrow\""

## Compiled Chart ##

chart = f"----------------MEDICAL CHART-------------------\n\nPatient: {patient}\nDate of Birth: {dob}\nAge: {age}\nWeight: {weight}\nHeight: {height}\nPatient IANA Language Code: {language_primary}\n\nCurrent Date: {date_current}\nCurrent Time: {time_current}\nZone: {zone}\nFloor: {floor}\nRoom: {room_number}\nRoom Temperature: {room_temperature}\nDate Admitted: {date_admitted}\nExpected Discharge Date: {date_discharge}\n\nALLERGIES\n{allergies}\n\nMEDICATIONS\n{medications}\n\nREASON FOR ADMISSION\n{admission_reason}\n\nASSESSMENT\n{assessment}\n\nTREATMENT PLAN\n{treatment_plan}\n\nFOLLOW-UP\n{follow_up}\n\nDISCHARGE PLAN\n{discharge_plan}\n\nCONDITIONS AND PRECAUTIONS\nLast Pain Medication: {last_pain_med}\nNext Pain Medication: {next_pain_med}\nMobility Restriction: {restrict_mobility}\nFluid Restriction: {restrict_fluid}\nDiet Restriction: {restrict_diet}\nFall Risk: {fall_risk}\nIsolation: {isolation}\n\nVITALS\nBP: {blood_pressure}\nHR: {pulse}\nRR: {respiratory_rate}\nTemp: {temperature}\nO2: {oxygen_saturation}\n\nCARE TEAM\nAttending Provider: {attending_provider}\nPulmonologist: {pulmonologist}\nRespiratory Therapist: {respiratory_therapist}\nPhysical Therapist: {physical_therapist}\nNurse Practitioner: {nurse_practitioner}\nRegistered Nurse: {registered_nurse}\nNurse Assistant: {nurse_assistant}\n\nGOALS / PLAN FOR THE DAY\n{goals}\n\nUPCOMING EVENTS\n{events}\n\nUPCOMING CONSULTS\n{consults}\n\nPREVIOUS SHIFT MESSAGES TO PATIENT\n{daily_message}\n\n----------------COMMANDS-------------------\n\nFor each request that "+patient+" needs, alert the care team by inserting the exact matching command and it's details to replace between brackets within a message.\n\n[BED ASSIST: (DETAILS TO REPLACE)]\n[BATHROOM ASSIST: (DETAILS TO REPLACE)]\n[DRESS ASSIST: (DETAILS TO REPLACE)]\n[PAIN REQUEST: (DETAILS TO REPLACE)]\n[FOOD REQUEST: (DETAILS TO REPLACE)]\n[FLUID REQUEST: (DETAILS TO REPLACE)]\n[NURSE CALL: (DETAILS TO REPLACE)]\n\n----------------START OF CHAT-------------------\n"

### SETUP VARIABLES ###
context = "" # concatenates message history for re-insertion with every prompt
messages = [] # stores separate messages in list to be concatenated
silence_count = 0 # counts number of no prompt
current_requests = [] # stores recognized commands

def concatenate_context():
    
    global messages
    global context
    
    if len(messages) == 3:
        messages.pop()
        
    #print(len(messages))
        
    for message in messages:
        context += message

# inputs and reads patient prompt
# responds with given style from TONE_GPT3()
# returns response
def chat_gpt3(zice):
    
    start_time = time.time()
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt= "You are, "+bot+", a clinical bedside intelligent virtual assistant at Trinity University Hospital for a patient named "+patient+". Speak to "+patient+" only in "+language_primary+" colloquially with patience, compassion, empathy, and assurance. The patient should be relaxed by you and the conversations you have with them. For each request that "+patient+" needs, alert the care team by inserting the exact command and it's details to replace between brackets within a message.\n\n"+chart+context+"\n"+patient+": "+zice+"\n"+bot+":",
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
    response_time = time.time() - start_time
    
    # create variables to collect the stream of events
    collected_events = []
    completion_text = ""
    print(f"{bot}:", end="")
    
    # iterate through the stream of events
    for event in response:
        event_time = time.time() - start_time  # calculate the time delay of the event
        collected_events.append(event)  # save the event response
        event_text = event['choices'][0]['text']  # extract the text
        # Encode the string using the utf-8 codec
        encoded_text = event_text.encode('utf-8')
        decoded_text = encoded_text.decode('utf-8')
        completion_text += decoded_text  # append the text
        print(decoded_text, end="")  # print the delay and text
    
    # print response time
    print(f" [{response_time:.2f} S]\n")
        
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
    
    command = request_split[0].upper()
    parameter = request_split[1].upper()
    
    match command:
        case "NURSE CALL":
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
        case default:
            playsound('call.wav', False)
            print(f"\n[{time_current}] {command}: {parameter}\n")
        

# inputs response SSML from CHAT_GPT()
# streams async synthesis
def tts(ssml):
    
    global speech_synthesis_result
    
    #speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml)
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()

def respond(prompt, response):
    
    global messages
    global silence_count
    
    response_formatted = f"{bot}:" + response

    messages.append("\n"+prompt+"\n"+response_formatted)
    
    # take out commands
    response = parse_command(response)
    
    # runs if commands are present
    if current_requests: run_command()

    # concats message to memory/history
    concatenate_context()

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

    # synthesizes TTS with input SSML
    tts(xml_string)

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
        print("\n\n"+prompt)
        
        # gets GPT text message response completion
        response = chat_gpt3(inp)
        
        respond(prompt, response)
        
        return
    
    # assumes there is no input
    # checks if has been silent for three rounds
    elif silence_count == 2:
        
        # imitates silent input
        prompt = patient+": ..."
        print("\n\n"+prompt)
        
        # gets GPT text message response completion
        response = chat_gpt3("...")
        
        respond(prompt, response)
        
        return
            
    # increases silence count
    silence_count += 1
    
def listeningAnimation():
    
    listening = "||||||||||"
    
    for character in listening:
        time.sleep(0.005)
        print(character, end="")
    
def recognize():
    
    # gets azure stt
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    #speech_recognizer.start_continuous_recognition_async()
    
    return speech_recognition_result
    
def listen():
    
    # listens for speech
    while True:

        playsound('start.mp3', False)
        
        listeningAnimation()
        
        speech_recognition_result = recognize()
        
        playsound('stop.mp3', False)

        # gets tts from azure stt
        speech_recognizer.recognized.connect(think(speech_recognition_result.text))

        #message = input(patient + ": ")
        #think(message)
        
def wait_for_key(key):
    
    while True:  # making a loop
        if keyboard.is_pressed(key):  # if key is pressed
            break  # finishing the loop

print("\nVIA-Bedside\n\nWait for the |||||||||| command and sound cue before speaking.\n\nPress the space key to continue...\n")

wait_for_key('space')

listen()