from django.shortcuts import render, redirect, Http404
from django.contrib import messages
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import UserProfile, WorkExperience, Education, ContactMessage

FEATURED_PROJECT = {
    "id": "fabric-sales-dashboard",
    "title": "Enterprise Sales Intelligence & Medallion Lakehouse",
    "subtitle": "Microsoft Fabric OneLake, PySpark Delta Lake & Power BI Direct Lake Mode",
    "category": "Microsoft Fabric & Power BI",
    "status": "Live Case Study",
    "badge_color": "indigo",
    "featured": True,
    "metrics": [
        {"label": "Fact Transactions", "value": "35,502"},
        {"label": "Analyzed Revenue", "value": "$131.88M"},
        {"label": "Global Territories", "value": "7 Countries"},
        {"label": "Query Latency", "value": "< 1.0s (Direct Lake)"}
    ],
    "description": "Architected an end-to-end Medallion Lakehouse in Microsoft Fabric (Bronze ingestion, Silver cleansing with PySpark, Gold Kimball Star Schema) paired with a high-performance Direct Lake Power BI Semantic Model with sub-second in-memory query speeds and What-If margin sensitivity analysis.",
    "tags": ["Microsoft Fabric", "Power BI", "Direct Lake", "DAX", "PySpark", "Delta Lake", "Kimball Star Schema", "Data Factory"],
    "preview_url": "/preview/sales-dashboard/",
    "case_study_url": "/project/fabric-sales-dashboard/",
    "github_url": "https://github.com",
}

OTHER_PROJECTS = [
    {
        "id": "fpa-margin-command-center",
        "title": "Executive B2B FP&A & Margin Command Center",
        "subtitle": "Multi-Currency Consolidation, Dynamic Pareto 80/20 & Top N Rollups",
        "category": "Power BI & DAX",
        "status": "Coming Soon",
        "badge_color": "amber",
        "featured": False,
        "metrics": [
            {"label": "Impact", "value": "+18.5% Margin Recovery"},
            {"label": "Currency Pairs", "value": "5 Dynamic Currencies"}
        ],
        "description": "Consolidated three legacy ERP silos into an executive single-pane-of-glass dashboard tracking EBITDA, organic growth, and FX translation impacts across 14 global territories.",
        "tags": ["Power BI", "Advanced DAX", "Calculation Groups", "SQL Server"]
    },
    {
        "id": "rfm-churn-engine",
        "title": "E-Commerce Customer RFM Segmentation & Churn Predictor",
        "subtitle": "Unsupervised Machine Learning & Cohort Retention Analytics",
        "category": "Python & Machine Learning",
        "status": "Coming Soon",
        "badge_color": "blue",
        "featured": False,
        "metrics": [
            {"label": "Customer Accounts", "value": "180,000+"},
            {"label": "Retained Revenue", "value": "$320k Annual"}
        ],
        "description": "Analyzed 1.2M transactions using Python Scikit-Learn to cluster customers into Recency-Frequency-Monetary quintiles and modeled monthly cohort attrition curves in Power BI.",
        "tags": ["Python", "Scikit-Learn", "Pandas", "Power BI", "Clustering"]
    },
    {
        "id": "supply-chain-stockout",
        "title": "Supply Chain Inventory Stockout & Lead-Time Optimizer",
        "subtitle": "Automated Reorder Thresholds & Safety Stock Modeling",
        "category": "Operations BI",
        "status": "Coming Soon",
        "badge_color": "emerald",
        "featured": False,
        "metrics": [
            {"label": "Stockout Reduction", "value": "-32%"},
            {"label": "Warning Horizon", "value": "14 Days"}
        ],
        "description": "Built an automated inventory telemetry model linking supplier lead times, buffer stock variations, and SKU velocity to trigger early stockout warnings for distribution centers.",
        "tags": ["Power BI", "SQL Queries", "Python ETL", "Supply Chain"]
    },
    {
        "id": "healthcare-readmission",
        "title": "Clinical Patient Outcomes & 30-Day Hospital Readmission",
        "subtitle": "Risk Stratification & Clinical Quality Measures (CQM)",
        "category": "Healthcare BI",
        "status": "Coming Soon",
        "badge_color": "rose",
        "featured": False,
        "metrics": [
            {"label": "Readmission Lift", "value": "-14.2%"},
            {"label": "HIPAA Governed", "value": "100% Compliant"}
        ],
        "description": "Aggregated electronic health record (EHR) data through SSIS pipelines to identify high-risk chronic patients and track hospital readmission penalties under CMS guidelines.",
        "tags": ["Power BI", "SSIS", "T-SQL Stored Procs", "Healthcare"]
    },
    {
        "id": "sap-cdc-partner-360",
        "title": "SAP S/4HANA Partner Master 360 & Real-Time CDC",
        "subtitle": "Fabric Lakehouse Delta Live Tables & Partner Health Scoring",
        "category": "Microsoft Fabric",
        "status": "Coming Soon",
        "badge_color": "indigo",
        "featured": False,
        "metrics": [
            {"label": "SAP Records", "value": "15M+ Rows"},
            {"label": "Refresh Frequency", "value": "Hourly CDC"}
        ],
        "description": "Integrated SAP sales orders (VBAK/VBAP) and open billing items (BSID) into Fabric Delta Lake with SCD Type 2 tracking and dynamic partner health credit indicators.",
        "tags": ["Microsoft Fabric", "Delta Lake", "SAP CDC", "PySpark"]
    },
    {
        "id": "marketing-attribution-cac",
        "title": "Omnichannel Marketing Attribution & Customer Acquisition Cost",
        "subtitle": "Multi-Touch Attribution Modeling across Paid & Organic Funnels",
        "category": "Marketing Analytics",
        "status": "Coming Soon",
        "badge_color": "violet",
        "featured": False,
        "metrics": [
            {"label": "CAC Efficiency", "value": "+22.4%"},
            {"label": "Ad Spend Analyzed", "value": "$4.5M"}
        ],
        "description": "Combined ad spend from Google, Meta, and LinkedIn with CRM opportunity pipeline to compute first-touch, last-touch, and position-based ROAS and CAC paybacks.",
        "tags": ["Power BI", "DAX", "SQL", "Google Analytics"]
    },
    {
        "id": "hr-workforce-attrition",
        "title": "HR Workforce Analytics & Employee Flight Risk Predictor",
        "subtitle": "Organizational Network Analysis, Diversity & Retention Metrics",
        "category": "People Analytics",
        "status": "Coming Soon",
        "badge_color": "cyan",
        "featured": False,
        "metrics": [
            {"label": "Turnover Reduction", "value": "-11.8%"},
            {"label": "Headcount Tracked", "value": "5,400"}
        ],
        "description": "Evaluated tenure, compensation benchmarks, and engagement survey data using statistical logistic regression to highlight departments with acute flight risks.",
        "tags": ["Power BI", "Python", "HR Analytics", "Statistical Analysis"]
    },
    {
        "id": "saas-cohort-clv",
        "title": "SaaS B2B Subscription Analytics & Cohort Net Revenue Retention",
        "subtitle": "MRR/ARR Waterfall, Expansion, Contraction & Logo Churn",
        "category": "SaaS Analytics",
        "status": "Coming Soon",
        "badge_color": "sky",
        "featured": False,
        "metrics": [
            {"label": "Net Retention (NRR)", "value": "118%"},
            {"label": "ARR Tracked", "value": "$68M"}
        ],
        "description": "Modeled monthly SaaS renewal waterfalls breaking down New ARR, Expansion, Contraction, and Churn with granular cohort retention heatmaps in DAX.",
        "tags": ["Power BI", "DAX Time Intelligence", "SQL Window Functions"]
    },
    {
        "id": "sql-data-quality-suite",
        "title": "Automated SQL Data Quality & Reconciliation Suite",
        "subtitle": "Anomaly Detection, Automated Schema Testing & CI/CD Auditing",
        "category": "Data Engineering & Governance",
        "status": "Coming Soon",
        "badge_color": "teal",
        "featured": False,
        "metrics": [
            {"label": "Audit Coverage", "value": "100% Core Tables"},
            {"label": "Alert Speed", "value": "< 3 Minutes"}
        ],
        "description": "Architected automated SQL assertions, null validation tests, and referential integrity checks scheduled with SSIS/Python, alerting data engineering via Slack and email.",
        "tags": ["SQL Server", "SSIS", "Python", "Data Quality", "Automation"]
    }
]

DEFAULT_PROFILE = {
    "full_name": "Divyashree L",
    "headline": "Power BI Developer & Microsoft Fabric Specialist",
    "education": "Master of Business Administration in Finance | B.E. Computer Science",
    "experience_powerbi": "4+ Years (Power BI & Advanced DAX)",
    "experience_sql": "2+ Years (SQL Server / T-SQL / SSIS)",
    "email": "contact@divyaanalytica.in",
    "phone": "+91 7676046225",
    "location": "Bengaluru, India / Open to Relocation",
    "linkedin_url": "https://www.linkedin.com/in/divyashree-l/",
    "github_url": "https://github.com/Divyashree-08996",
    "bio": "Data Analyst and BI Specialist with an MBA in Finance and B.E. in Computer Science, 4+ years of hands-on expertise building enterprise reporting architectures in Power BI, and 2+ years in relational SQL and SSIS pipelines. Currently advancing core engineering capabilities in Microsoft Fabric (OneLake, Medallion Lakehouse, PySpark Delta Lake, and Direct Lake semantic models).",
    "is_public": True,
}

DEFAULT_EXPERIENCES = [
    {
        "role_title": "Power BI Developer",
        "company_name": "First Meridian Global Services | Client - SAP INDIA",
        "location": "Bengaluru, India",
        "duration": "2023 - 2025",
        "is_current": True,
        "get_bullet_list": [
            "Developed interactive Power BI dashboards using SAP Partner datasets, designing star-schema data models, writing complex DAX measures, and reducing report loading time by 38%.",
            "Architected Kimball star-schema dimensional models, established optimized 1-to-many relationships, and configured bidirectional filter protections.",
            "Engineered advanced DAX measures for Time Intelligence (YoY, MoM, YTD), dynamic Top N Pareto rollups, and calculation groups."
        ],
        "get_tech_list": ["Power BI", "DAX", "SAP ERP", "Python", "Data Modeling", "Advanced Excel"]
    },
    {
        "role_title": "SQL & Power BI Developer",
        "company_name": "Winfeet IT Solutions",
        "location": "Bengaluru, India",
        "duration": "2020 - 2023",
        "is_current": False,
        "get_bullet_list": [
            "SQL & Power BI Developer experienced in writing and altering complex Stored Procedures, managing robust ETL pipelines, and building interactive dashboards that translate raw data into actionable business insights.",
            "Engineered, tuned, and maintained complex SQL Server stored procedures, CTEs, window functions, and views powering core analytics pipelines.",
            "Automated scheduled data validation scripts and exception handling routines to maintain 100% reporting data integrity."
        ],
        "get_tech_list": ["SQL Server", "T-SQL", "Power BI", "SSIS", "ETL", "Star Schema"]
    }
]

DEFAULT_EDUCATIONS = [
    {
        "degree": "Master of Business Administration in Finance Specialization",
        "institution": "AIMIT",
        "year": "2018 - 2020",
        "grade_or_honors": "First Class with Distinction",
        "details": "Specialization in Financial Analytics, Corporate Financial Management, Quantitative Business Analysis, and Predictive Decision Models."
    },
    {
        "degree": "Bachelor of Engineering in Computer Science",
        "institution": "GAT",
        "year": "2014 - 2018",
        "grade_or_honors": "First Class",
        "details": "Core foundations in Relational Database Management Systems (RDBMS), SQL Architecture, Algorithms, Data Structures, and Software Engineering."
    }
]

def home(request):
    try:
        profile = UserProfile.objects.first()
    except Exception:
        profile = None

    if not profile:
        profile = DEFAULT_PROFILE

    # Restricting Access check: If profile set to private and user not logged in
    is_public = getattr(profile, "is_public", True) if hasattr(profile, "is_public") else profile.get("is_public", True)
    if not is_public and not request.user.is_authenticated:
        return render(request, "restricted.html", {"profile": profile})

    # Handle Contact Form POST Submission
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "Portfolio Inbound").strip()
        message = request.POST.get("message", "").strip()

        if name and email and message:
            ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
            try:
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message,
                    ip_address=ip.split(',')[0].strip() if ip else None
                )
            except Exception:
                pass
            try:
                messages.success(request, "Thank you! Your message has been sent successfully. I will get back to you shortly.")
            except Exception:
                pass
            return redirect('/#contact')

    skills = [
        {"name": "Power BI & Advanced DAX", "level": "Expert (4 Years)", "badge": "Primary"},
        {"name": "SQL & Stored Procedures", "level": "Proficient (2 Years)", "badge": "Primary"},
        {"name": "Microsoft Fabric", "level": "OneLake, Lakehouse, Direct Lake", "badge": "Advanced"},
        {"name": "Python & Scripting", "level": "Data Science & PySpark", "badge": "Proficient"},
        {"name": "SSIS & Data Pipelines", "level": "ETL & Orchestration", "badge": "Production"},
        {"name": "Data Modeling", "level": "Kimball Star Schema", "badge": "Core"}
    ]

    try:
        experiences = list(WorkExperience.objects.all())
    except Exception:
        experiences = []
    if not experiences:
        experiences = DEFAULT_EXPERIENCES

    try:
        educations = list(Education.objects.all())
    except Exception:
        educations = []
    if not educations:
        educations = DEFAULT_EDUCATIONS

    context = {
        "profile": profile,
        "skills": skills,
        "experiences": experiences,
        "educations": educations,
        "featured_project": FEATURED_PROJECT,
        "other_projects": OTHER_PROJECTS,
        "total_projects_count": 10
    }
    return render(request, "index.html", context)

def project_detail(request, slug):
    try:
        profile = UserProfile.objects.first()
    except Exception:
        profile = DEFAULT_PROFILE
    if not profile:
        profile = DEFAULT_PROFILE
    if slug == "fabric-sales-dashboard":
        context = {
            "profile": profile,
            "project": FEATURED_PROJECT
        }
        return render(request, "project_detail.html", context)
    raise Http404("Project case study is coming soon.")

@xframe_options_exempt
def dashboard_preview(request):
    return render(request, "sales_dashboard_preview.html")
