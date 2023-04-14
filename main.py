import argparse
import keys
import db_util
import requests
import json

#TODO add ARGs to handle clearing DB and parsing data options
db_util.db_check()
db, mycursor = db_util.init_db()

#TODO fix trip_updates schema to match this
db_util.create_tables(mycursor)

#TODO add error handling for API call
data = requests.get('https://api.goswift.ly/real-time/vta/gtfs-rt-trip-updates?apiKey=' + keys.API_key + '&format=json')
data = json.loads(data.text)
data = data["entity"]

#TODO clean up this loop
#for every tripupdate
count = 0
for update_set in data:
  count += 1
  trip_update = update_set['tripUpdate']
  #for every stopTimeUpdate
  if 'stopTimeUpdate' in trip_update:
    stop_updates = trip_update['stopTimeUpdate']
    for stop_update in stop_updates:
      query = "INSERT IGNORE INTO stoptimeupdates (id, stop_sequence, stop_id, schedule_relationship) VALUES (%s, %s, %s, %s)"
      val = (update_set["id"], stop_update["stopSequence"], stop_update["stopId"], stop_update["scheduleRelationship"])
      mycursor.execute(query,val)

      #if add departures and arrivals entity if they exist
      if 'departure' in stop_update:
        departure = stop_update['departure']
        query = "INSERT IGNORE INTO departures (id, stop_id, time) VALUES (%s, %s, %s)"
        val = (update_set["id"], stop_update["stopId"], departure['time'])
        mycursor.execute(query,val)
      if 'arrival' in stop_update:
        arrival = stop_update['arrival']
        query = "INSERT IGNORE INTO arrivals (id, stop_id, time) VALUES (%s, %s, %s)"
        val = (update_set["id"], stop_update["stopId"], arrival['time'])
        mycursor.execute(query,val)
  query = "INSERT IGNORE INTO tripupdates (id, timestamp) VALUES (%s, %s)"
  val = (update_set["id"], trip_update["timestamp"])
  mycursor.execute(query,val)

print("Logged", count, "entries")
db.commit()
db.close()
