# Divyashree — Data Analyst & Microsoft Fabric / Power BI Specialist
### Master of Science in Data Science | 4 Years Power BI & DAX | 2 Years SQL & ETL

[![Power BI](https://img.shields.io/badge/Power_BI-Direct_Lake-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Microsoft Fabric](https://img.shields.io/badge/Microsoft_Fabric-OneLake-0078D4?logo=microsoft)](https://azure.microsoft.com/products/microsoft-fabric)
[![Python](https://img.shields.io/badge/Python-PySpark_%26_Django-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-Advanced_Queries_%26_SSIS-CC292B?logo=microsoftsqlserver&logoColor=white)](https://learn.microsoft.com/en-us/sql/)

A production-grade analytics portfolio featuring an **End-to-End Microsoft Fabric Lakehouse & Power BI Direct Lake Sales Analytics Platform**, alongside an enterprise portfolio of **10 production reports** built with Django, Tailwind CSS, and interactive Chart.js simulators.

---

## 🌟 Featured Capstone Project
### End-to-End Enterprise Sales Intelligence & Medallion Lakehouse in Microsoft Fabric

- **Data Scope**: **35,502 fact sales transactions** across 7 global countries ($131.88M revenue, $69.6M gross margin).
- **Architecture**: OneLake Medallion Architecture (Bronze Ingestion ➔ Silver Cleansing & Windowed Deduplication ➔ Gold Kimball Star Schema).
- **Engine Optimization**: Delta Lake Parquet V-Order optimization and Z-Order clustering (`OPTIMIZE gold_fact_sales ZORDER BY (OrderDateKey, CustomerKey)`).
- **Power BI Engine**: **Direct Lake Mode** providing sub-second in-memory VertiPaq queries directly over Delta Lake without scheduled data refresh delays.
- **Advanced Features**:
  - Interactive What-If margin sensitivity analysis (price elasticity & supplier cost inflation sliders).
  - Dynamic Time Intelligence (YoY Sales Growth %, MoM %, YTD Sales).
  - Quota attainment tracking vs FP&A budgets.
  - T-SQL Analytics Endpoint views and Dynamic Row-Level Security (RLS).

---

## 💼 Skills & Technical Toolkit

| Domain | Competencies |
| :--- | :--- |
| **Business Intelligence** | Power BI Desktop & Service, Advanced DAX, Calculation Groups, Direct Lake Mode, Data Modeling (Kimball Star Schema) |
| **Cloud Analytics** | Microsoft Fabric (OneLake, Lakehouse, Delta Lake, Fabric Data Factory Pipelines, PySpark) |
| **Database & SQL** | T-SQL, Stored Procedures, Views, Window Functions, Query Performance Tuning, SSIS ETL Pipelines |
| **Data Science & Scripting**| Python (Pandas, NumPy, Scikit-Learn), PySpark, Django Backend Engineering, Automation Scripting |
| **Education** | **Master of Science in Data Science** |

---

## 🚀 How to Run the Portfolio Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run database migrations
python manage.py migrate

# 3. Start the local server
python manage.py runserver
```
Navigate to: **`http://127.0.0.1:8000/`**

---

## 📁 Repository Structure

```text
├── fabric_sales_analytics_project/
│   ├── data/                         # Intermediate enterprise sales datasets (CSV)
│   ├── fabric_lakehouse_notebooks/   # PySpark Medallion Lakehouse ETL (01 Bronze, 02 Silver, 03 Gold)
│   ├── fabric_pipeline/              # Fabric Data Factory orchestration pipeline JSON
│   ├── sql_analytics_endpoint/       # T-SQL views, analytical queries, and Dynamic RLS
│   ├── semantic_model/               # Production DAX measures library (YoY, AOV, Margin, What-If)
│   ├── powerbi_pbip/                 # Power BI Developer Project files (.pbip)
│   └── interactive_dashboard/        # Standalone interactive Power BI web simulator
├── templates/                        # Django portfolio templates with Dark/Light mode
├── main/                             # Django application models, views, and visitor tracking
├── portfolio/                        # Django project configuration & WhiteNoise settings
├── sales_dashboard_preview.html      # Zero-setup standalone Power BI interactive preview
├── requirements.txt                  # Python dependencies
└── build.sh                          # Render cloud deployment script
```

---

## 📬 Contact & Connect

- **Live Portfolio**: [https://divyaanalytica.in](https://divyaanalytica.in)
- **GitHub**: [https://github.com/Divyashree-08996](https://github.com/Divyashree-08996)
