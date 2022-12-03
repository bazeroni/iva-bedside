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
roomTemperature = "73.4 F"
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
diet = "Nothing by mouth after midnight"
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

chart = f"----------------"+patient.upper()+"'S CHART-------------------\nPatient: {patient}\nDate of Birth: {dob}\nAge: {age}\nWeight: {weight}\nHeight: {height}\n\nCurrent Date: {dateCurrent}\nCurrent Time: {timeCurrent}\nZone: {zone}\nFloor: {floor}\nRoom: {roomNumber}\nRoom Temperature: {roomTemperature}\nDate Admitted: {dateAdmitted}\nExpected Discharge Date: {dateDischarge}\n\nALLERGIES\n{allergies}\n\nMEDICATIONS\n{medications}\n\nREASON FOR ADMISSION\n{reasonForAdmission}\n\nASSESSMENT\n{assessment}\n\nTREATMENT PLAN\n{treatmentPlan}\n\nFOLLOW-UP\n{followUp}\n\nDISCHARGE PLAN\n{dischargePlan}\n\nCONDITIONS AND PRECAUTIONS\nLast Pain Med Request: {lastPainMedRequest}\nMobility Restriction: {restrictMobility}\nFluid Restriction: {restrictFluid}\nDiet: {diet}\nFall Risk: {fallRisk}\nIsolation: {isolation}\n\nVITALS\nBP: {bloodPressure}\nHR: {pulse}\nRR: {respiratoryRate}\nTemp: {temperature}\nO2: {oxygenSaturation}\n\nCARE TEAM\nAttending Provider: {attendingProvider}\nPulmonologist: {pulmonologist}\nRespiratory Therapist: {respiratoryTherapist}\nPhysical Therapist: {physicalTherapist}\nNurse Practitioner: {nursePractitioner}\nRegistered Nurse: {registeredNurse}\nNurse Assistant: {nurseAssistant}\n\nGOALS / PLAN FOR THE DAY\n{goals}\n\nUPCOMING EVENTS\n{events}\n\nUPCOMING CONSULTS\n{consults}\n\nPREVIOUS SHIFT MESSAGES TO PATIENT\n{dailyMessage}\n\n----------------START OF CHAT-------------------\n"

print(chart)