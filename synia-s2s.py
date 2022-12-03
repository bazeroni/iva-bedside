#import random
import keyboard
#import whisper
#import io
#import time
import os
import openai
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from playsound import playsound

# loads env variables file
load_dotenv()

### AUTH KEYS ###

AZURE_SPEECH_KEY = os.getenv("AZURE") #AZURE
OAI_API_KEY = os.getenv("YOUR_API_KEY") #OPENAI
openai.api_key=OAI_API_KEY #OPEN AI INIT

### AZURE ###

# configs tts
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region="eastus")

# configs stt lang
speech_config.speech_recognition_language="en-US"
#speech_config.speech_recognition_language="es-US"

# configs tts voice
# other than Aria, style compatible (-empathetic) with Davis, Guy, Jane, Jason, Jenny, Nancy, Tony

speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
#speech_config.speech_synthesis_voice_name='en-US-JennyMultilingualNeural'
#speech_config.speech_synthesis_voice_name='en-US-AIGenerate1Neural'
#speech_config.speech_synthesis_voice_name='es-MX-CarlotaNeural'

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
bot = "VBA"
patient = "Andrew Lopez"

### bedside variables ###

## basic info
dob = "03-22-95"
age = "27"
weight = "63 kg"
height = "180.3 cm"

dateCurrent = "11-30-22"
timeCurrent = "12:23 AM"
zone = "Rock Pavilion (Zone A)"
floor = "3 West"
roomNumber = "A315"
roomTemperature = "73.4 F (Only adjustable through TV remote or nurse)"
dateAdmitted = "11-22-22"
dateDischarge = "12-10-22"

## vitals
bloodPressure = "125/90 mmHg"
pulse = "77 bpm"
temperature = "97.9 F"
respiratoryRate = "16 breaths/min"
oxygenSaturation = "96%"

## conditions and precautions
lastPainMedRequest = "11-29-22 07:15 AM"
restrictMobility = "Yes, Bed Rest"
restrictFluid = "Yes, please see nurse"
restrictDiet = "Yes, Nothing by mouth after midnight (NPO)"
fallRisk = "Yes, call for assistance"
isolation = "Yes, visitors must follow isolation instructions"

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

## Compiled Chart ##

chart = f"----------------MEDICAL CHART-------------------\n\nPatient: {patient}\nDate of Birth: {dob}\nAge: {age}\nWeight: {weight}\nHeight: {height}\n\nCurrent Date: {dateCurrent}\nCurrent Time: {timeCurrent}\nZone: {zone}\nFloor: {floor}\nRoom: {roomNumber}\nRoom Temperature: {roomTemperature}\nDate Admitted: {dateAdmitted}\nExpected Discharge Date: {dateDischarge}\n\nALLERGIES\n{allergies}\n\nMEDICATIONS\n{medications}\n\nREASON FOR ADMISSION\n{reasonForAdmission}\n\nASSESSMENT\n{assessment}\n\nTREATMENT PLAN\n{treatmentPlan}\n\nFOLLOW-UP\n{followUp}\n\nDISCHARGE PLAN\n{dischargePlan}\n\nCONDITIONS AND PRECAUTIONS\nLast Pain Med Request: {lastPainMedRequest}\nMobility Restriction: {restrictMobility}\nFluid Restriction: {restrictFluid}\nDiet Restriction: {restrictDiet}\nFall Risk: {fallRisk}\nIsolation: {isolation}\n\nVITALS\nBP: {bloodPressure}\nHR: {pulse}\nRR: {respiratoryRate}\nTemp: {temperature}\nO2: {oxygenSaturation}\n\nCARE TEAM\nAttending Provider: {attendingProvider}\nPulmonologist: {pulmonologist}\nRespiratory Therapist: {respiratoryTherapist}\nPhysical Therapist: {physicalTherapist}\nNurse Practitioner: {nursePractitioner}\nRegistered Nurse: {registeredNurse}\nNurse Assistant: {nurseAssistant}\n\nGOALS / PLAN FOR THE DAY\n{goals}\n\nUPCOMING EVENTS\n{events}\n\nUPCOMING CONSULTS\n{consults}\n\nPREVIOUS SHIFT MESSAGES TO PATIENT\n{dailyMessage}\n\n----------------START OF CHAT-------------------\n"

### SETUP VARIABLES ###
# concats message history for re-insertion with every prompt
context = ""
messages = []
# last response from GPT
raspuns = ""
raspunsF = ""
# holds emotional response chosen by GPT-3
style = ""
# counts number of times patient silence for input
silenceCount = 0
# counts number of messages in conversation history 
messageCount = 0

""" TONE_GPT3()
1. inputs and reads patient prompt
3. chooses emotional response from given list of styles: friendly, empathetic, cheerful, excited, hopeful, sad
2. returns style/emotion
"""
def tone_gpt3(zice):
    toneLabel = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Read the following interaction, then pick just one of the emotions for "+bot+" to respond to "+patient+" with from this list only: [friendly, empathetic, cheerful, excited, hopeful, sad].\n"+bot+": "+raspuns+"\n"+patient+": "+zice+"\n\nEmotion: [",
        temperature=0.0,
        max_tokens=12,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=[patient+":", bot+":", "Emotion: [", ","],
        echo=False,
    )
    return toneLabel

# Define a callback function that will be called
# whenever a key is pressed
def on_key_press(key):
    # Print the character that was pressed
    print("You pressed: ", key.name)

    input = input(patient + ": ")

    textSpeech(input)

def concatContext():
    
    global messages
    global context
    
    if len(messages) == 6:
        messages.pop()
        
    #print(len(messages))
        
    for message in messages:
        context += message

""" CHAT_GPT3()
1. inputs and reads patient prompt
2. responds with given style from TONE_GPT3()
3. returns response
"""
def chat_gpt3(zice):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt= "You are, "+bot+", a virtual bedside assistant at Temple University Hospital for a patient named "+patient+". Kindly instruct the patient to press their nurse call button when needed.\n\n"+chart+context+"\n"+patient+": "+zice+"\n"+bot+" ["+style+"]:",
        temperature=1.0,
        max_tokens=512,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=[patient+":", bot+":", "["],
        echo=False,
    )
    return response

""" TTS()
1. inputs response SSML from CHAT_GPT()
2. streams async synthesis
"""
def tts(ssml):
    global speech_synthesis_result
    #speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml)
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()
    
# given input stt
# generates style and response from GPT-3
# synthesizes response tts
def textSpeech(inp):
    
    inp.encode("utf-8")
    
    # parses and formats patient input
    prompt = patient+": "+inp

    # global counter and helper variables
    global silenceCount
    global context
    global style
    global raspuns
    global raspunsF
    global done

    # processes non-silent interaction
    if inp != "":
        
        # prints status
        #print("NON-SILENCE")
        print(prompt)

        # gets style GPT would like to respond with
        style = ((tone_gpt3(inp)).choices[0].text).split("]")[0]
        #print(style)

        # gets GPT text message response completion
        raspuns = (chat_gpt3(inp)).choices[0].text
        
        # formats raspuns
        raspunsF = bot+" ["+style+"]: " + raspuns
        #raspunsF = bot+": "+raspuns

        # prints raspuns
        print(raspunsF)
        #print(raspuns)
        
        messages.append("\n"+prompt+"\n"+raspunsF)

        # concats message to memory/history
        concatContext()

        # SSML for TTS with response and style
        xmlString = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
        xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="'''+voice+'''">
        <prosody rate="medium">
        <mstts:express-as style="'''+style+'''" styledegree="0.5">
        '''+ raspuns +'''
        </mstts:express-as>
        </prosody>
        </voice>
        </speak>'''

        # synthesizes TTS with input SSML
        tts(xmlString)

        # resets silence count to 0
        silenceCount = 0

        # marks interaction
        done = True

    # processes silent interaction
    else:

        # checks if patient has been silent for certain amount of time
        if silenceCount == 2:
            
            # imitates silent input
            prompt = patient+": ..."

            # prints status
            #print("SILENCE PROMPT")
            print(prompt)

            # gets style GPT would like to respond with
            style = ((tone_gpt3("...")).choices[0].text).split("]")[0]
            #print(style)

            # gets GPT text message response completion
            raspuns = (chat_gpt3("...")).choices[0].text

            # formats raspuns
            raspunsF = bot+" ["+style+"]: " + raspuns
            #raspunsF = bot+": "+raspuns

            # prints raspuns
            print(raspunsF)

            messages.append("\n"+prompt+"\n"+raspunsF)

            # concats message to memory/history
            concatContext()

            # SSML for TTS with response and style
            xmlString = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
            xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
            <voice name="'''+voice+'''">
            <prosody rate="medium">
            <mstts:express-as style="'''+style+'''" styledegree="0.5">
            '''+ raspuns +'''
            </mstts:express-as>
            </prosody>
            </voice>
            </speak>'''

            # synthesizes TTS with input SSML
            tts(xmlString)

            # resets silence count to 0
            silenceCount = 0

            # marks interaction
            done = True

        # increases silence count
        #print("SILENCE")
        silenceCount += 1
        
def listen():
    
    global done
    
    # listens for speech
    while not done:
        
        print("\n|||||||||| LISTENING ||||||||||\n")
        playsound('start.mp3', False)
        
        # gets azure stt
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        #speech_recognizer.start_continuous_recognition_async()

        playsound('stop.mp3', False)

        # gets tts from azure stt
        speech_recognizer.recognized.connect(textSpeech(speech_recognition_result.text))

        # Start listening for keystrokes
        #keyboard.on_press(on_key_press)
    """

    while not done:

        message = input(patient + ": ")

        textSpeech(message)
    """
    

while (True):

    try:
        
        # controls whether interaction has been recieved and processed or not
        done = False
        
        print("\nPress the space key to continue...")
        
        while True:  # making a loop
            if keyboard.is_pressed('space'):  # if key 'space' is pressed 
                break  # finishing the loop
        
        listen()

    # excepts if not understood
    except Exception as e:
        print("Could not understand", e)