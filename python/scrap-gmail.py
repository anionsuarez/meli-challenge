from __future__ import print_function
import sys
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

from datetime import datetime
import time
import dateutil.parser as parser


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

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()

    headers = message['payload']['headers']
    for header in headers:
      if header['name'] == "Date" :
        fecha_texto = header['value']
        parseo = (parser.parse(fecha_texto))
        fecha = (parseo.date())
      if header['name'] == "From" :
        de = header['value']
      if header['name'] == "Subject" :
        asunto = header['value']
    # fecha = [i['value'] for i in headers if i["name"]=="Date"]
    # de = [i['value'] for i in headers if i["name"]=="From"]
    # asunto = [i['value'] for i in headers if i["name"]=="Subject"]
    return (fecha,de,asunto)

  except errors.HttpError as error:
    print ('An error occurred: %s' % error)

def database_setup(dbasename):

  # Open database connection ( If database is not created don't give dbname)
  db = MySQLdb.connect("challenge_db_1","root","root")

  # prepare a cursor object using cursor() method
  cursor = db.cursor()

  # For creating create db
  # Below line  is hide your warning 
  cursor.execute("SET sql_notes = 0; ")
  # create db here....
  cursor.execute("create database IF NOT EXISTS "+dbasename)

  # create table
  cursor.execute("SET sql_notes = 0; ")
  cursor.execute("CREATE TABLE if not exists "+dbasename+".correos(\
                  `ID` int NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                  `Fecha` date NOT NULL, \
                  `From` varchar(80) NOT NULL, \
                  `Subject` text NOT NULL) COLLATE 'utf8mb4_bin'")
  cursor.execute("SET sql_notes = 1; ")

  return(cursor,db)

def database_store(dbasename,cursor,fecha,de,asunto):
  
  
  #insert data
  cursor.execute("INSERT INTO "+dbasename+".correos (`Fecha`, `From`, `Subject`) VALUES (%s, %s, %s)", (fecha,de,asunto))

  # cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
  #                 (name, email, username, password))
  # Commit your changes in the database

def database_save(db):
  db.commit()

  # disconnect from server
  db.close() 

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    try:
      service = build('gmail', 'v1', credentials=creds)
    except:
      print('Antes de ejecutar este comando debe validar Gmail\n Ejecute:\npython3 first-run-validation.py')
      sys.exit()

    messages = ListMessagesMatchingQuery(service,'me','label: DO newsletter')
    # is:unread subject:devops devops -in:chats
    # f= open("ids.txt","w+")
    dbasename='mailingresado'
    cursor,db = database_setup(dbasename)
    inserts = 0
    for message in messages:
        # print (message['id'])
        fecha,de,asunto = GetMessage(service, 'me', message['id'])

        database_store(dbasename,cursor,fecha,de,asunto)
        inserts += 1 

    database_save(db)
    print ("Se insertaron "+str(inserts)+" registros en la base de datos")

main()