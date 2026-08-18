# N100 Financial Intelligence Platform

A financial intelligence platform designed to analyze and present financial information for N100 companies through financial analytics, KPI analysis, peer comparison, screening, reports, and visual dashboards.

---

## 📌 Project Overview

The **N100 Financial Intelligence Platform** provides a structured way to analyze company-level financial information and generate useful financial insights.

The platform combines:

- Financial analytics
- KPI and ratio analysis
- Peer comparison
- Company screening
- Capital allocation analysis
- Financial reports
- Data visualization
- Radar charts
- REST API access

The project is designed to provide financial information in a clear and easy-to-understand format.

---

## 🚀 Key Features

### 📊 Financial Analytics

Analyze important financial metrics and company performance using structured financial data.

### 📈 KPI & Ratio Analysis

Calculate and analyze financial ratios and key performance indicators to understand company performance.

### 🏢 Company Profiles

Access company-level information and financial details.

### 🔎 Investment Screener

Screen companies based on financial metrics and investment-related criteria.

### 🤝 Peer Comparison

Compare companies with their peers to understand relative financial performance.

### 💰 Capital Allocation

Analyze how companies allocate capital across different areas of their business.

### 📑 Financial Reports

Generate financial reports containing useful financial information and visualizations.

### 📊 Data Visualization

The platform generates different visualizations including:

- Growth charts
- Profit charts
- Radar charts
- Sector analysis
- Company dashboards

### 🌐 REST API

The platform provides a FastAPI-based REST API for accessing company and financial information.

### 🧪 Automated Testing

The project includes automated tests for:

- API endpoints
- ETL functionality
- Data normalization
- KPI ratios
- Data quality rules

---

## 🛠️ Technology Stack

### Programming Language

- Python 3.11

### Data & Analytics

- Pandas
- NumPy
- Matplotlib
- OpenPyXL

### Backend

- FastAPI
- Uvicorn

### Testing

- Pytest
- FastAPI TestClient

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 📁 Project Structure

```text
N100_FINANCIAL_INTELLIGENCE_PLATFORM/
│
├── src/
│   ├── analytics/
│   │   ├── cagr.py
│   │   ├── capital_allocation_report.py
│   │   ├── cashflow_intelligence.py
│   │   ├── cashflow_kpis.py
│   │   ├── check_profit.py
│   │   ├── clustering.py
│   │   ├── company_profile.py
│   │   ├── health_score.py
│   │   ├── investment_screener.py
│   │   ├── peer.py
│   │   ├── ratios.py
│   │   └── sector_analytics.py
│   │
│   ├── api/
│   │   ├── main.py
│   │   └── routers/
│   │
│   ├── reports/
│   │   ├── charts.py
│   │   ├── company_dashboard.py
│   │   ├── growth_chart.py
│   │   ├── profit_chart.py
│   │   ├── radar_chart.py
│   │   ├── report_generator.py
│   │   └── tearsheet.py
│   │
│   └── ...
│
├── tests/
│   ├── dq/
│   │   └── test_rules.py
│   ├── etl/
│   │   ├── test_loader.py
│   │   └── test_normalise.py
│   ├── kpi/
│   │   └── test_ratios.py
│   └── test_api.py
│
├── screenshots/
│
├── requirements.txt
├── README.md
├── .gitignore
└── sample_tearsheet.pdf