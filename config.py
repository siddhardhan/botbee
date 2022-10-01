import os

class DefaultConfig:
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_URL="https://sid-auth-0988.cognitiveservices.azure.com/luis/prediction/v3.0/apps/e31e2e97-ce5b-4c8a-9708-76e2fff6a00c/slots/production/predict?verbose=true&show-all-intents=true&log=true&subscription-key=17eef37902314781b553a7b38b4d9e8b&query="