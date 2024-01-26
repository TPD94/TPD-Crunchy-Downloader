# Import dependencies
import os
import sqlite3


# Define function to check and create database
def database_check_and_create():

    # Check to see if a database exists in keys directory, if not create it
    if not os.path.isfile(f"{os.getcwd()}/config/database/keys.db"):
        dbconnection = sqlite3.connect(f"{os.getcwd()}/config/database/keys.db")
        dbcursor = dbconnection.cursor()
        dbcursor.execute('CREATE TABLE IF NOT EXISTS "DATABASE" ( "pssh" TEXT, "keys" TEXT, PRIMARY KEY("pssh") )')
        dbconnection.close()


# Define function to cache keys in database
def cache_keys(pssh: str, keys: str):
    dbconnection = sqlite3.connect(f"{os.getcwd()}/config/database/keys.db")
    dbcursor = dbconnection.cursor()
    dbcursor.execute("INSERT or REPLACE INTO database VALUES (?, ?)", (pssh, keys))
    dbconnection.commit()
    dbconnection.close()