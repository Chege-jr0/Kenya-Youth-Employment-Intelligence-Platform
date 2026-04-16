from airflow.sdk import dag, task
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@dag(
    dag_id = "kenya_employment_pipeline",
    description = "Weekly Kenya Youth Employment Data Pipeline",
    schedule = "08**1", #Every Monday at 0800hrs
    start_date = datetime(2026, 1, 1),
    catchup = False,
    tags = ["kenya", "employment", "youth", "dalberg"],
    default_args = {
        "retries": 2,
        "retry_delay": timedelta(minutes = 5)
    }
)

def kenya_employment_pipeline():
    """
    Kenya Youth Employment Intelligence Pipeline

    Runs every Monday at 8:00 AM to:
    1. Extract data from World Bank API and KNBS Sources
    2. Transform and clean the data
    3. Load into SQLite database
    4. Dashboard automatically reflects updated data
    """
# Pulls data from World Bank API and the KNBS simulation data
    @task()
    def extract():
        """Step 1 - Extract raw data from all sources."""
        from extract import extract_all
        print("Starting extraction ...")
        result = extract_all()
        print(f"Extraction Complete!")
        return {
            "national_records": len(result["world_bank"]),
            "county_records": len(result["county"]),
            "education_records": len(result["education"]),
            "industry_records": len(result["industry"])
        }
    
# Cleans and enriches the data  
    @task()
    def transform(extraction_summary: dict):
        """Step 2 - Clean and transform extracted data."""
        from transform import transform_all
        print("Starting transformation...")
        print(f"Processing: {extraction_summary}")
        data = transform_all()
        print("Transformation complete")
        return {
            "national_records": len(data["national"]),
            "county_records": len(data["county"]),
            "education_records": len(data["education"]),
            "industry_recoords": len(data["industry"])
        }
    
# Stores clean data in SQLite    
    @task()
    def load(trasnformation_summary: dict):
        """Step 3 - Load clean data into SQLite database."""
        from load import load_all
        print("Starting data load...")
        print(f"Loading: {trasnformation_summary}")
        load_all()
        print("Data loaded successfully")
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "records_loaded": trasnformation_summary
        }
# Checks all tables have records, pipeline fails if empty    
    @task()
    def validate(load_summary: dict):
        """Step 4 - Validate data was loaded correctly."""
        import sqlite3
        import pandas as pd

        print("Validating database ...")

        DATABASE_PATH = "database/employment.db"
        conn = sqlite3.connect(DATABASE_PATH)

        tables = [
            "national_unemployment",
            "county_unemployment",
            "education_employment",
            "industry_employment"
        ]

        validation_results = {}
        all_passed = True

        for table in tables:
            try:
                count = pd.read_sql(
                    f"SELECT COUNT(*) AS total FROM {table}",
                    conn
                )
                records = int(count["total"][0])
                validation_results[table] = records
                print(f"{table}: {records} records")

                if records == 0:
                    all_passed = False
                    print(f"{table}: EMPTY - pipeline may have failed!")


            except Exception as e:
                validation_results[table] = 0
                all_passed = False
                print(f" Failed {table}: Error - {e}")

        conn.close()

        if all_passed:
            print("All validation checks passed!")
        else :
            raise  ValueError("Validation failed - some tables are empty!")

        return {
            "validation_passed": all_passed,
            "table_counts": validation_results,
            "pipeline_completed_at": datetime.now().isoformat()
        }     
    # Define task dependencies
    extraction_summary = extract()
    transformation_summary = transform(extraction_summary)
    load_summary = load(transformation_summary)     
    validate(load_summary)

#Instantiate the DAG     
kenya_employment_pipeline()   
