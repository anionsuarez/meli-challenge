from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# import mysql.connector
# from mysql.connector import errorcode
import MySQLdb

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

"""Get a list of Messages from the user's mailbox.
"""
from apiclient import errors

def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # --------
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)

    # try:
    #   service = build('gmail', 'v1', credentials=creds)

    #   messages = ListMessagesMatchingQuery(service,'me','label: DO newsletter')
    #   # f= open("ids.txt","w+")

    #   for message in messages:
    #       print (message['id'])
    # except:
    #   print('Antes de ejecutar este comando debe validar Gmail\n Ejecute:\npython3 first-run-validation.py')
    # -------
    dbasename='elmailingresado'

    # Open database connection ( If database is not created don't give dbname)
    db = MySQLdb.connect("challenge_db_1","root","root")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # For creating create db
    # Below line  is hide your warning 
    cursor.execute("SET sql_notes = 0; ")
    # create db here....
    cursor.execute("create database IF NOT EXISTS Writersdb")

    # create table
    cursor.execute("SET sql_notes = 0; ")
    cursor.execute("CREATE TABLE if not exists Writersdb.Writers(Id INT PRIMARY KEY AUTO_INCREMENT, \
                Name VARCHAR(25))")
    cursor.execute("SET sql_notes = 1; ")

    #insert data
    cursor.execute("INSERT INTO Writersdb.Writers(Name) VALUES('Jack London')")

    # Commit your changes in the database
    db.commit()

    # disconnect from server
    db.close()

main()

# CREATE TABLE `devops_mails` (
#   `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
#   `date` date NOT NULL,
#   `from` text COLLATE 'utf8_bin' NOT NULL,
#   `subject` text COLLATE 'utf8_bin' NOT NULL
# );