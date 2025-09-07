# This script connects to the database and displays all registered users
# in a clean, readable format using the pandas library.

import mysql.connector
import pandas as pd
from mysql.connector import errorcode

# --- Database Configuration ---
DB_NAME = "circle"
DB_USER = "root"
DB_PASSWORD = "cseds@32"
DB_HOST = "localhost"

def view_users():
    """
    Connects to the database and prints all users from the 'users' table.
    """
    try:
        # Connect to the MySQL database
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cursor = cnx.cursor()
        print(f"✅ Connected to MySQL database '{DB_NAME}'.")

        # Execute a query to select all data from the users table
        query = "SELECT id, name, email FROM users"
        cursor.execute(query)

        # Fetch all the records
        records = cursor.fetchall()
        
        if records:
            # Get column names from the cursor description
            columns = [col[0] for col in cursor.description]
            
            # Create a pandas DataFrame for a clean display
            df = pd.DataFrame(records, columns=columns)
            
            print("\n--- Registered Users ---")
            print(df)
            print("\n------------------------")
        else:
            print("\nNo users found in the database.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("❌ Database does not exist. Please run setup_db.py first.")
        else:
            print(f"❌ Error: {err}")

    finally:
        # Close the connection and cursor
        if 'cnx' in locals() and cnx.is_connected():
            cursor.close()
            cnx.close()
            print("Database connection closed.")

if __name__ == '__main__':
    view_users()
