import argparse
import keys
import db_util
import requests
import json

#TODO move src files to separate directory
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

#for every tripupdate
count = 0
for update_set in data:
  count += 1
  trip_update = update_set['tripUpdate']
  db_util.delete_dupes(trip_update)

  #for every stopTimeUpdate
  if 'stopTimeUpdate' in trip_update:
    stop_updates = trip_update['stopTimeUpdate']
    for stop_update in stop_updates:
      #check if arrivals and departures exists
      arrival_time = '-1'
      arrival_uncertainty = '-1'
      depart_time = '-1'
      depart_uncertainty = '-1'
      
      if 'arrival' in stop_update:
        arrival = stop_update["arrival"]
        if 'time' in arrival:
          arrival_time = arrival["time"]
        if 'uncertainty' in arrival:
          arrival_uncertainty = arrival["uncertainty"]
      if 'departure' in stop_update:
        departure = stop_update["departure"]
        if 'time' in departure:
          depart_time = departure["time"]
        if 'uncertainty' in departure:
          depart_uncertainty = departure["uncertainty"]
        
      query = "INSERT IGNORE INTO stoptimeupdates (id, stop_sequence, stop_id, schedule_relationship, arrival_uncertainty, arrival_time, departure_uncertainty, departure_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
      val = (update_set["id"], stop_update["stopSequence"], stop_update["stopId"], stop_update["scheduleRelationship"], arrival_uncertainty, arrival_time, depart_uncertainty, depart_time)
      mycursor.execute(query,val)

  #store tripupdate object
  query = "INSERT IGNORE INTO tripupdates (id, trip_id, route_id, start_date, schedule_relationship, vehicle_id, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
  trip = trip_update["trip"]
  if 'vehicle' in trip_update:
    vehicle = trip_update["vehicle"]
    vehicle = vehicle["id"]
  else:
    vehicle = 'null'
  val = (update_set["id"], trip["tripId"], trip["routeId"], trip["startDate"], trip["scheduleRelationship"], vehicle, trip_update["timestamp"])
  mycursor.execute(query,val)

print("Logged", count, "entries from the API call")
db_util.count_trip_updates(mycursor)
db.commit()
db.close()
