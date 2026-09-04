🤖 AI Business Analyst

An end-to-end AI Business Analyst dashboard built with Python, Pandas, SQLite, Streamlit, Plotly, Excel and a local Llama 3.2 AI assistant through Ollama.

The application converts business sales data into interactive KPIs, visual analysis, business insights, anomaly detection and AI-powered recommendations.

📌 Project Overview

This project simulates a real-world business analytics workflow:

Data → Cleaning/Processing → Analysis → Visualization → Business Insights → Anomaly Detection → AI Recommendations

The dashboard supports both:

🗄️ Sample business data stored in SQLite

📊 Excel file upload for analyzing external business data

The AI assistant uses the currently filtered business data to answer business questions without requiring a paid cloud AI API.

🚀 Key Features

📊 Business Performance Dashboard

Total Revenue

Total Orders

Average Order Value

Top Product

Top Customer

Best Month

Lowest Month

Best Region

Best Category

Top Product Revenue

Revenue Share

Profit analysis when cost data is available

🔎 Interactive Filters

Users can filter the analysis by:

Date Range

Region

Customer

Category

Product

All major calculations and visualizations update according to the selected filters.

📈 Data Visualization

Interactive Plotly charts include:

Monthly Revenue Trend

Product-wise Revenue

Category-wise Revenue

Region-wise Revenue

Customer-wise Revenue

🧠 Business Insights

The system automatically generates business findings such as:

Highest-revenue product

Highest-revenue category

Best-performing region

Highest-value customer

Revenue concentration

Order performance

It also provides practical business recommendations based on the available data.

🚨 Anomaly Detection

The application detects unusual month-to-month revenue changes and highlights significant increases or decreases.

🤖 AI Business Analyst

Users can ask natural-language questions such as:

Which product is performing best?

Which region generates the most revenue?

What should the business focus on?

The AI assistant uses Ollama + Llama 3.2 locally and is instructed to use only the business data provided by the application.

📁 Excel Upload

Users can upload an Excel workbook and analyze business data without changing the Python database.

The Excel loader supports common business fields such as:

Order ID

Order Date

Product

Category

Quantity

Price

Revenue

Customer

Region

📤 Data Export

Filtered business data can be exported for further analysis:

CSV

Excel

🛠️ Tech Stack

Technology

Purpose

Python

Core programming

Pandas

Data processing and analysis

SQLite

Business data storage

Streamlit

Interactive dashboard

Plotly

Interactive visualizations

OpenPyXL

Excel file processing

Ollama

Local AI integration

Llama 3.2

Local language model

🏗️ Application Architecture

                    ┌─────────────────────┐
                    │   Business Data     │
                    │                     │
                    │ SQLite / Excel      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Processing   │
                    │                     │
                    │ Pandas + Python     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Business Analysis  │
                    │                     │
                    │ Revenue / Product   │
                    │ Customer / Region   │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
          ┌────────────┐ ┌────────────┐ ┌────────────┐
          │ Plotly     │ │ Insights   │ │ Anomaly    │
          │ Charts     │ │ Engine     │ │ Detection  │
          └────────────┘ └────────────┘ └────────────┘
                 │             │             │
                 └─────────────┼─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Dashboard │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Ollama + Llama 3.2  │
                    │ AI Business Analyst │
                    └─────────────────────┘

📸 Dashboard Screenshots

1. Dashboard Overview



2. Interactive Visualizations



3. Business Analysis Tables



4. Risk & Anomaly Detection



5. AI Business Analyst



📂 Project Structure

AI_Business_Analyst/
│
├── data/
│   └── business.db
│
├── screenshots/
│   ├── ai_assistant.png
│   ├── analysis_tables.png
│   ├── anomaly_detection.png
│   ├── charts.png
│   └── dashboard.png
│
├── src/
│   ├── database.py
│   ├── analysis.py
│   ├── insights.py
│   ├── visualization.py
│   ├── anomaly.py
│   ├── dashboard.py
│   ├── ai_assistant.py
│   └── excel_loader.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── Book1.xlsx

⚙️ How to Run

1. Clone or download the project

Open the project folder in VS Code.

2. Create and activate a virtual environment

Windows PowerShell:

python -m venv venv

Activate:

(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\venv\Scripts\Activate.ps1)

3. Install dependencies

pip install -r requirements.txt

4. Make sure Ollama is installed

Check:

ollama version

Download the model:

ollama pull llama3.2

5. Start Ollama

If required:

ollama run llama3.2

6. Run the dashboard

From the project root:

python -m streamlit run src/dashboard.py

The application will open in the browser.

🗄️ Sample Database

The included SQLite database contains example business entities:

Customers

Products

Orders

Order Items

The dashboard calculates revenue and business KPIs from these relationships.

📊 Business Analysis Workflow

The application follows a typical Business Analyst workflow:

Step 1 — Data Collection

Business data is loaded from SQLite or Excel.

Step 2 — Data Processing

Pandas is used to clean, transform and structure the data.

Step 3 — KPI Calculation

Important business metrics are calculated.

Step 4 — Exploratory Analysis

Revenue is analyzed by:

Product

Category

Region

Customer

Month

Step 5 — Visualization

Interactive charts make business trends easier to understand.

Step 6 — Insight Generation

The system converts analytical results into business findings.

Step 7 — Risk Detection

Revenue anomalies are identified automatically.

Step 8 — AI Assistance

The local Llama model answers natural-language business questions using the available data.

🧠 AI Safety & Data-Grounded Reasoning

The AI assistant is designed to reduce unsupported conclusions.

It is instructed to:

Use only the provided business data

Avoid inventing statistics

Avoid unsupported percentages

Avoid confusing revenue with profit

State when the available data is insufficient

Separate findings, analysis and recommendations

For example, if cost/COGS data is unavailable, the assistant should not invent a profit margin.

💼 Business Analyst Skills Demonstrated

This project demonstrates practical skills relevant to a Business Analyst / Data Analyst role:

Requirement-oriented problem solving

Data collection

Data cleaning

Data transformation

KPI development

Exploratory Data Analysis

Revenue analysis

Customer analysis

Product analysis

Regional analysis

Trend analysis

Anomaly detection

Data visualization

Dashboard development

Excel integration

SQL / SQLite

Python / Pandas

AI-assisted business analysis

Data-driven recommendations

🎯 Example Business Questions

The dashboard can help answer questions such as:

Which product generates the highest revenue?

Which region performs best?

Which customer contributes the most revenue?

What is the monthly revenue trend?

Which category dominates revenue?

Are there unusual revenue changes?

What business area should be investigated further?

Is profit margin available from the current data?

🔮 Future Enhancements

Possible future improvements include:

Real-time business data integration

More advanced forecasting

Customer segmentation

Churn prediction

Automated PDF reports

Advanced profitability analysis

Power BI integration

Cloud deployment

Role-based dashboard access

Automated scheduled business reports

👩‍💻 Author

Shravani Shahakar

B.E. — Electronics & Telecommunication Engineering

This project was developed as a portfolio project to demonstrate practical Python, data analytics, dashboard development and AI integration skills.

⭐ Project Highlights

AI Business Analyst =

Python
+
Pandas
+
SQLite
+
Excel
+
Plotly
+
Streamlit
+
Anomaly Detection
+
Local AI
+
Business Insights

A complete end-to-end analytics application that transforms raw business data into actionable business intelligence.