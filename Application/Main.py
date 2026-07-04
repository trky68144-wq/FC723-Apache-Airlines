# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 20:44:34 2026

@author: PC
"""

# Import random to generate random characters for booking references
import random
 
# Import string to get the list of letters and digits
import string
 
# Import sqlite3 to create and use a local database for passenger details
import sqlite3



def setup_database(conn):
    # This function creates the bookings table in the database
    # It only creates the table if it does not already exist
 
    # Get a cursor to run SQL commands
    cursor = conn.cursor()
 
    # Create the bookings table with all required columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_ref   TEXT PRIMARY KEY,
            passport_no   TEXT NOT NULL,
            first_name    TEXT NOT NULL,
            last_name     TEXT NOT NULL,
            seat_row      INTEGER NOT NULL,
            seat_column   TEXT NOT NULL
        )
    """)
 
    # Save the changes to the database
    conn.commit()
    print("  Database ready.")