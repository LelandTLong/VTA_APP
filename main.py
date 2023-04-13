import argparse
import mysql.connector
import keys
import db_util

DATABASE_NAME = "vtadatabase"
TRIPUPDATES_TABLE = "TripUpdates"
STOPTIMEUPDATES_TABLE = "StopTimeUpdates"

dbCheck = mysql.connector.connect(
  host="localhost",
  user=keys.user,
  password=keys.password,
)

mycursor = dbCheck.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS " + DATABASE_NAME)
db_util.show_databases(mycursor)

db = mysql.connector.connect(
  host="localhost",
  user=keys.user,
  password=keys.password,
  database=DATABASE_NAME
)

mycursor = db.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS " + TRIPUPDATES_TABLE + " (ID VARCHAR(255))")
db_util.show_tables(mycursor)