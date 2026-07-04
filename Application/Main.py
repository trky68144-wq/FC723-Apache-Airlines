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
        
       
def create_seat_map():
    # This function builds the seat map for the Burak757 aircraft
    # The map is a 2D list with 7 columns and 80 rows

    # Create an empty list to hold all the columns
    seat_map = []

    # Define the column labels in order
    col_labels = ["A", "B", "C", "X", "D", "E", "F"]

    # Loop through each column label
    for col_index, col_label in enumerate(col_labels):

        # Create an empty list for this column
        column = []

        # Loop through all 80 rows
        for row in range(80):

            if col_label == "X":
                # This is the aisle column — no bookings allowed
                column.append("X")

            elif col_label in ("D", "E", "F") and row in (76, 77):
                # Rows 77 and 78 in columns D, E, F are storage areas
                column.append("S")

            else:
                # All other seats start as free
                column.append("F")

        # Add this column to the seat map
        seat_map.append(column)

    # Return the completed 2D seat map
    return seat_map


# Dictionary to convert a column letter to its index in the seat map
COL_TO_INDEX = {"A": 0, "B": 1, "C": 2, "X": 3, "D": 4, "E": 5, "F": 6}

# Dictionary to convert an index back to its column letter
INDEX_TO_COL = {v: k for k, v in COL_TO_INDEX.items()}


def parse_seat(seat_input):
    # This function converts a seat input like "5A" into (row_index, col_index)
    # Returns (None, None) if the input is invalid

    # Remove extra spaces and convert to uppercase
    seat_input = seat_input.strip().upper()

    # The last character is the column letter
    col_letter = seat_input[-1]

    # Everything before the last character is the row number
    row_str = seat_input[:-1]

    # Check the column letter is valid and not the aisle
    if col_letter not in COL_TO_INDEX or col_letter == "X":
        print(f"  Invalid column '{col_letter}'. Valid columns: A, B, C, D, E, F")
        return None, None

    # Try to convert the row part to a number
    try:
        row_num = int(row_str)
    except ValueError:
        # If it is not a number, show an error and return None
        print(f"  Invalid row number '{row_str}'.")
        return None, None

    # Check the row number is in the valid range
    if not (1 <= row_num <= 80):
        print(f"  Row {row_num} is out of range. Must be 1 to 80.")
        return None, None

    # Convert to 0-based indexes and return them
    return row_num - 1, COL_TO_INDEX[col_letter]


def check_availability(seat_map):
    # This function checks the status of a specific seat
    # and prints whether it is free, reserved, an aisle, or storage

    # Ask the user for a seat identifier
    seat_input = input("\n  Enter seat (e.g. 5A, 12D): ").strip()

    # Convert the input to row and column indexes
    row_index, col_index = parse_seat(seat_input)

    # Stop here if the input was invalid
    if row_index is None:
        return

    # Get the current value stored in that seat
    status = seat_map[col_index][row_index]

    # Build a readable seat label like "5A"
    seat_label = f"{row_index + 1}{INDEX_TO_COL[col_index]}"

    # Print the correct message based on the seat status
    if status == "F":
        print(f"  Seat {seat_label} is AVAILABLE.")
    elif status == "X":
        print(f"  {seat_label} is an aisle — cannot be booked.")
    elif status == "S":
        print(f"  {seat_label} is a storage area — cannot be booked.")
    else:
        # Any other value is a booking reference (Part B) or R (Part A)
        print(f"  Seat {seat_label} is RESERVED (Ref: {status}).")



def book_seat(seat_map, conn=None):
    # This function books a free seat
    # conn is None in Part A and a database connection in Part B

    # Ask the user which seat to book
    seat_input = input("\n  Enter seat to book (e.g. 5A, 12D): ").strip()

    # Convert the input to row and column indexes
    row_index, col_index = parse_seat(seat_input)

    # Stop here if the input was invalid
    if row_index is None:
        return

    # Get the current status of that seat
    status = seat_map[col_index][row_index]

    # Build a readable seat label
    seat_label = f"{row_index + 1}{INDEX_TO_COL[col_index]}"

    # Check the seat can actually be booked
    if status != "F":
        if status == "X":
            print(f"  Cannot book {seat_label} — this is an aisle.")
        elif status == "S":
            print(f"  Cannot book {seat_label} — this is a storage area.")
        else:
            # The seat already has a booking
            print(f"  Seat {seat_label} is already reserved (Ref: {status}).")
        return

    if conn is None:
        # Part A: just store "R" in the seat map to mark it as reserved
        seat_map[col_index][row_index] = "R"
        print(f"  Seat {seat_label} has been successfully booked.")

    else:
        # Part B: collect passenger details before booking
        print(f"\n  Booking seat {seat_label}. Please enter passenger details:")
        passport_no = input("  Passport number: ").strip()
        first_name  = input("  First name: ").strip()
        last_name   = input("  Last name: ").strip()

        # Make sure none of the fields are empty
        if not passport_no or not first_name or not last_name:
            print("  Booking cancelled — all fields are required.")
            return

        # Generate a unique 8-character booking reference
        ref = generate_booking_ref(conn)

        # Store the booking reference in the seat map instead of "R"
        seat_map[col_index][row_index] = ref

        # Save the passenger details to the database
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings
            (booking_ref, passport_no, first_name, last_name, seat_row, seat_column)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ref, passport_no, first_name, last_name, row_index + 1, INDEX_TO_COL[col_index]))

        # Save the changes permanently
        conn.commit()

        # Confirm the booking to the user
        print(f"\n  Booking confirmed!")
        print(f"  Seat: {seat_label}")
        print(f"  Booking Reference: {ref}")
        print(f"  Passenger: {first_name} {last_name}")