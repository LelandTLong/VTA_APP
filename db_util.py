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
