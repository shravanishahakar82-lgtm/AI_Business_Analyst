# 🤖 AI Business Analyst

An end-to-end AI Business Analyst dashboard built with **Python, Pandas, SQLite, Streamlit, Plotly, Excel and a local Llama 3.2 AI assistant through Ollama**.

The application converts business sales data into interactive KPIs, visual analysis, business insights, anomaly detection and AI-powered recommendations.

---

## 📌 Project Overview

This project simulates a real-world business analytics workflow:

**Data → Cleaning/Processing → Analysis → Visualization → Business Insights → Anomaly Detection → AI Recommendations**

The dashboard supports both:

- 🗄️ Sample business data stored in SQLite
- 📊 Excel file upload for analyzing external business data

The AI assistant uses the currently filtered business data to answer business questions without requiring a paid cloud AI API.

---

## 🚀 Key Features

### 📊 Business Performance Dashboard

The dashboard provides important business KPIs including:

- Total Revenue
- Total Orders
- Average Order Value
- Top Product
- Top Customer
- Best Month
- Lowest Month
- Best Region
- Best Category
- Top Product Revenue
- Revenue Share
- Profit analysis when cost data is available

---

### 🔎 Interactive Filters

Users can filter the analysis by:

- Date Range
- Region
- Customer
- Category
- Product

All major calculations and visualizations update according to the selected filters.

---

### 📈 Data Visualization

Interactive Plotly charts include:

- Monthly Revenue Trend
- Product-wise Revenue
- Category-wise Revenue
- Region-wise Revenue
- Customer-wise Revenue

---

### 🧠 Business Insights

The system automatically generates business findings such as:

- Highest-revenue product
- Highest-revenue category
- Best-performing region
- Highest-value customer
- Revenue concentration
- Order performance

It also provides practical business recommendations based on the available data.

---

### 🚨 Anomaly Detection

The application detects unusual month-to-month revenue changes and highlights significant increases or decreases.

---

### 🤖 AI Business Analyst

Users can ask natural-language questions such as:

- Which product is performing best?
- Which region generates the most revenue?
- What should the business focus on?

The AI assistant uses **Ollama + Llama 3.2 locally** and is instructed to use only the business data provided by the application.

---

### 📁 Excel Upload

Users can upload an Excel workbook and analyze business data without changing the Python database.

The Excel loader supports common business fields such as:

- Order ID
- Order Date
- Product
- Category
- Quantity
- Price
- Revenue
- Customer
- Region

---

### 📤 Data Export

Filtered business data can be exported for further analysis:

- CSV
- Excel

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data processing and analysis |
| SQLite | Business data storage |
| Streamlit | Interactive dashboard |
| Plotly | Interactive visualizations |
| OpenPyXL | Excel file processing |
| Ollama | Local AI integration |
| Llama 3.2 | Local language model |

---

## 🏗️ Application Architecture

```text
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