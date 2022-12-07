from pprint import pformat
import json

# Open the JSON file
with open('patient.json') as json_file:
    
    # Load the data from the JSON file
    patient = json.load(json_file)

patient = patient["CHART"]

patient_formatted = pformat(
    patient,
    indent=0,
    width=80,
    compact=False,
)

chars_to_remove = ["'"]
for char in chars_to_remove:
    patient_formatted = patient_formatted.replace(char, "")

print(patient_formatted)
