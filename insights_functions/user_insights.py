import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cloud_connection import database
import json

def get_data(user_id):
    # Get the user's biometrics
    ref = database().collection('biometrics').document(user_id)
    document = ref.get()

    if document.exists:
        return json.dumps(document.to_dict()), 200
    else:
        return 'No user found', 400

if __name__ == '__main__':
    print(get_data('test_id'))