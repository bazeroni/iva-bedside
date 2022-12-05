import keyboard
import os
import re
import time
import openai
import azure.cognitiveservices.speech as speechsdk
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

style = "Friendly"

# ENGLISH #
speech_config.speech_synthesis_voice_name='en-US-NancyNeural'
#speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
#speech_config.speech_synthesis_voice_name='en-US-AriaNeural'
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

# microphone device stt 
stt_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
# speaker device tts
tts_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# inits stt
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=stt_config)
# inits tts
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=tts_config)

# sets up identifiers for conversation
bot = "IVA"
patient = "Juan Lopez"

### bedside variables ###

## basic info
dob = "03-22-95"
age = "27"
weight = "63 kg"
height = "180.3 cm"
primaryLanguage = speech_config.speech_recognition_language

dateCurrent = "11-30-22"
timeCurrent = "12:23 AM"
zone = "Tioga Pavilion (Zone A)"
floor = "3 West"
roomNumber = "A-315"
roomTemperature = "73.4 F (Only patient/nurse adjustable through button on TV remote)"
dateAdmitted = "11-22-22"
dateDischarge = "12-10-22"

## vitals
bloodPressure = "125/90 mmHg"
pulse = "77 bpm"
temperature = "97.9 F"
respiratoryRate = "16 breaths/min"
oxygenSaturation = "96%"

## conditions and precautions
lastPainMed = "11-29-22 07:15 AM"
nextPainMed = "11-30-22 07:15 AM"
restrictMobility = "Yes, bed rest"
restrictFluid = "Yes, fluid restriction, please see nurse"
restrictDiet = "Yes, nothing by mouth after midnight (NPO)"
fallRisk = "Yes, call for assistance"
isolation = "Yes, visitors must follow isolation instructions"
covid = "No"

## allergies
allergies = "-Peanut\n-Shellfish\n-Penicillin"

## medications
medications = "-Amoxicillin\n-Ibuprofen"

## reason for admission
reasonForAdmission = "-Suspected pneumonia"

## assessment
assessment = "-Chest X-ray shows infiltrates in the lower lobes of the lungs\n-Cough with yellow sputum production\n-Shortness of breath"

## treatment plan
treatmentPlan = "-Administer intravenous antibiotics\n-Administer oxygen therapy\n-Monitor vital signs and oxygen saturation levels\n-Encourage deep breathing and coughing exercises"

## follow-up
followUp = "-Repeat chest X-ray in 48 hours\n-Consult with pulmonologist for further management"

## discharge plan
dischargePlan = "-Prescribe oral antibiotics for 7-10 days\n-Follow up with primary care physician in 1 week\n-Recommend influenza vaccine to prevent future respiratory infections"

## care team
attendingProvider = "Dr. Jacksonville"
pulmonologist = "Dr. Washington"
respiratoryTherapist = "Sandra"
physicalTherapist = "Mary"
nursePractitioner = "Dietra"
registeredNurse = "Maureen"
nurseAssistant = "David"

## agenda
goals = "-Rest\n-Coughing Exercises\n-Family Meeting AM"
events = "Morning: Radiology\nAfternoon: Pulmonologist"
consults = "-West Chester Radiology"
dailyMessage = "-\"Hey this is RN Jane. Great job today! See you tomorrow\""

## commands
currentRequests = []

## Compiled Chart ##

chart = f"----------------MEDICAL CHART-------------------\n\nPatient: {patient}\nDate of Birth: {dob}\nAge: {age}\nWeight: {weight}\nHeight: {height}\nPatient IANA Language Code: {primaryLanguage}\n\nCurrent Date: {dateCurrent}\nCurrent Time: {timeCurrent}\nZone: {zone}\nFloor: {floor}\nRoom: {roomNumber}\nRoom Temperature: {roomTemperature}\nDate Admitted: {dateAdmitted}\nExpected Discharge Date: {dateDischarge}\n\nALLERGIES\n{allergies}\n\nMEDICATIONS\n{medications}\n\nREASON FOR ADMISSION\n{reasonForAdmission}\n\nASSESSMENT\n{assessment}\n\nTREATMENT PLAN\n{treatmentPlan}\n\nFOLLOW-UP\n{followUp}\n\nDISCHARGE PLAN\n{dischargePlan}\n\nCONDITIONS AND PRECAUTIONS\nLast Pain Medication: {lastPainMed}\nNext Pain Medication: {nextPainMed}\nMobility Restriction: {restrictMobility}\nFluid Restriction: {restrictFluid}\nDiet Restriction: {restrictDiet}\nFall Risk: {fallRisk}\nIsolation: {isolation}\n\nVITALS\nBP: {bloodPressure}\nHR: {pulse}\nRR: {respiratoryRate}\nTemp: {temperature}\nO2: {oxygenSaturation}\n\nCARE TEAM\nAttending Provider: {attendingProvider}\nPulmonologist: {pulmonologist}\nRespiratory Therapist: {respiratoryTherapist}\nPhysical Therapist: {physicalTherapist}\nNurse Practitioner: {nursePractitioner}\nRegistered Nurse: {registeredNurse}\nNurse Assistant: {nurseAssistant}\n\nGOALS / PLAN FOR THE DAY\n{goals}\n\nUPCOMING EVENTS\n{events}\n\nUPCOMING CONSULTS\n{consults}\n\nPREVIOUS SHIFT MESSAGES TO PATIENT\n{dailyMessage}\n\n----------------COMMANDS-------------------\n\nFor each request that "+patient+" needs, alert the care team by inserting the exact matching command and it's details to replace between brackets within a message.\n\n[BED ASSIST: (DETAILS TO REPLACE)]\n[BATHROOM ASSIST: (DETAILS TO REPLACE)]\n[DRESS ASSIST: (DETAILS TO REPLACE)]\n[PAIN REQUEST: (DETAILS TO REPLACE)]\n[FOOD REQUEST: (DETAILS TO REPLACE)]\n[FLUID REQUEST: (DETAILS TO REPLACE)]\n[NURSE CALL: (DETAILS TO REPLACE)]\n\n----------------START OF CHAT-------------------\n"

### SETUP VARIABLES ###
# concatenates message history for re-insertion with every prompt
context = ""
# stores separate messages in list to be concatenated
messages = []
silenceCount = 0

# Define a callback function that will be called
# whenever a key is pressed
def on_key_press(key):
    # Print the character that was pressed
    print("You pressed: ", key.name)

    input = input(patient + ": ")

    think(input)

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
        prompt= "You are, "+bot+", a clinical bedside intelligent virtual assistant (IVA) at Trinity University Hospital for a patient named "+patient+". Speak to "+patient+" only in "+primaryLanguage+" with patience, compassion, empathy, and assurance. Keep the patient company and have conversations with them. For each request that "+patient+" needs, alert the care team by inserting the exact command and it's details to replace between brackets within a message.\n\n"+chart+context+"\n"+patient+": "+zice+"\n"+bot+":",
        #prompt= "You are, "+bot+", a clinical bedside intelligent virtual assistant (IVA) at Trinity University Hospital for a patient named "+patient+". Speak to "+patient+" only in "+primaryLanguage+" with patience, empathy, and assurance. Keep the patient company and have conversations with them. Kindly instruct the patient to press their nurse call button on their TV remote when needed.\n\n"+chart+context+"\n"+patient+": "+zice+"\n"+bot+":",
        temperature=0.7,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=2.0,
        presence_penalty=2.0,
        stop=[patient+":", bot+":"],
        echo=False,
        stream=True,
    )
    responseTime = time.time() - start_time
    
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
    print(f" [{responseTime:.2f} S]\n")
        
    return completion_text

def parse_command(text):
    
    global currentRequests
    
    # strips tts text of commands
    textClean = re.sub(r'\[.*?\]', '', text)
    
    # compile regular expression pattern to match contents of brackets '[]'
    pattern = re.compile(r'\[(.*?)\]')
    
    # find all occurrences of pattern in string and save as list
    currentRequests = pattern.findall(text)
    
    return textClean

def run_command():
    
    global currentRequests
    
    requestSplit = currentRequests[0].split(":")
    
    command = requestSplit[0].upper()
    parameter = requestSplit[1].upper()
    
    match command:
        case "NURSE CALL":
            playsound('call.wav', False)
            print(f"\n[{timeCurrent}] {command}: {parameter}\n")
        case "BED ASSIST":
            playsound('call.wav', False)
            print(f"\n[{timeCurrent}] {command}: {parameter}\n")
        case "BATHROOM ASSIST":
            playsound('call.wav', False)
            print(f"\n[{timeCurrent}] {command}: {parameter}\n")
        case "DRESS ASSIST":
            playsound('call.wav', False)
            print(f"\n[{timeCurrent}] {command}: {parameter}\n")
        case "PAIN REQUEST":
            playsound('call.wav', False)
            print(f"\n[{timeCurrent}] {command}: {parameter}\n")
        case "FOOD REQUEST":
            playsound('call.wav', False)
            print(f"\n[{timeCurrent}] {command}: {parameter}\n")
        case "FLUID REQUEST":
            playsound('call.wav', False)
            print(f"\n[{timeCurrent}] {command}: {parameter}\n")
        case default:
            playsound('call.wav', False)
            print(f"\n[{timeCurrent}] {command}: {parameter}\n")
        

# inputs response SSML from CHAT_GPT()
# streams async synthesis
def tts(ssml):
    
    global speech_synthesis_result
    
    #speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml)
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()

def respond(prompt, response):
    
    global messages
    global silenceCount
    
    responseFormatted = f"{bot}:" + response

    messages.append("\n"+prompt+"\n"+responseFormatted)
    
    # take out commands
    response = parse_command(response)
    
    # runs if commands are present
    if currentRequests: run_command()

    # concats message to memory/history
    concatenate_context()

    # SSML for TTS with response and style
    xmlString = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
    xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="'''+voice+'''">
    <prosody rate="medium">
    <mstts:express-as style="'''+style+'''" styledegree="2">
    '''+ response +'''
    </mstts:express-as>
    </prosody>
    </voice>
    </speak>'''

    # synthesizes TTS with input SSML
    tts(xmlString)

    # resets silence count to 0
    silenceCount = 0

# given input stt
# generates style and response from GPT-3
# synthesizes response tts
def think(inp):
    
    global silenceCount
    
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
    elif silenceCount == 2:
        
        # imitates silent input
        prompt = patient+": ..."
        print("\n\n"+prompt)
        
        # gets GPT text message response completion
        response = chat_gpt3("...")
        
        respond(prompt, response)
        
        return
            
    # increases silence count
    silenceCount += 1
    
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