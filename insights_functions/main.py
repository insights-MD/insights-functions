import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from image_insights import analyze_image
from speech_insights import analyze_speech
from biometrics_insights import analyze_biometrics
from user_insights import get_data

def upload_image(request):
    """
    Request: Multipart Form Request
    """

    user_id = request.form['userId']
    image_file = request.files['image']
    filestream = image_file.stream
    filestream.seek(0)

    return analyze_image(user_id, filestream)

def upload_biometrics(request):
    """
    Request: JSON body
    """

    request_json = request.get_json()
    user_id = request_json['userId']
    biometric_data = request_json['data']

    return analyze_biometrics(user_id, biometric_data)

def get_speech_insights(request):
    """
    Request: Multipart Form Request
    """

    user_id = request.form['userId']
    wav_file = request.files['audio']
    filestream = wav_file.stream
    filestream.seek(0)

    return analyze_speech(user_id, filestream)

def get_user_data(request):
    """
    Request: JSON body
    """

    request_json = request.get_json()
    user_id = request_json['userId']

    return get_data(user_id)