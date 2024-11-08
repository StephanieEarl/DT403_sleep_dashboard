# Converting my csvs to a .db

import pandas as pd
import sqlite3
import logging

# Setup logging
logging.basicConfig(filename="app.log", level=logging.DEBUG)

DATABASE = 'sleep_dashboard.db'

def drop_tables(tables):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            for table in tables:
                query = f"DROP TABLE IF EXISTS {table}"
                cursor.execute(query)
                logging.info("Dropped table %s", table)
    except sqlite3.Error as e:
        logging.error("Database error: %s", e)

# List of tables to drop
tables_to_drop = ['Participant', 'Physical', 'Sessions', 'Sleep']

# Drop the tables
drop_tables(tables_to_drop)

print("Tables dropped successfully.")

# List of CSV files and corresponding table names
csv_files = ['Participant.csv', 'Sessions.csv', 'Physical.csv', 'Sleep.csv']
table_names = ['Participant', 'Sessions', 'Physical', 'Sleep']

# Create SQLite database

conn = sqlite3.connect('sleep_dashboard.db')
cursor = conn.cursor()

# Create the Sessions table with the correct data types
create_sessions_table = """
CREATE TABLE Sessions (
    person_ID INTEGER,
    session_ID TEXT,
    session_type TEXT,
    session_date DATE,
    session_status TEXT,
    sessions_attended INTEGER,
    course_status TEXT
);
"""
cursor.execute(create_sessions_table)


# Looping through each  CSV to write to a separate table

for csv_files, table_names in zip(csv_files, table_names):
    df = pd.read_csv(csv_files)

# Convert date columns to datetime format
    for column in df.columns:
        if 'date' in column.lower():
            df[column] = pd.to_datetime(df[column], format='%d/%m/%Y', errors='coerce').dt.date

    if table_names =='Sessions':
        df.to_sql(table_names, conn, if_exists='append', index=False)
    else:
        df.to_sql(table_names, conn, if_exists='replace', index=False)

# Renaming a column in an existing table
alter_sessions_table = """
ALTER TABLE Sessions RENAME COLUMN course_status TO clinic_status;
"""
cursor.execute(alter_sessions_table)

alter_physical_table = """
ALTER TABLE Physical RENAME COLUMN bmi TO calculated_bmi;
"""
cursor.execute(alter_physical_table)

alter_sleep_table = """
ALTER TABLE Sleep RENAME COLUMN sleep_duration_hours TO avg_sleep_hours;
"""
cursor.execute(alter_sleep_table)

# Commit and close the connection

conn.commit()
conn.close()

print("CSVs now .db file")

