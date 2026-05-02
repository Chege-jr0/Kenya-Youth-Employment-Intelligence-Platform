import pandas as pd
import datetime as datetime
import numpy as np


# Defining the markets and cities
CITIES = ["Nairobi", "Mombasa", "Kisumu", "Eldoret", "Nakuru"]

PROPERTY_TYPES = ["Residential", "Land", "Commercial"]

NEIGHBORHOODS = {
    "Nairobi": ["Westlands", "Karen", "Langata", "Runda", "Kilimani"],
    "Mombasa": ["Nyali", "Kongowea", "Likoni", "Mvita", "Changamwe"],
    "Kisumu": ["Milimani", "Kondele", "Nyamasaria", "Kibuye", "Obunga"],
    "Eldoret": ["Kapsoya", "Kipkaren", "Langas", "Huruma", "Kimumu"],
    "Nakuru": ["Milimani", "Kivumbini", "Rhoda", "Flamingo", "Biashara"]
}

# Defining the function with the simulated data
def  generate_market_data ():
    np.random.seed(42)  
    # This makes our random data consistent every time the app runs
    # Without this, the data would change every time we run the app, which is not ideal for testing and development
    # 42 is just a convention, any number works as long as it's the same every time.

    base_prices  = {
        "Nairobi" : {
            "Residential" : 12500000,
            "Land" : 45000000,
            "Commercial" : 25000000
        },
        "Mombasa" : {
            "Residential" : 8500000,
            "Land" : 30000000,
            "Commercial" : 15000000
        },
        "Kisumu" : {
            "Residential" : 5500000,
            "Land" : 180000000,
            "Commercial" : 80000000
        },
        "Eldoret" : {
            "Residential" : 4500000,
            "Land" : 12000000,
            "Commercial" : 6000000
        },
        "Nakuru" : {
            "Residential" : 65000000,
            "Land" : 220000000,
            "Commercial" : 10000000
        }

        
    }

    quarters = [
         "Q1 2022", "Q2 2022", "Q3 2022", "Q4 2022",
         "Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023",
         "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"
        ]

    records = []

    # There are 3 loops here, for city, for prop_type, for i in quarter, list for the quarters
    # for each quarter, calaculate growth, and the records
    for city in CITIES:
            for prop_type in PROPERTY_TYPES:
                base = base_prices[city][prop_type]
                for i, quarter in enumerate(quarters):
                    growth = 1 + (0.02 * i) + np.random.uniform(-0.01, 0.03)
                    price = base * growth
                    records.append({
                        "City" : city,
                        "Property Type" : prop_type,
                        "Quarter" : quarter,
                        "Avg_Price_KES" : round(price),
                        "Rental_Yield": round(np.random.uniform(5.5, 9.5), 2),
                        "Occupanncy_Rate": round(np.random.uniform(70, 95), 1),
                        "Transactions": np.random.randint(50, 500),
                        "Price_Per_Sqft": round(price / np.random.uniform(800, 2000))
                    })

    return pd.DataFrame(records)

# Getting the latest summary for a specific city
def get_city_summary(df, city):
    latest_quarter = df["Quarter"].iloc[-1]
    city_data = df[(df["City"] == city) & (df["Quarter"] == latest_quarter)]
    return city_data

#Getting the price trend over time for a city and propeerty type
def get_price_trend(df, city, prop_type):
    filtered = df[
        (df["City"] == city) & (df["Property_Type"] == prop_type)
    ]
    return filtered[["Quarter", "Avg_Price_KES"]]

# Getting the market overview for a city
def get_market_overview(df):
    latest_quarter =  df["Quarter"].iloc[-1]
    return df[df["Quarter"] == latest_quarter]

# Getting the top performing city based on rental yield
def get_top_performing_city(df):
    latest = get_market_overview(df)
    top = latest.groupby("City")["Rental_Yield"].mean().idxmax()
    return top

# Getting the summary statistics across the whole market
def get_summary_stats(df):
    latest = get_market_overview(df)
    summary = {
        "Avg_Price_KES": round(latest["Avg_Price_KES"].mean()),
        "Avg_Rental_Yield": round(latest["Rental_Yield"].mean(), 2),
        "Occupancy_Rate": round(latest["Occupancy_Rate"].mean(), 1),
        "Transactions": round(latest["Transactions"].sum()),
        "top_city": get_top_performing_city
    }
    return summary
