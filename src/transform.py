"""
This file cleans the data extracted from the other file in the extract.py
"""
import pandas as pd
import numpy as np
import os

RAW_DATA_PATH = "data/raw"

print("Transform module loaded")


"""
This function is going to clean and enrich national unemployment data
"""
def transform_national_data():
    print ("Transforming the world bank data")

    #df = pd.read_csv(f""{RAW_DATA_PATH}/world_bank_unemployment.csv")

    df = df.dropna() # dropping missing value
    df = df.drop_duplicates() # dropping duplicates
    df["year"] = df["year"].astype(int) # converting the year to interger type
    df["unemployment_rate"] = df["unemployment_rate"].astype(float) # Converting the unemployment rate to float datatype

    # Derive Metrics
    df = df.sort_values("year") # sorting the data by year
    df["year_on_year_change"] = df["unemployment_rate"].diff().round(2) # calculating the year on year change in unemployment rate
    df["trend"] = df["unemployment_rate"].rolling(window=3).mean().round(2) #calculating the 3 year rolling average to identify trends

    print(f"National data transformed, {len(df)} records.")   

    return df



"""
This function transforms the County level data and creates a derived column that categorises your data
"""     

def transform_county_data():
    print("Transforiming the County Level Data")

    df =  pd.read_csv(f"{RAW_DATA_PATH}/county_unemployment.csv")

    df = df.dropna()
    df = df.drop_duplicates()
    df["year"] = df["year"].astype(int)   

    # Round all the rate columns
    rate_cols = [
        "overall_unemployment_rate",
        "male_unemployment_rate",
        "female_unemployment_rate",
        "gender_gap",
        "urban_rate",
        "rural_rate"
    ] 

    for col in rate_cols:
        df[col] = df[col].astype(float).round(1)

    # Add Severity Clarification
    # This involves dividing unemployment rates into four different categories which makes the haetmap instantly readable
    df["severity"] = pd.cut(
        df["overall_unemployment_rate"],
        bins = [0, 20, 30, 40, 100],
        labels  = ["low", "Medium", "High", "Severe"]

    )   
    #Add urban rural gap
    df["urban_rural_gap"] = (
        df["rural_rate"] - df["urban_rate"]
    ).round(1)

    print(f"County data Transformed {len(df)} records")
    return df



"""
This function transforms the education level data and categorise educational levels into Primary, Secondary and so forth ...
"""
def transform_education_data():
    print("Transforming Education data ...")

    df = pd.read_csv(f"{RAW_DATA_PATH}/education_unemployment.csv")

    df = df.dropna()
    df = df.drop_duplicates()
    df["year"] = df["year"].astype(int)

    rate_cols = [
        "employment_rate",
        "male_employment_rate",
        "female_employment_rate"
    ]
    for col in rate_cols:
        df[col] = df[col].astype(float).round(1)

    # Gender employment gap per education level
    df["gender_employment_gap"] = (
        df["male_employment_rate"] - df["female_employment_rate"]
    ).round(1)

    #Education Order For Charts
    education_order = [
        "No Formal Education",
        "Primary Education",
        "Secondary Education",
        "University Degree",
        "Postgraduate"
    ]
    df["education_level"] = pd.Categorical(
        df["education_level"],
        categories = education_order,
        ordered=True
    )
    df = df.sort_values(["education_level", "year"])

    print(f"Education data transformed, {len(df)} records.")
    return df


"""
This function transforms the industry level data and categorises the data according to salary range

"""
def transform_industry_data():
    print("Transforming Industry data")

    df = pd.read_csv(f"{RAW_DATA_PATH}/industry_employment.csv")

    # Cleaning the data
    df = df.dropna()
    df = df.drop_duplicates()
    df["year"] = df["year"].astype(int)
    df["youth_absorption_rate"] = df["youth_absorption_rate"].astype(float).round(1)
    df["avg_monthly_salary_kes"] = df["avg_monthly_salary_kes"].astype(float).round(0)

    # Salary Tier Classification
    df["salary_tier"] = pd.cut(
        df["avg_monthly_salary_kes"],
        bins = [0, 25000, 50000, 75000, 200000],
        labels = ["Entry_Level", "Mid_Level", "Senior_Level", "Executive"]
    )

    print(f"Industry data Transformed {len(df)} records.")
    return df

# Transform function
"""
Thi

"""
def transform_all():
    print("Starting data transformation..")

    #national = transform_national_data()
    county = transform_county_data()
    education = transform_education_data()
    industry = transform_industry_data()

    print("All data transformed successfully")

    return {
        #"national": national,
        "county": county,
        "education": education, 
        "industry": industry
    }


if __name__ == "__main__":
    data = transform_all()

    print(data).head()