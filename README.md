## Kenya Youth Employment Intelligence Plaitform
An AI-powered data platform that tracks, analyses and generates policy insights on youth unemployment across Kenya, built with Apache Airflow 3.0, SQLite, Streamlit, Plotly and a free local AI model.

"Kenya's youth unemployment rate stands among the highest in Sub-Saharan Africa. Understanding where, why and who is affected is the first step towards fixing it."

## Why This Project Exists
Youth Unemployment is one of Kenya's most pressing development challenges. Yet the data telling this story is scattered across government reports, World Bank datasets and economic surveys which is rarely visualized in one place and almost never made accessible to decisoion makers in real time.

This platform changes all that by creating building automated ETL pipelines, structured SQLite databases, creating 6 interactive plotly charts and a layer of AI that generates policy insights.

## Data Sources
1. Kenya National Bureau of Statistics(Simulation based on actual data)
2. World Bank Open Data API
3. Kenya Economic Survey Reports

## Tech Stack
1. Apache Airflow -> Pipeline Orchestration
2. SQLite -> Lightweight, no server setup needed
3. Pandas -> Cleans and Structures raw data
4. Streamlit -> Builds interactive UI in pure python
5. Plotly -> Interactive, proffessional charts
6. Ollama + TinyLlama -> Free, private and no API costs.
7. Docker -> One Commmand runs everything
8. Python -> Ties everything together


## Project Architecture

## Project Structure

KE_Une/
│
├── dags/
│   └── pipeline.py               # Airflow 3.0 DAG — 4 task pipeline
│
├── data/
│   └── raw/                      # Raw CSV files from extraction
│
├── database/
│   └── employment.db             # SQLite database (auto-created)
│
├── src/
│   ├── extract.py                # Step 1 — World Bank API + KNBS data
│   ├── transform.py              # Step 2 — Clean, enrich, classify
│   ├── load.py                   # Step 3 — Write to SQLite
│   └── ai_insights.py            # AI policy insights & Q&A engine
│
├── dashboard/
│   └── app.py                    # Streamlit dashboard (6 charts + AI)
│
├── requirements.txt
└── README.md

# The Four Pipeline Tasks
1. extract() - Pulls world bank API + generates KNBS data

2. transform() - Cleans data, creates severity labels, calculates gaps.

3. load() - Writes 4 tables to SQLite

4. validate() - Counts records in every table.

# How the Pipeline Works
Airflow schedules and monitors tha data pipeline automatically. Instead of manually running scripts, it runs them every Monday at 8:00am, like a smart alarm clock of your data.



## SQLite Database
Loaded data into SQLite3 and closed the database instead of leaving it open with close()

The file stored include county_unemployment.csv, education_employment.csv, industry_employment.csv and, world_bank_unemployment.csv

## AI Insights Layer
I chose to use Ollama AI model, since it is free, data stays on your machine, it works offline, and it is ideal to work with, somehow easy to work with.

## Streamlit Dashboard

1. Started off with metrics including the:
 National Youth Unemployment rate, County with the Highest Unemployment, County with the lowest unemployment, Average Gender Gap, Rural Urban Gap.

2. Trend Line - This shows the national rate of unemployment throughout the years (2005 - 2025).

3. Clustered Column Chart - This shows the unemployment rate by County for both male and female.

4. Two Trend Lines - This shows the rate of unemployment for both male and female in both counties.

5. Clustered Column Bar Charts - This shows difference in urban and rural arates of unemployment in specific counties.

6. Bar Chart - This shows the rate of employment by people with education qualifications.

7. Bar Chart - This shows the rate of absorption for the youth by different sectors.

## Setup and Installation
1. Step 1 - Clone the Repository

2. Create Virtual Environment

3. Install Dependencies

4. Pull the AI model

5. Run the Pipeline

6. Launch the Dashboard

## Related Articles

Medium: https://medium.com/@paulgikonyo100/i-built-an-ai-powered-youth-intelligence-platform-dashboard-to-track-the-rate-of-unemployment-here-69b1016e1764

Linkediin: https://www.linkedin.com/in/paul-gikonyo-15389418b/?skipRedirect=true

## Author
Built as part of a self educated AI engineering learning journey, combining a background in data analytics with modern data engineering tools, applied to Kenya's most pressing development challenges

## License
MIT License - feel free to use, modify and build on this project.
