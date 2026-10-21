#!/usr/bin/env python3
"""
Python Portfolio Backend & Static Server
Author: Alex Rivera | Data Analyst & Power BI Developer
Stack: Python (Flask), JSON API, HTML5/Tailwind/Chart.js
"""

import os
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

# Portfolio data store (can be connected to PostgreSQL or SQLite)
PROJECTS_DATA = [
    {
        "id": "fabric-sap-partner-360",
        "title": "Enterprise SAP Partner 360 & Analytics in Microsoft Fabric",
        "tool": "Microsoft Fabric & Delta Lake",
        "category": "Microsoft Fabric",
        "impact": "15M+ SAP Records | < 1s Direct Lake | Hourly CDC",
        "description": "Architected an end-to-end Medallion Lakehouse (Bronze-Silver-Gold) ingesting SAP S/4HANA & ECC partner master data with PySpark SCD2 and Direct Lake Power BI.",
        "tags": ["Microsoft Fabric", "Delta Lake", "SAP CDC", "PySpark", "Direct Lake", "DAX"]
    },
    {
        "id": "sales-command-center",
        "title": "Executive B2B Sales & Margins Command Center",
        "tool": "Power BI & DAX",
        "category": "Power BI",
        "impact": "+18.5% Margin Recovery | -40 hrs Monthly Reporting",
        "description": "Consolidated 3 legacy ERP silos into an interactive single-pane-of-glass dashboard for C-suite decision-makers across 14 global territories.",
        "tags": ["Power BI", "Star Schema", "DAX", "SQL Server"]
    },
    {
        "id": "customer-rfm-segmentation",
        "title": "E-Commerce RFM Segmentation & Churn Predictor",
        "tool": "Python & Unsupervised ML",
        "category": "Python & ML",
        "impact": "24% Email CTR Lift | $320k Saved Retention",
        "description": "Analyzed 1.2M transactions to cluster 180,000 customers into 5 strategic cohorts using K-Means and Recency-Frequency-Monetary scoring.",
        "tags": ["Python", "Pandas", "Scikit-Learn", "Seaborn"]
    },
    {
        "id": "inventory-stockout-prevention",
        "title": "Supply Chain & Inventory Stockout Prevention",
        "tool": "Power BI + Python ETL",
        "category": "Operations BI",
        "impact": "-32% Stockouts | 14-day Lead Warning",
        "description": "Automated inventory reorder thresholds using Python anomaly detection and published live alerts to a Power BI operations dashboard.",
        "tags": ["Power BI", "Python ETL", "Logistics", "Plotly"]
    },
    {
        "id": "sql-data-quality-suite",
        "title": "Automated SQL Data Quality & Reconciliation Suite",
        "tool": "SQL & Data Quality",
        "category": "Data Engineering",
        "impact": "100% Audit Coverage | < 3m Anomaly Alerting",
        "description": "Designed automated schema tests, null-checks, and foreign key audits running daily in PostgreSQL with Slack/Email anomaly alerts.",
        "tags": ["PostgreSQL", "Python", "Data Quality", "CI/CD"]
    }
]

METRICS_DATA = {
    "dashboards_deployed": 50,
    "rows_analyzed": "37M+",
    "pipeline_accuracy": "99.9%",
    "revenue_optimized": "$5.8M",
    "certifications": [
        "Microsoft Certified: Fabric Analytics Engineer Associate (DP-600)",
        "Microsoft Certified: PL-300 Power BI Data Analyst Associate",
        "PCAP™ – Certified Associate in Python Programming",
        "Advanced Relational SQL & Index Optimization"
    ]
}


@app.route("/")
def index():
    """Serve the clean minimalist light portfolio."""
    return send_from_directory(".", "index.html")


@app.route("/api/projects", methods=["GET"])
def get_projects():
    """REST API endpoint returning project case studies."""
    category = request.args.get("category")
    if category:
        filtered = [p for p in PROJECTS_DATA if category.lower() in p["category"].lower()]
        return jsonify({"count": len(filtered), "projects": filtered})
    return jsonify({"count": len(PROJECTS_DATA), "projects": PROJECTS_DATA})


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    """REST API endpoint returning career KPIs."""
    return jsonify(METRICS_DATA)


@app.route("/api/contact", methods=["POST"])
def submit_contact():
    """Contact form submission receiver."""
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get("name", "Visitor")
    email = data.get("email", "unknown@example.com")
    message = data.get("message", "")
    
    # In production, integrate with SendGrid, SMTP, or Slack Webhook
    return jsonify({
        "status": "success",
        "message": f"Thank you {name}! Your message has been logged. Alex will follow up at {email}."
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n=======================================================")
    print(f"  Alex Rivera | Data Analyst & Power BI Portfolio")
    print(f"  Running Python server at: http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=True)
