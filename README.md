# FAF Freight Analysis Dashboard

An AI-powered freight analytics dashboard built on U.S. Department of Transportation data, 
designed to support military logistics decision-making.

## Overview
This project analyzes U.S. freight flow data from the Freight Analysis Framework (FAF 5.7.1),
produced by the Bureau of Transportation Statistics. It provides interactive visualizations
and AI-generated insights across transport modes, commodities, trade types, and time trends
from 2018 to 2024.

## Features
- 📊 **Overview Tab** — KPI metrics and freight volume by transport mode
- 📈 **Trend Analysis** — Year-over-year freight trends with COVID-19 impact highlighted
- 📦 **Commodity Intelligence** — Top commodities by tonnage and economic value
- 🌐 **Trade Flow** — Domestic vs import vs export analysis with value per ton
- 🤖 **AI Insights** — Locally hosted LLM (phi3 via Ollama) generates plain English 
  summaries for each chart — no API key or internet required

## Tech Stack
- Python 3.11
- Streamlit
- Plotly Express
- Pandas
- Ollama (phi3) — local AI model

## Data Source
Freight Analysis Framework (FAF) 5.7.1
Bureau of Transportation Statistics & Federal Highway Administration
https://www.bts.gov/faf

> Raw data is not included in this repo due to file size (1.1GB).
> Download FAF5.7.1.csv from the link above and place it in:
> `data/raw/extracted/FAF5.7.1.csv`

## Setup & Installation

**1. Clone the repo:**
```bash
git clone https://github.com/alexp2967/faf-secure-logistics-analysis.git
cd faf-secure-logistics-analysis
```

**2. Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Install and start Ollama:**
```bash
brew install ollama
ollama serve
ollama pull phi3
```

**5. Run the dashboard:**
```bash
streamlit run app.py
```

## Project Structure

## Key Findings
- **Truck dominates** U.S. freight at 63% of total tonnage
- **Air freight** carries 0.03% by weight but generates 95x higher value per ton
- **COVID-19 impact** visible in 2021 as a 30% drop followed by strong recovery in 2024
- **Domestic trade** accounts for 87% of freight volume but imports carry 3x higher value per ton
- **Energy commodities** (Natural Gas, Gasoline) lead by tonnage
- **High-value goods** (Motorized Vehicles, Electronics) lead by economic value

## Relevance to Military Logistics
This dashboard demonstrates core Army Vantage analyst skills:
- Dashboard configuration and reuse
- Data validation and quality checks
- Analytics handoff for non-technical decision makers
- AI-assisted insight generation for operational briefings