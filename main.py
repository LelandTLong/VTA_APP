import argparse
import mysql.connector

#TODO add username and password option for database

DATABASE_NAME = "vtadatabase"
TRIPUPDATES_TABLE = "TripUpdates"
STOPTIMEUPDATES_TABLE = "StopTimeUpdates"

dbCheck = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
)

mycursor = dbCheck.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS " + DATABASE_NAME)
mycursor.execute("SHOW DATABASES")

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database=DATABASE_NAME
)

mycursor = db.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS " + TRIPUPDATES_TABLE + " (ID VARCHAR(255))")
mycursor.execute("SHOW TABLES")