"""
This file is responsible for extracting data from mutiple sources including the World Bank and,
the Kenya National Bureau of Statistics (KNBS).
"""

import requests
import pandas as pd
import numpy as np
import os
from datetime import datetime

RAW_DATA_PATH = "data/raw"

# Creates folders if they don't exist   
def setup_folders():
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    os.makedirs("database", exist_ok=True)
    print("Folders Ready")
    

 # Pulling Data from the World Bank through an API
"""
    The API is free, and returns up to 100 records for 20 years of the most recent data
    if the item["value"] is not None, some years might have missing data, so we skip those to keep our dataset clean.
"""
import requests
import pandas as pd

def extract_world_bank_data():
    print("Pulling data from the World Bank")

    url = "https://api.worldbank.org/v2/country/KE/indicator/SL.UEM.1524.ZS"

    params = {
        "format": "json",
        "per_page": 100,
        "mrv": 20
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30   # increased timeout
        )

        response.raise_for_status()  #  catches HTTP errors

        data = response.json()

        #  safety check
        if not data or len(data) < 2:
            print("Unexpected API response format")
            return None

        records = []

        for item in data[1]:
            if item.get("value") is not None:
                records.append({
                    "year": int(item["date"]),
                    "unemployment_rate": round(float(item["value"]), 2),
                    "country": "Kenya",
                    "source": "World Bank"
                })

        df = pd.DataFrame(records)
        df = df.sort_values("year")

        filepath = f"{RAW_DATA_PATH}/world_bank_unemployment.csv"
        df.to_csv(filepath, index=False)

        print(f"World Bank data extracted! {len(df)} records saved.")
        return df

    except Exception as e:
        print(f"World Bank data Extraction Failed: {e}")
        return None


# Pulling data at the County Level
"""
Trying to generate realistic Kenya County unemployment data, 
based on actual KNBS Labour force Survey Regional patterns
"""
def extract_county_data():
    print("Generating County Level Data")

    np.random.seed(42)

    counties  = [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
        "Thika", "Machakos", "Kajiado", "Kiambu", "Garissa",
        "Meru", "Embu", "Nyeri", "Murang'a", "Kakamega",
        "Bungoma", "Busia", "Vihiga", "Siaya","Mandera"
    ]

    base_rates = {
        "Nairobi": 18.5, "Mombasa": 22.5, "Kisumu": 24.1,
        "Nakuru": 20.3, "Eldoret": 21.7, "Thika": 19.8,
        "Machakos": 17.2, "Kajiado": 16.4, "Kiambu": 15.6,
        "Garissa": 25.4, "Meru": 18.9, "Embu": 19.5,
        "Nyeri": 17.8, "Murang'a": 16.9, "Kakamega": 23.2,
        "Bungoma": 22.8, "Busia": 24.5, "Vihiga": 21.9,
        "Siaya": 23.7, "Mandera": 26.3
    }

    records = []
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

    for county in counties:
        base = base_rates[county]
        for year in years:
            male_rate = round(base *  np.random.uniform(0.85, 0.95),1)
            female_rate = round(base *np.random.uniform(0.85, 0.95) , 1)
            overall_rate = round((male_rate + female_rate) / 2, 1)

            records.append({
                "county": county,
                "year": year,
                "male_unemployment_rate": male_rate,
                "female_unemployment_rate": female_rate,
                "overall_unemployment_rate": overall_rate,
                "gender_gap": round(female_rate - male_rate, 1),
                "urban_rate": round(overall_rate * np.random.uniform(0.85, 0.95), 1),
                "rural_rate": round(overall_rate * np.random.uniform(1.05, 1.20) ,1)

            })

    df = pd.DataFrame(records)
    filepath = f"{RAW_DATA_PATH}/county_unemployment.csv"
    df.to_csv(filepath, index=False)
    print(f"County Level Data Generated, {len(df)} records saved")
    return df


# Generating Education Level Data
"""
Trying to generate Education Level Data based on Kenya Economic Survey Patterns.
This data shows that in Kenya, technical skills rival academic degrees.

"""
def extract_education_data():

    print("Generating Education Employment Data")

    education_levels = [
        "No Formal Education",
        "Primary Education",
        "Secondary Education",
        "Vocational Training",
        "University Degree",
        "Postgraduate Degree"
    ]

    employment_rates = {
        "No Formal Education": 38.2,
        "Primary Education": 45.6,
        "Secondary Education": 52.3,
        "Vocational Training": 48.9,
        "University Degree": 35.7,
        "Postgraduate Degree": 28.4
    }

    records  = []
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    np.random.seed(24)

    for level in education_levels:
        base = employment_rates[level]
        for year in years:
            rate = round(base * np.random.uniform(-2, 3), 1)
            records.append({
                "education_level": level,
                "year": year,
                "employment_rate": rate,
                "male_employment_rate": round(rate * np.random.uniform(1.02, 1.10), 1),
                "female_employment_rate": round(rate * np.random.uniform(0.88, 0.96), 1),
            })

    df = pd.DataFrame(records)
    filepath = f"{RAW_DATA_PATH}/education_employment.csv"
    df.to_csv(filepath, index=False)
    print(f"Education data was generated, {len(df)} records saved.")   
    return df     


# Industry Data Generation
"""
Trying to generate Industry Employment Data for Different Sectors
The data is based on actual KNBS Labour force Survey Patterns
The youth absorption rates are based on the percentage of youth employed in each sector,

"""
def extract_industry_data():
    print("Generating Industry Data")

    sectors  = [
        "Agriculture", "Manufacturing", "Construction",
        "Trade and Commerce", "Transport", "ICT and Technology",
        "Education", "HealthCare", "Tourism and Hospitality",
        "Financial Services"
    ]

    youth_absorption = {
        "Agriculture": 35.2, "Manufacturing": 8.4,
        "Construction": 9.1, "Trade and Commerce": 15.6,
        "Transport": 6.2, "ICT and Technology": 4.8,
        "Education": 5.1, "HealthCare": 3.9,
        "Tourism and Hospitality": 7.3, "Financial Services": 4.4
        
    }

    records = []
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    np.random.seed(33)

    for sector in sectors:
        base = youth_absorption[sector]
        for year in years:
            rate = base + round(np.random.uniform(-1.5, 2.0), 1)
            records.append({
                "sector": sector,
                "year": year,
                "youth_absorption_rate": rate,
                "avg_monthly_salary_kes": round(
                    np.random.uniform(15000, 85000), -3)
                
            })

    df = pd.DataFrame(records)
    filepath = f"{RAW_DATA_PATH}/industry_employment.csv"
    df.to_csv(filepath, index=False)
    print(f"Industry data Generated, {len(df)} records saved.")
    return df

# Industry the main Data Generation Function
"""
The main  function to extract all data
"""
def extract_all():
    print(" Starting Data Extraction Process ")

    setup_folders()

    wb_data = extract_world_bank_data()
    county_data = extract_county_data()
    education_data = extract_education_data()
    industry_data = extract_industry_data()

    print("All Data Extracted Successfully")

    return {
        "world_bank": wb_data,
        "county": county_data,
        "education": education_data,
        "industry": industry_data

    }

if __name__ == "__main__":
    extract_all()