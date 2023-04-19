import argparse
import keys
import db_util
import requests
import json

#TODO move src files to separate directory
#TODO add ARGs to handle clearing DB and parsing data options
parser = argparse.ArgumentParser(
  prog='VTA_APP'
)
parser.add_argument(
  '--clear-data', 
  dest='clear_data', 
  action='store_true', 
  required=False, 
  default=False,
  help='Clear existing DB data before running application'
)
args = parser.parse_args()

db_util.db_check()
db, mycursor = db_util.init_db()
if args.clear_data == True:
  print('wiping the DB')
  db_util.clear_data(mycursor)
db_util.create_tables(mycursor)

#TODO add error handling for API call
data = requests.get('https://api.goswift.ly/real-time/vta/gtfs-rt-trip-updates?apiKey=' + keys.API_key + '&format=json')
data = json.loads(data.text)
data = data["entity"]

#TODO add trip object for extra credit
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
  
  #store the trip object
  """
  trip = trip_update['trip']
  query = "INSERT IGNORE INTO trips (id, trip_id, route_id, start_date, schedule_relationship) VALUES (%s, %s, %s, %s, %s)"
  val = (update_set["id"], trip["tripId"], trip["routeId"], trip["startDate"], trip["scheduleRelationship"])
  mycursor.execute(query,val)

  #store vehicle object - check since this isn't required
  vehicle = trip_update['vehicle']
  query = "INSERT IGNORE INTO vehicles (id, vehicle_id) VALUES (%s, %s, %s)"
  val = (update_set["id"], trip["id"])
  mycursor.execute(query,val)
  """
  #check if there is an outdated entry of this tripupdate
  #query = "SELECT EXISTS(SELECT * FROM tripupdates where ("

  #store tripupdate object
  query = "INSERT IGNORE INTO tripupdates (id, trip_id, route_id, start_date, schedule_relationship, vehicle_id, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
  trip = trip_update["trip"]
  if 'vehicle' in trip_update:
    vehicle = trip_update["vehicle"]
    vehicle = vehicle["id"]
  else:
    vehicle = None
  val = (update_set["id"], trip["tripId"], trip["routeId"], trip["startDate"], trip["scheduleRelationship"], vehicle, trip_update["timestamp"])
  mycursor.execute(query,val)

print("Logged", count, "entries from the API call")
db_util.count_trip_updates(mycursor)
db.commit()
db.close()
