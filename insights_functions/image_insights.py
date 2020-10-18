import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cloud_connection import vision, database, max_window
import json
import math

def analyze_image(user_id, image_file):
    if image_file is None:
        with open('./test.jpg', 'rb') as test_file:
            content = test_file.read()
    else:
        content = image_file.read()

    response = vision().face_detection({
        'content': content
    })

    joy = list()
    sorrow = list()
    anger = list()
    surprise = list()
    score = list()

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
        if 'emotional_index_score' in data:
            score = data['emotional_index_score']

    joy_score = int(response.face_annotations[0].joy_likelihood)
    sorrow_score = int(response.face_annotations[0].sorrow_likelihood)
    anger_score = int(response.face_annotations[0].anger_likelihood)
    surprise_score = int(response.face_annotations[0].surprise_likelihood)

    EIS = 1 / (1 + math.exp(-1 * ((joy_score - ((sorrow_score + anger_score + surprise_score) / 3)))))

    joy.append(joy_score)
    sorrow.append(sorrow_score)
    anger.append(anger_score)
    surprise.append(surprise_score)
    score.append(EIS)

    max_seconds = max_window()
    if len(joy) > max_seconds:
        joy = joy[len(joy)  - max_seconds:]

    if len(sorrow) > max_seconds:
        sorrow = sorrow[len(sorrow)  - max_seconds:]

    if len(anger) > max_seconds:
        anger = anger[len(anger)  - max_seconds:]

    if len(surprise) > max_seconds:
        surprise = surprise[len(surprise)  - max_seconds:]

    if len(score) > max_seconds:
        score = score[len(score)  - max_seconds:]

    if document.exists:
        ref.update({
            'joy': joy,
            'sorrow': sorrow,
            'anger': anger,
            'surprise': surprise,
            'emotional_index_score': score
        })
    else:
        ref.set({
            'joy': joy,
            'sorrow': sorrow,
            'anger': anger,
            'surprise': surprise,
            'emotional_index_score': score
        })

    print('Updated emotion data:')
    print(f'Joy Len: {len(joy)}')
    print(f'Sorrow Len: {len(sorrow)}')
    print(f'Anger Len: {len(anger)}')
    print(f'Surprise Len: {len(surprise)}')
    print(f'Score: {EIS}')
    
    return str(EIS), 200

if __name__ == '__main__':
    print(analyze_image('test_id', None))