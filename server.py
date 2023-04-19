from flask import Flask, json
import keys
import mysql.connector
import db_util

#TODO move DB creation to a separate module
db, mycursor = db_util.init_db()

#TODO clean this up
"""
query = "SELECT json_arrayagg(json_object('id', id, 'tripupdates', " \
"json_object('stoptimeupdate', (" \
"SELECT json_arrayagg(json_object('stop_sequence', stop.stop_sequence, 'stop_id', stop.stop_id" \
", 'arrival'," \
"(SELECT json_object('time', arr.time) from arrivals as arr WHERE stop.id = arr.id AND stop.stop_id = arr.stop_id)" \
", 'departure'," \
"(SELECT json_object('time', dept.time) from departures as dept WHERE stop.id = dept.id AND stop.stop_id = dept.stop_id)"\
")) FROM stopTimeUpdates AS stop WHERE stop.id = trip.id))" \
", 'timestamp', timestamp)) FROM tripUpdates as trip LIMIT 100"
"""

query = "SELECT json_arrayagg(json_object('id', id, 'tripupdates', " \
"json_object('stoptimeupdate', (" \
"SELECT json_arrayagg(json_object('stop_sequence', stop.stop_sequence, 'stop_id', stop.stop_id" \
", 'arrival', json_object('time', stop.arrival_time, 'uncertainty', stop.arrival_uncertainty)" \
", 'departure', json_object('time', stop.departure_time, 'uncertainty', stop.departure_uncertainty)" \
")) FROM stopTimeUpdates AS stop WHERE stop.id = trip.id))" \
", 'timestamp', timestamp)) FROM tripUpdates as trip LIMIT 100"

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