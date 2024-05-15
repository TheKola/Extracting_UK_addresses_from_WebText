import sqlite3
import json

db_file = 'data/DATABASE_FILE.db'
json_file = 'data/database.json'
table_name = 'TABLE_NAME'

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Get a list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"Table Name: {table_name}")
    
    # Get the schema of each table
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()
    
    # Print the schema
    for column in schema:
        print(f"Column Name: {column[1]}, Type: {column[2]}")

# Execute a query to select all data from the table
cursor.execute(f"SELECT * FROM {table_name}")

# Fetch all the rows from the result
rows = cursor.fetchall()

# Define a list to store the data
data = []

# Fetch the column names for the keys in the JSON
column_names = [description[0] for description in cursor.description]

# Convert the rows to dictionaries and add them to the data list
for row in rows:
    row_dict = dict(zip(column_names, row))
    data.append(row_dict)

# Save the data to a JSON file
with open(json_file, 'w') as file:
    json.dump(data, file, indent=4)

# Close the cursor and the database connection
cursor.close()
conn.close()

print(f"Data from '{table_name}' table has been saved to '{json_file}' in JSON format.")