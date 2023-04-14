import argparse
import mysql.connector
import keys
import db_util
import requests
import json

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
#mycursor.execute("DROP TABLE " + TRIPUPDATES_TABLE)
mycursor.execute("CREATE TABLE IF NOT EXISTS " + TRIPUPDATES_TABLE + " (id VARCHAR(255), timestamp INT, PRIMARY KEY (id))")
db_util.show_tables(mycursor)

#TODO add error handling for API call
data = requests.get('https://api.goswift.ly/real-time/vta/gtfs-rt-trip-updates?apiKey=' + keys.API_key + '&format=json')
data = json.loads(data.text)
data = data["entity"]

for update in data:
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
