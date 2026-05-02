# The app.py pulls data from the data.py and gets insights from the ai_insights.py and displays it on a beatiful interactive dashboard
# plotly creates beautiful interactive charts, unlinke matplotlib
import streamlit as st
import plotly.express as px
import pandas as pd
from data import (
    generate_market_data,
    get_city_summary,
    get_price_trend,
    get_market_overview,
    get_summary_stats,
    CITIES,
    PROPERTY_TYPES
)
from ai_insights import generate_market_insights, ask_market_question

st.set_page_config(
    page_title = "Kenya Real Estate Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("Kenya Real Estate Market Dashboard")
st.markdown("AI-powered marker intelligence for Kenyan Property Investors")
st.markdown("---")

# Without cache, the once the user clicks the slicer, the data refreshes from the pipeline but with cache, tha data loads from the cache without waiting.

@st.cache_data
def load_data():
    return generate_market_data()

df = load_data()
stats = get_summary_stats(df)

# Dasboard Filters
st.sidebar.title("Dasboard Filters")
st.sidebar.markdown("---")

selected_city = st.sidebar.selectbox(
    "Select City",
    options = ["All Cities"] + CITIES
)

selected_property = st.sidebar.selectbox(
    "Select Propert Type",
    options=["All Types"] + PROPERTY_TYPES
)

st.sidebar.markdown("---")
st.sidebar.markdown("About this Dashboard")
st.sidebar.markdown("Data Covers Q1 2022 TO Q4 2024 across 5 major cities in Kenya")



# This is the KPI Section that appears at the Top of the Dashboard
st.subheader("Market Overview - Q4 2024")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
    )

with col2:
    st.metric(
        label = "Avg Rental Yield",
        value = f"{stats['rental_yield']}%"
    )

with col3:
    st.metric(
        label = "Avg Occupancy Rate",
        value = f"{stats['occupancy_rate']}%"
    )

with col4:
    st.metric(
        label = "Total Transactions",
        value = f"{stats['total_transactions']:,}"
    )

with col5:
    st.metric(
        label = "Top Performing City",
        value = f"{stats['top_city']}"
    )
st.markdown("---")    



#Chart 1 - Price Trends Line Chart
st.subheader("Property Price Trends Over Time")

# Apply filters BEFORE creating columns
city_for_trend = selected_city if selected_city != "All Cities" else "Nairobi"
prop_for_trend = selected_property if selected_property != "All Types" else "Residential"
trend_data = get_price_trend(df, city_for_trend, prop_for_trend)

col1, col2 = st.columns(2)

with col1:
    fig_line = px.line(
        trend_data,
        x="Quarter",
        y="Avg_Price_KES",
        title=f"{city_for_trend} — {prop_for_trend} Price Trend",
        labels={
            "Avg_Price_KES": "Average Price (KES)",
            "Quarter": "Quarter"
        },
        markers=True,
        color_discrete_sequence=["#2E86AB"]
    )
    fig_line.update_layout(
        plot_bgcolor="white",
        yaxis_tickformat=",",
        value = stats['top_city']
    )
st.markdown("---")    

#Chart 1 - Price Trends Line Chart
st.subheader("Property Trends Over Time")
col1, col2 = st.columns(2)

with col1: 
    city_for_trend = selected_city if selected_city != "All Cities" else "Nairobi"
    prop_for_trend = selected_property if selected_property != "All Types" else "Residential"

    trend_data = get_price_trend(df, city_for_trend, prop_for_trend)

    fig_line = px.line(
        trend_data,
        x="Quarter",
        y="Ävg_Price_KES",
        title= f"{city_for_trend} - {prop_for_trend} Price Trend",
        labels={"Avg_Price_KES": "Average Price (KES)", "Quarter": "Quarter"},
        markers=True, #Adds a dot to each data point
        color_discrete_sequence=["#2E86AB"]
    )

    fig_line.update_layout(
        plot_bgcolor="white", #white background
        yaxis_tickformat = "," #Formats the Y-axis with commas

    )
    st.plotly_chart(fig_line, use_container_width=True)


    # Chart 2 - City Comparison Bar Chart
    with col2:
        overview_data = get_market_overview(df)

        if selected_property != "All Types": #If selected, make the chart respond to filters dynamically
            overview_data = overview_data[overview_data["Property_Type"] == selected_property]

        fig_bar = px.bar(
            overview_data, 
            x="City",
            y="Avg_Price_KES",
            color = "Property_Type",
            title =  "Current Prices by City and Property Type",
            labels={"Avg_Price_KES": "Average Price (KES)", "City": "City"},
            barmode="group",
            color_discrete_sequence=["#2E86AB", "#A23B72", "#F18F01"] 
        )  

        fig_bar.update_layout(
            plot_bgcolor = "white",
            yaxis_tickformat = ","
        )  

        st.plotly_chart(fig_bar, use_container_width=True)

# Rental Yield HeatMap
# The Pivot table turns your data to a gridformat city as columns, property as rows.
# px.imshow creates a heatmap color Red=low yield, Yellow=medium, Green=high yield.
st.markdown("---")
st.subheader("Rental Yield HeatMap by City and Property Type")


st.caption(""""
           
           Green: High Rental Yield(Best Returns)

           Yellow: Average Rental Yield

           Red: Low Rental Yield(Lowest Returns)""")

heatmap_data = get_market_overview(df).pivot_table(
    values = "Rental_Yield",
    index = "Property_Type",
     columns = "City",
    aggfunc = "mean"

).round(2)

fig_heatmap = px.imshow(
    heatmap_data,
    title = "Average Rental Yield - Q4 2024",
    color_continuous_scale = "RdYlGn",
    aspect = "auto",
    text_auto=True,
     labels={"Property_Type": "Property Type", "City": "City"}

)

fig_heatmap.update_layout(
    plot_bgcolor="white"
)


st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")


#AI SECTION

# AI insights Section
st.subheader("AI Market Insights")

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Generate Market Insights"):
        with st.spinner("Analysing the Market.. "):
            city = selected_city if selected_city != "All Cities" else None
            prop = selected_property if selected_property != "All Cities" else None
            insights = generate_market_insights(stats, city, prop)
        st.success("AI Analysis Complete")
        st.write(insights)    

with col2:
    st.info("""
    How to use: 
1. Use the sidebar filters to focus on a specific city or property type.
2. Click Generate Insights for AI Analysis.
3. Or ask your own question below.
                                    
""")   


# ASK the AI Anything
st.markdown("---")
st.subheader("Ask the AI Anything about the Market")

question = st.text_input(
    "Type your Question Here:",
    placeholder="Which City has the best rental yield? Is Mombasa  a good investment?"
)

if st.button("Ask AI"):
    if question == "":
        st.warning("Plaese type a question first!")

    else:
        with st.spinner("Thinking"):
            city = selected_city if selected_city != "All Cities" else None
            prop = selected_property if selected_property != "All Types" else None
            answer = ask_market_question(question, stats, city, prop) 
        st.success("Answer: ") 
        st.write(answer)    

 

# Raw Table Section of the Charts
st.markdown("---")
st.subheader("Raw Market Data")

if st.checkbox("Show Raw Data"):
    if selected_city != "All Cities":
        display_df = df[df["City"] == selected_city]

    else:
        display_df = df

    if selected_property != "All Types":
        display_df = df[df["Property_Type"] == selected_property]   

    st.dataframe(display_df, use_container_width=True) 
    st.caption(f"Showing {len(display_df)} records")      

st.markdown("---")
st.caption("Kenya Real Estate Dashboard | Built with Streamlit, Plotly and Ollama(model = tinyllama)")
st.caption("Made by PAUL GIKONYO (Data Analyst)")
st.plotly_chart(fig_heatmap, use_container_width=True)

