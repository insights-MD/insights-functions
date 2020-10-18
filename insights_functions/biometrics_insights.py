import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cloud_connection import database, max_window

def analyze_biometrics(user_id, biometrics):
    blood_oxygen = list()
    heart_rate = list()
    temperature = list()

    # Get the user's biometrics
    ref = database().collection('biometrics').document(user_id)
    document = ref.get()

    # If the user exists, update existing records
    if document.exists:
        data = document.to_dict()
        if 'SPO2' in data:
            blood_oxygen = data['SPO2']
        if 'HR' in data:
            heart_rate = data['HR']
        if 'temperature' in data:
            temperature = data['temperature']

    for scan in biometrics:
        blood_oxygen.append(int(scan['SPO2']))
        heart_rate.append(int(scan['HR'].split()[0]))
        temperature.append(int(scan['temperature'][0]))

    max_seconds = max_window()
    if len(blood_oxygen) > max_seconds:
        blood_oxygen = blood_oxygen[len(blood_oxygen)  - max_seconds:]

    if len(heart_rate) > max_seconds:
        heart_rate = heart_rate[len(heart_rate)  - max_seconds:]

    if len(temperature) > max_seconds:
        temperature = temperature[len(temperature)  - max_seconds:]

    if document.exists:
        ref.update({
            'SPO2': blood_oxygen,
            'HR': heart_rate,
            'temperature': temperature
        })
    else:
        ref.set({
            'SPO2': blood_oxygen,
            'HR': heart_rate,
            'temperature': temperature
        })

    print('Updated biometric data:')
    print(f'Blood O2 Len: {len(blood_oxygen)}')
    print(f'HR Len: {len(heart_rate)}')
    print(f'Temp Len: {len(temperature)}')

    return 'Updated Biometric Data', 200

if __name__ == '__main__':
    biometrics = [
        {
            "red": "51249",
            "ir": "31048",
            "SPO2": "96",
            "temperature": [ "90", "F" ],
            "HR": "86 B"
        },
        {
            "red": "50824",
            "ir": "31138",
            "SPO2": "95",
            "temperature": [ "91", "F" ],
            "HR": "88 B"
        }
    ]

    print(analyze_biometrics('test_id', biometrics))