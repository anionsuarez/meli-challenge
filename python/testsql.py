from __future__ import print_function
import sys
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from apiclient import errors

from datetime import datetime
import dateutil.parser as parser

import MySQLdb

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

"""Get a list of Messages from the user's mailbox.
"""

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
                  `ID` int NOT NULL PRIMARY KEY, \
                  `Fecha` date NOT NULL, \
                  `From` varchar(80) NOT NULL, \
                  `Subject` text NOT NULL) COLLATE 'utf8mb4_bin'")
  cursor.execute("SET sql_notes = 1; ")

  return(cursor,db)

def database_getID(dbasename,cursor): # Obtengo los IDs de cada correo que tengo guardado
  cursor.execute("SELECT ID FROM "+dbasename+".correos")
  ids = cursor.fetchall() # Me devuelve una lista de listas, hago un recursivo para dejar todo en una lista unica
  lista_unica = []
  for sublist in ids:
    for item in sublist:
        lista_unica.append(item)
  return (lista_unica)

def database_store(dbasename,cursor,mail_id,fecha,de,asunto):
  cursor.execute("INSERT INTO "+dbasename+".correos (`ID`,`Fecha`, `From`, `Subject`) VALUES (%s, %s, %s, %s)", (mail_id,fecha,de,asunto))

def database_save(db):
  db.commit()
  db.close() 

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    dbasename='mailingresado'
    cursor,db = database_setup(dbasename)
    ids = database_getID(dbasename,cursor)
    
    print (ids)
    if 212 not in ids:
      print ("No Esta")
    
main()

# PENDIENTES
# Guardar los id de los mensajes en la base, traerlos a una lista y en el loop consultar si esta en la lista
# evito consultas de mas e inserto solo los nuevos.

# Como plus, dejar como leido el mensaje