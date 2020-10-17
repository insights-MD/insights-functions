# insights-functions
Cloud functions for insights-md

## Installation
- pyenv install 3.8.2
- pyenv local 3.8.2
- poetry install
- poetry shell

## Deploying Functions
gcloud functions deploy upload_image --entry-point upload_image --runtime python38 --trigger-http --allow-unauthenticated
gcloud functions deploy get_speech_insights --entry-point get_speech_insights --runtime python38 --trigger-http --allow-unauthenticated
gcloud functions deploy upload_biometrics --entry-point upload_biometrics --runtime python38 --trigger-http --allow-unauthenticated
gcloud functions deploy get_user_data --entry-point get_user_data --runtime python38 --trigger-http --allow-unauthenticated
