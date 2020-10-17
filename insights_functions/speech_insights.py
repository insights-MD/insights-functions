import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cloud_connection import speech, language

def analyze_speech(audio_file):
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

    entities = list()
    for entity in response.entities:
        entities.append(entity.name)

    return str(entities), 200

if __name__ == '__main__':
    print(analyze_speech(None))