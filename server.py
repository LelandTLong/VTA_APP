from flask import Flask, json
import keys
import mysql.connector

#TODO move DB creation to a separate module
DATABASE_NAME = "vtadatabase"
db = mysql.connector.connect(
  host="localhost",
  user=keys.user,
  password=keys.password,
  database=DATABASE_NAME
)
mycursor = db.cursor()
#query = "SELECT json_object('id', id, 'tripupdate', (SELECT json_arrayagg(json_object('stop_sequence', stop.stop_sequence, 'stop_id', stop.stop_id)) FROM stopTimeUpdates AS stop WHERE stop.id = trip.id)) AS stopRecord, 'timestamp', timestamp FROM tripUpdates as trip"
#query = "SELECT json_arrayagg(json_object('id', id, 'stoptimeupdate', (SELECT json_arrayagg(json_object('stop_sequence', stop.stop_sequence, 'stop_id', stop.stop_id)) FROM stopTimeUpdates AS stop WHERE stop.id = trip.id), 'timestamp', timestamp)) FROM tripUpdates as trip"
#query2 = "SELECT json_arrayagg(json_object('id', id, 'tripupdates', json_object('stoptimeupdate', (SELECT json_arrayagg(json_object('stop_sequence', stop.stop_sequence, 'stop_id', stop.stop_id)) FROM stopTimeUpdates AS stop WHERE stop.id = trip.id)), 'timestamp', timestamp)) FROM tripUpdates as trip"

#TODO clean this up
query = "SELECT json_arrayagg(json_object('id', id, 'tripupdates', " \
"json_object('stoptimeupdate', (" \
"SELECT json_arrayagg(json_object('stop_sequence', stop.stop_sequence, 'stop_id', stop.stop_id" \
", 'arrival'," \
"(SELECT json_object('time', arr.time) from arrivals as arr WHERE stop.id = arr.id AND stop.stop_id = arr.stop_id)" \
", 'departure'," \
"(SELECT json_object('time', dept.time) from departures as dept WHERE stop.id = dept.id AND stop.stop_id = dept.stop_id)"\
")) FROM stopTimeUpdates AS stop WHERE stop.id = trip.id))" \
", 'timestamp', timestamp)) FROM tripUpdates as trip"

mycursor.execute(query)
result = ""
for x in mycursor:
  result = result + x[0]

api = Flask(__name__)

@api.route('/real-time/trip-updates', methods=['GET'])
def get_trip_updates():
  return result

if __name__ == '__main__':
    api.run()