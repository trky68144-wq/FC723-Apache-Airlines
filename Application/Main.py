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
    
    

def generate_booking_ref(conn):
    # This function creates a unique 8-character booking reference
    # 1. Build a pool: A-Z and 0-9 (36 characters)
    # 2. Pick 8 random characters
    # 3. Check the database — if unique, return it
    # 4. If not unique, try again

    # Get a cursor to run database queries
    cursor = conn.cursor()

    # Build the pool of characters: uppercase letters and digits
    characters = string.ascii_uppercase + string.digits

    # Keep trying until a unique reference is found
    while True:

        # Pick 8 random characters and join them into one string
        ref = "".join(random.choices(characters, k=8))

        # Check if this reference already exists in the database
        cursor.execute(
            "SELECT COUNT(*) FROM bookings WHERE booking_ref = ?", (ref,)
        )

        # If count is 0 the reference is unique — return it
        if cursor.fetchone()[0] == 0:
            return ref

        # If count is not 0 the reference already exists — loop again