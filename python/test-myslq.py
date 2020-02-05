# import mysql.connector
# from mysql.connector import Error

# try:
#     connection = mysql.connector.connect(host='localhost',
#                                         #  database='test',
#                                          user='root',
#                                          password='root')
#     if connection.is_connected():
#         db_Info = connection.get_server_info()
#         print("Connected to MySQL Server version ", db_Info)
#         cursor = connection.cursor()
#         cursor.execute("select database();")
#         record = cursor.fetchone()
#         print("You're connected to database: ", record)

# except Error as e:
#     print("Error while connecting to MySQL", e)
# finally:
#     if (connection.is_connected()):
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")

import MySQLdb

dbasename='elmailingresado'
# db=MySQLdb.connect(passwd="root")
# db=

# Open database connection ( If database is not created don't give dbname)
db = MySQLdb.connect("challenge_db_1","root","root")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# For creating create db
# Below line  is hide your warning 
cursor.execute("SET sql_notes = 0; ")
# create db here....
cursor.execute("create database IF NOT EXISTS "+dbasename)