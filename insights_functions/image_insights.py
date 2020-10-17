import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cloud_connection import vision, database, max_window
import json

def analyze_image(user_id, image_file):
    if image_file is None:
        with open('./test.jpg', 'rb') as test_file:
            content = test_file.read()
    else:
        content = image_file.read()

    response = vision().face_detection({
        'content': content
    })

    emotions = {
        'joy': response.face_annotations[0].joy_likelihood,
        'sorrow': response.face_annotations[0].sorrow_likelihood,
        'anger': response.face_annotations[0].anger_likelihood,
        'surprise': response.face_annotations[0].surprise_likelihood
    }

    joy = list()
    sorrow = list()
    anger = list()
    surprise = list()

    # Get the user's emotions
    ref = database().collection('biometrics').document(user_id)
    document = ref.get()

    # If the user exists, update existing records
    if document.exists:
        data = document.to_dict()
        if 'joy' in data:
            joy = data['joy']
        if 'sorrow' in data:
            sorrow = data['sorrow']
        if 'anger' in data:
            anger = data['anger']
        if 'surprise' in data:
            surprise = data['surprise']

    joy.append(int(response.face_annotations[0].joy_likelihood))
    sorrow.append(int(response.face_annotations[0].sorrow_likelihood))
    anger.append(int(response.face_annotations[0].anger_likelihood))
    surprise.append(int(response.face_annotations[0].surprise_likelihood))

    max_seconds = max_window()
    if len(joy) > max_seconds:
        joy = joy[len(joy)  - max_seconds:]

    if len(sorrow) > max_seconds:
        sorrow = sorrow[len(sorrow)  - max_seconds:]

    if len(anger) > max_seconds:
        anger = anger[len(anger)  - max_seconds:]

    if len(surprise) > max_seconds:
        surprise = surprise[len(surprise)  - max_seconds:]

    if document.exists:
        ref.update({
            'joy': joy,
            'sorrow': sorrow,
            'anger': anger,
            'surprise': surprise
        })
    else:
        ref.set({
            'joy': joy,
            'sorrow': sorrow,
            'anger': anger,
            'surprise': surprise
        })   

    print('Updated emotion data:')
    print(f'Joy Len: {len(joy)}')
    print(f'Sorrow Len: {len(sorrow)}')
    print(f'Anger Len: {len(anger)}')
    print(f'Surprise Len: {len(surprise)}')
    
    return json.dumps(emotions), 200

if __name__ == '__main__':
    print(analyze_image('test_id', None))