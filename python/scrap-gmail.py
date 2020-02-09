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
from dateutil import tz
import dateutil.parser as parser
import MySQLdb

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Defino el timezone de Uruguay, para imprimir mensajes mas adelante
UYT = tz.tzoffset("UYT",-10800)

# Lista todos los correos del usuario que cumplan con la query
def ListMessagesMatchingQuery(service, user_id, query=''):
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

# Pasado el id de un correo, devuelve su fecha, quien envia y el asunto
def GetMessage(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()

    headers = message['payload']['headers']
    asunto = '-- SIN ASUNTO --' # Para el caso de correos sin asunto, seteo la variable con ese valor 
    # Recorro los headers y busco la fecha, el origen y el asunto
    for header in headers:
      if header['name'] == "Date" :
        fecha_texto = header['value']
        parseo = (parser.parse(fecha_texto))
        fecha = (parseo.date())
      
      if header['name'] == "From" :
        de = header['value']
      
      if header['name'] == "Subject" :
        asunto = header['value']
    return (fecha,de,asunto)
  except errors.HttpError as error:
    print ('Error al recuperar un mensaje: %s' % error)

def database_setup(dbasename):
  # Me conecto al contenedor de la base de datos
  db = MySQLdb.connect("database_container","root","root")
  cursor = db.cursor()
  cursor.execute("SET sql_notes = 0; ")
  # Creo la base de datos si no existe
  cursor.execute("create database IF NOT EXISTS "+dbasename)
  cursor.execute("SET sql_notes = 0; ")
  # Creo la tabla
  cursor.execute("CREATE TABLE if not exists "+dbasename+".correos(\
                  `ID` varchar(25) NOT NULL PRIMARY KEY, \
                  `Fecha` date NOT NULL, \
                  `From` varchar(80) NOT NULL, \
                  `Subject` text NOT NULL) COLLATE 'utf8mb4_bin'")
  cursor.execute("SET sql_notes = 1; ")
  return(cursor,db)

# Obtengo los IDs de los correos que tengo en la base de datos
def database_getID(dbasename,cursor): 
  cursor.execute("SELECT ID FROM "+dbasename+".correos")
  ids = cursor.fetchall() # Me devuelve una lista de listas, hago un recursivo para dejar todo en lista_unica
  lista_unica = []
  for sublist in ids:
    for item in sublist:
      lista_unica.append(item)
  return (lista_unica)

# Guardo de a un mail a la vez
def database_store(dbasename,cursor,mail_id,fecha,de,asunto):
  cursor.execute("INSERT INTO "+dbasename+".correos (`ID`,`Fecha`, `From`, `Subject`) VALUES (%s, %s, %s, %s)", (mail_id,fecha,de,asunto))

def database_save(db):
  db.commit()
  db.close() 

def main():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    try:
      with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
      service = build('gmail', 'v1', credentials=creds)
    except:
      # Capturo el error del llamado a la api
      print('Error inesperado: ',sys.exc_info()[0])
      print('Fin del script\n')
      sys.exit()
  else:
    # Si no tengo el token.pickle tengo que correr la validación primero
    print('Antes de ejecutar este comando debe validar Gmail\n Ejecute:\npython3 first-run-validation.py')
    sys.exit()
  # Levanto todos los correos que validen con la búsqueda, busco devops excluyendo los chats
  messages = ListMessagesMatchingQuery(service,'me','devops -in:chats')
  # Levanto la info del profile, me quedo con el correo
  profile = service.users().getProfile(userId='me').execute()
  # Uso el username como nombre de la base de datos
  dbasename = profile['emailAddress'].split('@')[0]
  
  cursor,db = database_setup(dbasename)
  id_lists = database_getID(dbasename,cursor)
  inserts = 0
  # Recorro cada ID de mensaje que devuelve la búsqueda
  for message in messages:
      # Si no lo tengo en id_list, obtengo el mensaje completo
      if message['id'] not in id_lists:
        fecha,de,asunto = GetMessage(service, 'me', message['id'])
        # Lo guardo
        database_store(dbasename,cursor,message['id'],fecha,de,asunto)
        inserts += 1 

  if inserts > 0 :
    database_save(db)
    print ("Se insertaron "+str(inserts)+" registros en la base de datos")
  else:
    print ("No hay correos nuevos que validen la busqueda")
  
  print(datetime.now(tz=UYT).strftime("%m/%d/%Y, %H:%M:%S")+" - Fin del script\n")

main()