"""
This file is the visual layer of the whole project.
It reads data directly from thr sqlite database and displays 6 interactive charts thate tells the story of unemployment in Kenya.
Generates AI policy insights on demand using plain English.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import sys
import os

# Add src folder to path so we can import ai_insights
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

DATABASE_PATH = "database/employment.db"

st.set_page_config(
    page_title = "Kenya Youth Employment Intelligence",
    page_icon = "🇰🇪",
    page_layout = "wide"
)
st.title("🇰🇪 Kenya Youth Employment Intelligence Platform")
st.markdown("AI-powered insights on youth unemployment across Kenya(Built for policymakers and development organisations)")
st.markdown("---")

# Database Connection and Data Loading from sqlite database
@st.cache_data
def load_data():
    conn = sqlite3.connect(DATABASE_PATH)

    national = pd.read_sql("select * from world_bank_unemployment", conn)
    county = pd.read_sql("select * from county_unemployment", conn)
    education = pd.read_sql("select * from education_employment", conn)
    industry = pd.read_sql("select * from industry_employment", conn)

    conn.close()
    return national, county, education, industry

national_df, county_df, education_df, industry_df = load_data()


# Adding Filters to the Dashboard
"""
reverse = True -> shows most recent year first in the dropdown
.unique() -> gets all unique values in the dataset, automatically includes new years when pipeline runs
toList() converts it to a list
"""
st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("---")

selected_year = st.sidebar.selectbox(
    "Select Year",
    options = sorted(county_df["year"].unique(), reverse=True)
    
)

selected_county = st.sidebar.selectbox(
    "Select County",
    options = ["All Counties"] + sorted(county_df["county"].unique().tolist())
)

st.sidebar.markdown("---")
st.sidebar.markdown("Data Sources")
st.sidebar.markdown("World Bank Open Data")
st.sidebar.markdown("Kenya Economic Survey")
st.sidebar.markdown("---")
st.sidebar.markdown("Pipeline runs every Monday 8:00 am via Apache Airflow")

# Adding a subheader
"""
This section is the subheader of the dashboard
st.metric has a delta parameter that shows a change indicator
positive delta -> green arrow
negative delta -> red arrow
idxmax() and idxmin() returns the index of the highest value and the lowest value
Then .loc[index, 'county'] gets the county name at that index
"""
st.subheader("National Overview")

latest_national = national_df.sort_values("year").iloc[-1]
latest_county = county_df[county_df["year"] == selected_year]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label = "National Youth Unemployment",
        value = f"{latest_national['unemployment_rate']}%",
        delta = f"{latest_national['year_on_year_change']}% YoY"
    )

with col2:
    st.metric(
        label = "Highest County",
        value = latest_county.loc[latest_county['overall_unemployment_rate'].idxmax(), 'county'],
        delta = f"{latest_county["overall_unemployment_rate"].max()}%"
    )    
with col3:
    st.metric(
        label = "Lowest County",
        value = latest_county.loc[latest_county['overall_unemployment_rate'].idxmin(), 'county'],
        delta = f"{latest_county['overall_unemployment_rate'].min()}%"
    )
with col4:
    avg_gender_gap = round(latest_county["gender_gap"].mean(), 1)
    st.metric(
        label = "Avg Gender Gap",
        value = f"{avg_gender_gap}%",
        delta = "Female higher"
    )   
with col5:
    avg_urban_rural = round(latest_county["urban_rural_gap"].mean(), 1)
    st.metric(
        label = "Urban-Rural Gap",
        value = f"{avg_urban_rural}%",
        delta = "Rural Higher"
    )     

st.markdown("---")    