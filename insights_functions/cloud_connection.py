from google.cloud import firestore
from google.cloud.vision import ImageAnnotatorClient
from google.cloud.speech import SpeechClient, RecognitionAudio, RecognitionConfig
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

service_account_name = './service_account.json'
db = firestore.Client.from_service_account_json(service_account_name)
vision_client = ImageAnnotatorClient.from_service_account_json(service_account_name)
speech_client = SpeechClient.from_service_account_json(service_account_name)
language_client = language.LanguageServiceClient.from_service_account_json(service_account_name)

def max_window():
    return 60
    
def database():
    return db

def vision():
    return vision_client

def speech():
    return speech_client, RecognitionAudio, RecognitionConfig

def language(text):
    document = types.Document(content = text,
        type = enums.Document.Type.PLAIN_TEXT)

    return language_client, document