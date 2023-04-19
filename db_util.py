import mysql.connector
import keys

DATABASE_NAME = "vtadatabase"
TRIPUPDATES_TABLE = "TripUpdates"
STOPTIMEUPDATES_TABLE = "StopTimeUpdates"
DEPARTURES_TABLE = "Departures"
ARRIVALS_TABLE = "Arrivals"
#TRIPS_TABLE = "Trips"
#VEHICLES_TABLE = "Vehicles"
#table_array = [TRIPUPDATES_TABLE, STOPTIMEUPDATES_TABLE, DEPARTURES_TABLE, ARRIVALS_TABLE, TRIPS_TABLE, VEHICLE_TABLE]

#TODO add function headers
#TODO add array for all tables to add and drop

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
  cursor.execute("DROP TABLE tripupdates")
  cursor.execute("DROP TABLE stoptimeupdates")
  cursor.execute("DROP TABLE departures")
  cursor.execute("DROP TABLE arrivals")

def create_tables(cursor):
  cursor.execute("CREATE TABLE IF NOT EXISTS " + TRIPUPDATES_TABLE + " (id VARCHAR(255), timestamp INT, trip_id VARCHAR(255), route_id VARCHAR(255), start_date VARCHAR(255), schedule_relationship VARCHAR(255), vehicle_id VARCHAR(255), PRIMARY KEY (id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS " + STOPTIMEUPDATES_TABLE + " (id VARCHAR(255), stop_sequence INT, stop_id VARCHAR(255), schedule_relationship VARCHAR(255), PRIMARY KEY (id, stop_id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS " + DEPARTURES_TABLE + " (id VARCHAR(255), stop_id VARCHAR(255), time INT, PRIMARY KEY (id, stop_id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS " + ARRIVALS_TABLE + " (id VARCHAR(255), stop_id VARCHAR(255), time INT, PRIMARY KEY (id, stop_id))")
  #cursor.execute("CREATE TABLE IF NOT EXISTS " + TRIPS_TABLE + " (id VARCHAR(255), trip_id VARCHAR(255), route_id VARCHAR(255), start_date VARCHAR(255), schedule_relationship VARCHAR(255), PRIMARY KEY (id))")
  #cursor.execute("CREATE TABLE IF NOT EXISTS " + VEHICLES_TABLE + " (id VARCHAR(255), vehicle_id VARCHAR(255), label VARCHAR(255), PRIMARY KEY (id))")
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
