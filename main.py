import argparse
import mysql.connector
import keys
import db_util
import requests
import json

DATABASE_NAME = "vtadatabase"
TRIPUPDATES_TABLE = "TripUpdates"
STOPTIMEUPDATES_TABLE = "StopTimeUpdates"
DEPARTURES_TABLE = "Departures"
ARRIVALS_TABLE = "Arrivals"

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
#mycursor.execute("DROP TABLE " + TRIPUPDATES_TABLE)
#TODO move this to a separate module
mycursor.execute("CREATE TABLE IF NOT EXISTS " + TRIPUPDATES_TABLE + " (id VARCHAR(255), timestamp INT, PRIMARY KEY (id))")
mycursor.execute("CREATE TABLE IF NOT EXISTS " + STOPTIMEUPDATES_TABLE + " (id VARCHAR(255), stop_sequence INT, stop_id VARCHAR(255), schedule_relationship VARCHAR(255), PRIMARY KEY (id, stop_id))")
mycursor.execute("CREATE TABLE IF NOT EXISTS " + DEPARTURES_TABLE + " (id VARCHAR(255), stop_id VARCHAR(255), time INT, uncertainty INT, PRIMARY KEY (id, stop_id))")
mycursor.execute("CREATE TABLE IF NOT EXISTS " + ARRIVALS_TABLE + " (id VARCHAR(255), stop_id VARCHAR(255), time INT, uncertainty INT, PRIMARY KEY (id, stop_id))")
db_util.show_tables(mycursor)

#TODO add error handling for API call
#TODO fix strings to new concat style
data = requests.get('https://api.goswift.ly/real-time/vta/gtfs-rt-trip-updates?apiKey=' + keys.API_key + '&format=json')
data = json.loads(data.text)
data = data["entity"]

#TODO clean up this loop
#for every tripupdate
for update in data:
  #for every stopTimeUpdate
  if 'stopTimeUpdate' in update['tripUpdate']:
    update_arr = update['tripUpdate']['stopTimeUpdate']
    for timeUpdate in update_arr:
      query = "INSERT IGNORE INTO stoptimeupdates (id, stop_sequence, stop_id, schedule_relationship) VALUES (%s, %s, %s, %s)"
      val = (update["id"], timeUpdate["stopSequence"], timeUpdate["stopId"], timeUpdate["scheduleRelationship"])
      mycursor.execute(query,val)

  query = "INSERT IGNORE INTO tripupdates (id, timestamp) VALUES (%s, %s)"
  val = (update["id"], update["tripUpdate"]["timestamp"])
  mycursor.execute(query,val)
  #mycursor.execute("INSERT INTO " + TRIPUPDATES_TABLE + " (id, timestamp) VALUES (" + update["id"] + "," + update["tripUpdate"]["timestamp"] + ")")

mycursor.execute("select * from " + TRIPUPDATES_TABLE)
i = 0
for x in mycursor:
  i = i + 1
print(i)

db.commit()
#db.close()
