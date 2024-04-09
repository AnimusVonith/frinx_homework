import pandas as pd
import psycopg2
import json
import os

# Get database connection details from environment variables
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

def db_insert(holder):
    """
    Function to insert data into the PostgreSQL database.
    
    Parameters:
        holder (tuple): Tuple containing data to be inserted into the database.
    """
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASS,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        # Create a cursor object
        cur = conn.cursor()

        # Insert data into the table, excluding the 'id' column
        sql = """
        INSERT INTO frinx_configs (name, description, max_frame_size, config, port_channel_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        # Execute the SQL query
        cur.execute(sql, holder)

        # Get the generated 'id' value
        inserted_id = cur.fetchone()[0]

        # Commit the transaction
        conn.commit()

        print("Data inserted successfully with ID:", inserted_id)

    except (Exception, psycopg2.Error) as error:
        print("Error while inserting data:", error)

    finally:
        # Close communication with the database
        if conn is not None:
            cur.close()
            conn.close()

def main():
    # Read JSON data from file
    df = pd.read_json("configClear_v2.json")

    # Extract relevant data from the JSON structure
    df = df["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]

    # Iterate over the extracted data
    for key in df.keys():
        if str(key).lower() == "bdi" or str(key).lower() == "loopback":
            # Skip bdi and loopback interfaces
            continue
        for interface in df[key]:
            # Extract data for each interface
            name = str(key) + str(interface.get("name", ""))
            desc = interface.get("description", None)
            mtu = interface.get("mtu", None)
            config = interface
            port_channel_id = interface.get("Cisco-IOS-XE-ethernet:channel-group", {}).get("number", None)

            # Prepare data for database insertion
            holder = (name, desc, mtu, json.dumps(config), port_channel_id)
            
            # Call the function to insert data into the database
            db_insert(holder)

if __name__ == "__main__":
    main()
