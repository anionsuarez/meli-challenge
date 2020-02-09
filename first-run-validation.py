from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from shutil import copyfile

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('python/token.pickle'):
        # with open('token.pickle', 'rb') as token:
        #     creds = pickle.load(token)
        #  Levanta las credenciales para poder usarlas, pero yo solo quiero avisar de que puede correr docker
        print ('Ya estaban cargadas las credenciales, puede correr:\n docker-compose up -d --build\n')
    else:
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        copyfile('token.pickle', 'python/token.pickle') # Lo copio porque despues el docker file no me deja seleccionar archivos por arriba de su nivel
        print ('\nYa se cargaron las credenciales, puede correr:\n docker-compose up -d --build && docker logs -f challenge_python_1\n')

main()