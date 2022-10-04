import os

class DefaultConfig:
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_URL=""
    SQL_DB_SERVER = 'botbee-sql-server.database.windows.net'
    SQL_DATABASE = 'botbeeUserDataDB'
    SQL_USERNAME = 'azureuser'  
    SQL_DRIVER= '{ODBC Driver 17 for SQL Server}'

    # Fundamentals language
    LANGUAGE_ENDPOINT = "https://language-service-sid-0987.cognitiveservices.azure.com/"
    LANGUAGE_CREDENTIAL_KEY = "xxxxxxx"
    FUNDAMENTALS_KNOWLEDGE_BASE_PROJECT = "language-studio-proj-sid-0987"
    ASSOCIATE_KNOWLEDGE_BASE_PROJECT = "language-studio-proj-sid-0987"
