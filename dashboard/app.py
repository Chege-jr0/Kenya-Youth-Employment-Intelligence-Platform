
# This file is the visual layer of the whole project.
# It reads data directly from thr sqlite database and displays 6 interactive charts thate tells the story of unemployment in Kenya.
# Generates AI policy insights on demand using plain English.

import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3
import sys
import os

# Add src folder to path so we can import ai_insights
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)

if project_root not in sys.path:
    sys.path.insert(0, project_root)    

from  src.ai_insights import generate_employment_insights, ask_employment_question    

DATABASE_PATH = "database/employment_db"

st.set_page_config(
    page_title = "Kenya Youth Employment Intelligence",
    page_icon = "🇰🇪",
    layout = "wide"
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
# reverse = True -> shows most recent year first in the dropdown
# .unique() -> gets all unique values in the dataset, automatically includes new years when pipeline runs
# toList() converts it to a list

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

# Building context for the AI
def build_context():
    return {
        "national_rate": float(latest_national["unemployment_rate"]),
        "year_on_year": float(latest_national["year_on_year_change"])
                        if pd.notna(latest_national["year_on_year_change"])
                        else 0.0,
        "worst_county": str(latest_county.loc[
            latest_county["overall_unemployment_rate"].idxmax(), "county"
        ]),
        "worst_rate": float(latest_county["overall_unemployment_rate"].max()),
        "best_county": str(latest_county.loc[
            latest_county["overall_unemployment_rate"].idxmin(), "county"
        ]),
        "best_rate": float(latest_county["overall_unemployment_rate"].min()),
        "avg_gender_gap": float(avg_gender_gap),
        "selected_year": int(selected_year)
    }


# Adding a subheader

# This section is the subheader of the dashboard
# st.metric has a delta parameter that shows a change indicator
# positive delta -> green arrow
# negative delta -> red arrow
# idxmax() and idxmin() returns the index of the highest value and the lowest value
# Then .loc[index, 'county'] gets the county name at that index


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



# add_hline() used to show a horizontal reference line across the chart using the mean


st.subheader("Youth Unemployment Trends and County Analysis")

col1, col2 = st.columns(2)

with col1:
    fig_national = px.line(
        national_df.sort_values("year"),
        x = "year",
        y = "unemployment_rate",
        title = "National Youth Unemployment Rate(2019 - 2025)",
        labels = {
            "unemployment_rate": "Unemployment Rate(%)",
            "year": "Year"
        },
        markers = True,
        color_discrete_sequence = ["#E63946"]
    )

    fig_national.add_hline(
        y = national_df["unemployment_rate"].mean(),
        line_dash = "dash",
        line_color = "gray",
        annotation_text = "Average"
    )
    fig_national.update_layout(
        plot_bgcolor = "white",
        yaxis_ticksuffix = "%"
    )

    st.plotly_chart(fig_national, use_container_width = True)

with col2:
    county_sorted = latest_county.sort_values(
        "overall_unemployment_rate",
        ascending =  False
    )

    fig_county = px.bar(
        county_sorted,
        x = "overall_unemployment_rate",
        y = "county",
        orientation = "h",
        title = f"Youth Unemployment by County ({selected_year})",
        labels = {
            "overall_unemployment_rate": "Unemployment Rate(%)",
            "county": "County"
        },
        color = "overall_unemployment_rate",
        color_continuous_scale = "RdYlGn"
    )
    fig_county.update_layout(
        plot_bgcolor = "white",
        xaxis_ticksuffix = "%"
    )
    st.plotly_chart(fig_county, use_container_width = True)

    st.markdown("---")





st.subheader("Gender Gap and Urban-Rural Divide")

col1, col2 = st.columns(2)

with col1:
    
   #  If a specific county is selected, it shows the county gender gap,
   #  if all counties selected, show the national average gender gap.
    

    if selected_county != "All Counties":
        gender_data = county_df[county_df["county"] == selected_county]
        title_suffix = selected_county
    else:
        gender_data = county_df.groupby("year")[
            ["male_unemployment_rate", "female_unemployment_rate"]
        ].mean().reset_index()
        title_suffix = "All Counties"

    fig_gender = px.line(
        gender_data,
        x = "year",
        y = ["male_unemployment_rate", "female_unemployment_rate"],
        title = f"Gender Gap in Youth Employment - {title_suffix}",
        labels = {
            "value": "Unemployment Rate (%)",
            "year": "Year",
            "variable": "Gender"
        },
        markers = True,
        # This maps specific colors to specific variables.
        color_discrete_map = {
            "male_unemployment_rate": "#2196F3",
            "female_unemployment_rate": "#E91E63"
        }
    )  
    fig_gender.update_layout(
        plot_bgcolor = "white",
        yaxis_ticksuffix = "%"
    ) 

    st.plotly_chart(fig_gender, use_container_width = True)

with col2:
    urban_rural = county_df[county_df["year"] == selected_year].groupby("county")[
        ["urban_rate", "rural_rate"]
    ].mean().reset_index()

    fig_urban = px.bar(
        urban_rural.head(10),
        x = "county",
        y = ["urban_rate", "rural_rate"],
        title = f"Urban vs Rural Unemployment ({selected_year})",
        labels ={
            "value": "Unemployment Rate(%)",
            "county": "County",
            "variable": "Area Type"
        },
        barmode = "group",
        color_discrete_map = {
            "urban_rate": "#FF9800",
            "rural_rate": "#4caf50",
        }
    ) 
    fig_urban.update_layout(
        plot_bgcolor = "white",
        yaxis_ticksuffix = "%"
    ) 
    st.plotly_chart(fig_urban, use_container_width = True)



st.subheader("Education and Industry Insights")

col1, col2 = st.columns(2)

with col1:
    education_latest = education_df[
        education_df["year"] == selected_year
    ].sort_values("employment_rate", ascending = False)

    fig_education = px.bar(
        education_latest,
        x = "employment_rate",
        y = "education_level",
        orientation = "h",
        title = f"Employment Rate by Education Level({selected_year})",
        labels = {
            "employment_rate": "Employment Rate (%)",
            "education_level": "Education Level"
        },
        color = "employment_rate",
        color_continuous_scale = "Blues",
        text = "employment_rate"
    )
    fig_education.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_education.update_layout(
        plot_bgcolor = "white",
        xaxis_ticksuffix = "%"
    )
    st.plotly_chart(fig_education, use_container_width =  True)

    with col2:
        industry_latest = industry_df[
            industry_df["year"] == selected_year
        ].sort_values("youth_absorption_rate", ascending = False)

        fig_industry = px.bar(
            industry_latest,
            x = "sector",
            y = "youth_absorption_rate",
            title = f"Youth Absorption by Industry ({selected_year})",
            labels = {
                "youth_absorption_rate": "Youth Absorption Rate(%)",
                "sector": "Industry Sector"
            }, 
            color = "youth_absorption_rate",
            color_continuous_scale = "Viridis",
            text = "youth_absorption_rate"
        )
        fig_industry.update_traces(
            texttemplate = "%{text}%",
            textposition = "outside"
        )
        fig_industry.update_layout(
            plot_bgcolor = "white",
            xaxis_tickangle = -45,
            yaxis_ticksuffix = "%"
        )
        st.plotly_chart(fig_industry, use_container_width=True)

st.markdown("---")

st.subheader("AI Policy Insights")

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Generate Policy Insights"):
        with st.spinner("Analysing Kenya Employment data ..."):
            try:
                context = build_context()
                insights = generate_employment_insights(context)
                st.success("AI Policy Analysis")
                st.write(insights)

            except Exception as e:
                st.error(f"AI unavailable, Make sure Ollama is running")
                    
with col2:
    st.info("""
How to use:
            
1. Use sidebar filters to focus on specific year or county
2. Click Generate Policy Insights for AI Analysis
3. Or ask you own question

    Example Question
- Which county need the most urgent intervention?
- What is driving the gender gap?
- Which Industry should the youth target?
                                    
""")      
    st.markdown("---")
    st.subheader("Ask the AI anything about Kenya Youth Employment")

    question = st.text_input(
         "Type your Question:",
         placeholder = "eg. Which county has the worst female unemployment? What drives rural employment?"

    )
    if st.button("Ask AI"):
        if question == "":
            st.warning("Please type a question first!")
        else:
            with st.spinner("Thinking, a minute please"):
                try:
                    context = build_context()
                    answer = ask_employment_question(question, context)
                    st.success("After doing some research:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"AI unavailable. Make sure Ollama is running. {e}")


# Footer Section
st.markdown("---")
st.subheader("Raw Data Explorer")

table_choice = st.selectbox(
    "Select data to explore:",
    options = [
       "National Unemployment",
       "County Unemployment",
       "Education Employment",
       "Industry Employment" 
    ]
)

if st.checkbox("Show Raw Data"):
    if table_choice == "National Unemployment":
        st.dataframe(national_df, use_container_width = True)
    elif table_choice == "County Unemployment":
        if selected_county != "All Counties":
            st.dataframe(
                county_df[county_df["county"] == selected_county],
                use_container_width = True
            )    
        else:
            st.dataframe(
                county_df[county_df["year"] == selected_year],
                use_container_width = True
            )  
    elif table_choice == "Education Employment":
        st.dataframe(
            education_df[education_df["year"] == selected_year],
            use_container_width = True
        )  
    elif table_choice == "Industry Employment":
        st.dataframe(
            industry_df[industry_df["year"] == selected_year],
            use_container_width = True
        )  

st.markdown("---")
st.caption("""
Kenya Youth Employment Intelligence Platform || Built with Streamlit, Plotly, SQLite, Apache Airflow and Ollama || Data: KNBS, World Bank, Kenya Economic Survey
""")    
st.caption("""Built by Paul Gikonyo || Data Analyst@Everything Data Africa""")    
