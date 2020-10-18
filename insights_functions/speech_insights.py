import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cloud_connection import speech, language, database

def analyze_speech(user_id, audio_file):
    speech_client, RecognitionAudio, RecognitionConfig = speech()

    if audio_file is None:
        with open('./test.wav', 'rb') as test_file:
            content = test_file.read()
    else:
        content = audio_file.read()

    audio = RecognitionAudio(content = content)
    config = RecognitionConfig(encoding = RecognitionConfig.AudioEncoding.LINEAR16,
        language_code = 'en-US')

    response = speech_client.recognize(config = config, audio = audio)

    str_list = list()
    for result in response.results:
        str_list.append(result.alternatives[0].transcript)

    text = ''.join(str_list)
    
    language_client, document = language(text)
    response = language_client.analyze_entities(document = document, encoding_type = 'UTF32')

    entities = set()

    # Get the user's keywords
    ref = database().collection('biometrics').document(user_id)
    document = ref.get()

    # If the user exists, update existing records
    if document.exists:
        data = document.to_dict()
        if 'keywords' in data:
            entities = set(data['keywords'])

    for entity in response.entities:
        entities.add(entity.name)

    if document.exists:
        ref.update({
            'keywords': list(entities)
        })
    else:
        ref.set({
            'keywords': list(entities)
        })

    return str(entities), 200

if __name__ == '__main__':
    print(analyze_speech(None))