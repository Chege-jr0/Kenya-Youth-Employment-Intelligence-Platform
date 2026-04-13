## Kenya Youth Employment Intelligence Plaitform
An AI-powered data platform that tracks, analyses and generates policy insights on youth unemployment across Kenya

"Kenya's youth unemployment rate stands among the highest in Sub-Saharan Africa. Understanding where, why and who is affected is the first step towards fixing it."

## Data Sources
1. Kenya National Bureau of Statistics
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


## Apache Airflow Pipeline

## SQLite Database
Loaded data into SQLite3 and closed the database instead of leaving it open with close()

The file stored include county_unemployment.csv, education_employment.csv, industry_employment.csv and, world_bank_unemployment.csv

## AI Insights Layer

## Streamlit Dashboard

Started off with metrics including the:
1. National Youth Unemployment rate
2. County with the Highest Unemployment
3. County with the lowest unemployment
4. Average Gender Gap 
5. Rural Urban Gap

## License
MIT License - feel free to use, modify and build on this project.
