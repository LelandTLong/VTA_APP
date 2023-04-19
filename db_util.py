import mysql.connector
import keys

DATABASE_NAME = "vtadatabase"
TRIPUPDATES_TABLE = "TripUpdates"
STOPTIMEUPDATES_TABLE = "StopTimeUpdates"

#TODO add function headers

def db_check():
  dbCheck = mysql.connector.connect(
    host="localhost",
    user=keys.user,
    password=keys.password,
  )
  cursor = dbCheck.cursor()
  cursor.execute("CREATE DATABASE IF NOT EXISTS " + DATABASE_NAME)
  show_databases(cursor)

def clear_data(cursor):
  cursor.execute("DROP TABLE IF EXISTS tripupdates")
  cursor.execute("DROP TABLE IF EXISTS stoptimeupdates")

def create_tables(cursor):
  cursor.execute("CREATE TABLE IF NOT EXISTS " + TRIPUPDATES_TABLE + " (id VARCHAR(255), timestamp INT, trip_id VARCHAR(255), route_id VARCHAR(255), start_date VARCHAR(255), schedule_relationship VARCHAR(255), vehicle_id VARCHAR(255), PRIMARY KEY (id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS " + STOPTIMEUPDATES_TABLE + " (id VARCHAR(255), stop_sequence INT, stop_id VARCHAR(255), schedule_relationship VARCHAR(255), arrival_uncertainty INT, arrival_time INT, departure_uncertainty INT, departure_time INT, PRIMARY KEY (id, stop_id))")
  show_tables(cursor)

def init_db():
  db = mysql.connector.connect(
    host="localhost",
    user=keys.user,
    password=keys.password,
    database=DATABASE_NAME
  )
  mycursor = db.cursor()
  return db, mycursor

def show_tables(cursor):
  cursor.execute("SHOW TABLES")
  print("TABLES:")
  for table in cursor:
    print(table)

def show_databases(cursor):
  cursor.execute("SHOW DATABASES")
  print("DATABASES:")
  for database in cursor:
    print(database)

def count_trip_updates(cursor):
  i = 0
  cursor.execute("SELECT * FROM tripupdates")
  for entry in cursor:
    i += 1
  print("The number of trip updates in the DB is", i)

def delete_dupes(new_update):
  query = "SELECT * FROM tripupdates as old WHERE (old.trip_id = %s AND old.timestamp < %s)"
  val = (new_update['tripId'], new_update['timestamp'])
  cursor.execute(query, val)
