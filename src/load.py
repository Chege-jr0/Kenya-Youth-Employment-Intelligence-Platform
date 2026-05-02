"""
The Database Manager
This file takes the transformed data and loads it into a database.
Think of it like saving your Excel sheets into a proper database
We can use PostgreSQL, MySQL but for this, we need to setup the server.
For SQLite, we dont need to set up the server
"""

import pandas as pd
import sqlite3
import os
from transform import transform_all

DATABASE_PATH = "database/employment_db"

"""
This function creates a connection with the SQLite database
It also creates a directory for the database if it does not exist
"""
def get_connection():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


"""
This function loads the transformed data to the sqlite database.
The name will be the name of the table in the database.
if the table exists, replace it and create a new one.
And then we use pd.read_sql reads the table and returns the result.

"""
def load_world_bank_data(conn, df):
    print("Loading and Transforming World_bank data")

    df.to_sql(
        name = "world_bank_unemployment",
        con = conn,
        if_exists = "replace",
        index = False
    )

    count = pd.read_sql("SELECT COUNT(*) AS total FROM world_bank_unemployment", conn)
    print(f"World Bank data loaded {count['total'][0]} records in database.")

"""
This function loads the county data and creates a table in the database
"""
def load_county_data(conn, df):
    print("Loading County data..")

    df["severity"] = df["severity"].astype(str)

    df.to_sql(
        name = "county_unemployment",
        con = conn,
        if_exists = "replace",
        index = False
    )

    count = pd.read_sql("SELECT COUNT (*) AS total FROM county_unemployment", conn)
    print(f"County data loaded {count['total'][0]} records in database")


    """
    This method loads the education data and creates a table in the database if there is one
    """
def load_education_data(conn, df):
    print("Load Education data")

    df["education_level"] = df["education_level"].astype(str)

    df.to_sql(
        name = "education_employment",
        con =conn,
        if_exists = "replace",
        index = False
    )
    count = pd.read_sql("select count(*) as total from education_employment", conn)
    print(f"Education data loaded {count['total'][0]} records in database.")


"""
This function loads the industry data into sqlite database
SQlite doesn't understand basic types like text, numbers and dates, thats why we converted to str for thr categorical values we created.
"""    
def load_industry_data(conn, df):
    print("Loading Industry data ...")

    df["salary_tier"] = df["salary_tier"].astype(str)

    df.to_sql(
        name = "industry_employment",
        con = conn,
        if_exists = "replace",
        index = False
    )

    count = pd.read_sql("SELECT COUNT(*) AS total FROM industry_employment", conn)
    print(f"Industry data loaded! {count['total'][0]} records in database.")


"""
Verify in the database whether what we created is really there.
Loops through all the tables and runs a query to count all the rows and returns it as the summary
"""

def verify_database(conn):
    print("Database Summary: ")
    print("-" * 40)

    tables = [
        "world_bank_unemployment",
        "county_unemployment",
        "education_employment",
        "industry_employment"
    ]

    for table in tables:
        try:
            count = pd.read_sql(f"select count (*) as total from {table}", conn)
            print(f"{table}: {count['total'][0]} records")
        except Exception as e:
            print(f"{table}: Error - {e}")

    print("-" * 40)          

"""
This is the main load function which loads all the function and to excute
"""

def load_all():
    print("Starting data load...")
    print("-" * 40)

    #Step 1 - Transform all the data in our previous file
    data = transform_all()

    # Step 2 - Connect to the database
    conn = get_connection()

    # Step 3 - Load each dataset
    load_world_bank_data(conn, data["national"])
    load_county_data(conn, data["county"])
    load_education_data(conn, data["education"])
    load_industry_data(conn, data["industry"])

    # Step 4 - Verify the database is storing correctly
    verify_database(conn)

    #Step 5 - Close the Connection
    # .close() is an inbuilt method that closes the function
    conn.close()
    print("Database connection closed!")
    print("ETL Pipeline Complete")

if __name__ == "__main__":
     load_all()
