"""
Alex Rivera | Data Analyst & Power BI Developer Portfolio
Framework: Streamlit + Plotly + Pandas
Theme: Clean Minimalist Light
Run Command: streamlit run portfolio_streamlit.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration (Clean Minimalist Layout)
st.set_page_config(
    page_title="Alex Rivera | Data Analyst & Power BI Developer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Minimalist Light Styling CSS
st.markdown("""
<style>
    /* Main Background & Clean Typography */
    .main {
        background-color: #FAFAFA;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    h1, h2, h3 {
        color: #0F172A;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    p, li {
        color: #475569;
        font-size: 0.95rem;
    }
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
    }
    /* Custom badge */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        background-color: #EFF6FF;
        color: #1D4ED8;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-amber {
        background-color: #FEF3C7;
        color: #B45309;
    }
    .card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Profile & Filters
with st.sidebar:
    st.markdown("### 📊 Alex Rivera")
    st.caption("Data Analyst | Power BI Developer | Python")
    st.markdown("---")
    
    st.markdown("**Core Accreditations**")
    st.markdown("""
    - ⚡ **DP-600:** Fabric Analytics Engineer Associate
    - 🏅 **PL-300:** Power BI Data Analyst Associate
    - 🐍 **PCAP™:** Python Certified Associate
    - 🗄️ **SQL:** Advanced Query Optimization
    """)
    st.markdown("---")
    
    st.markdown("**Navigation Filter**")
    active_view = st.radio(
        "Jump to section:",
        ["Executive Summary & KPIs", "Live BI Dashboard Simulator", "Featured Project Case Studies", "Technical Skills Matrix", "Contact & Download CV"]
    )
    
    st.markdown("---")
    st.caption("📍 Based in New York, NY • Open to Remote & Hybrid Roles")

# 4. Header & Intro
st.markdown("<span class='badge'>Available for Senior Roles</span> <span class='badge badge-amber'>PL-300 Certified</span>", unsafe_allow_html=True)
st.title("Alex Rivera")
st.markdown("#### **Senior Data Analyst & Power BI Solutions Architect**")
st.markdown(
    "Translating raw data into automated executive dashboards, statistical models, and measurable business growth."
)

st.write("")

# 5. Conditional Views
if active_view == "Executive Summary & KPIs":
    st.subheader("Key Career Benchmarks")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Power BI Dashboards", value="45+", delta="Production Deployed")
    with col2:
        st.metric(label="Rows Analyzed & Modeled", value="22M+", delta="High-Performance Star Schema")
    with col3:
        st.metric(label="Identified Cost Optimization", value="$4.2M", delta="+18.5% Margin Lift")
    with col4:
        st.metric(label="Data Pipeline SLA", value="99.8%", delta="Zero Silent Failures")

    st.markdown("---")
    
    st.subheader("About My Approach")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="card">
            <h4>🎯 Business-Centric Analytics</h4>
            <p>I don't just create charts; I build <strong>decision platforms</strong> that align directly with executive OKRs. From gross margin variance to cohort churn drivers, every visualization serves an operational question.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="card">
            <h4>⚡ Python + Power BI Synergies</h4>
            <p>I combine Python's heavy lifting (automated scraping, feature engineering, clustering, statistical cleaning) with Power BI's interactive DAX modeling to create frictionless analytics workflows.</p>
        </div>
        """, unsafe_allow_html=True)

elif active_view == "Live BI Dashboard Simulator":
    st.subheader("Interactive Revenue & Margin Intelligence")
    st.caption("Simulate how cross-filtering updates executive KPIs in real time.")
    
    # Filter Row
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        selected_region = st.selectbox("Select Territory:", ["Global (All)", "North America", "Europe (EMEA)", "Asia-Pacific (APAC)"])
    with f_col2:
        selected_period = st.selectbox("Fiscal Horizon:", ["Full Year 2026", "Q3 2026", "Trailing 12 Months"])
    
    # Seed data generator based on selection
    mult = 1.0 if selected_region == "Global (All)" else (0.55 if selected_region == "North America" else 0.3)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    actuals = np.array([380, 410, 430, 460, 475, 490, 510, 530, 545, 560, 575, 595]) * mult
    targets = np.array([370, 395, 420, 440, 460, 480, 500, 515, 530, 550, 565, 580]) * mult
    
    # Dynamic Metric ribbon
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Gross Revenue", f"${actuals.sum():,.0f}k", "+14.2% YoY")
    m2.metric("Gross Margin %", "42.8%", "+1.9 pts")
    m3.metric("Active Client Accounts", f"{int(1420 * mult):,}", "+8.4%")
    m4.metric("Customer Churn", "1.84%", "-0.42 pts")
    
    # Plotly Trend Chart
    df_trend = pd.DataFrame({"Month": months, "Actual Revenue ($k)": actuals, "Target ($k)": targets})
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_trend["Month"], y=df_trend["Actual Revenue ($k)"],
        mode='lines+markers', name='Actual Revenue ($k)',
        line=dict(color='#2563EB', width=3),
        fill='tozeroy', fillcolor='rgba(37, 99, 235, 0.08)'
    ))
    fig.add_trace(go.Scatter(
        x=df_trend["Month"], y=df_trend["Target ($k)"],
        mode='lines', name='Target Budget ($k)',
        line=dict(color='#94A3B8', width=2, dash='dash')
    ))
    fig.update_layout(
        title="Monthly Actuals vs. Budgeted Forecasts",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

elif active_view == "Featured Project Case Studies":
    st.subheader("Production Analytics Case Studies")
    
    tab_fabric, tab1, tab2, tab3 = st.tabs([
        "⭐ Microsoft Fabric SAP Partner 360",
        "1. Power BI Sales Command Center",
        "2. Python RFM Customer Clustering",
        "3. Supply Chain Inventory Risk"
    ])

    with tab_fabric:
        st.markdown("### Enterprise SAP Partner 360 & Analytics in Microsoft Fabric")
        st.markdown("**Platform:** Microsoft Fabric & OneLake • **Architecture:** Medallion Delta Lake (Bronze $\\rightarrow$ Silver $\\rightarrow$ Gold) • **Languages:** PySpark, DAX, SAP CDC")
        
        st.info("💡 **Business Impact:** Processed 15M+ SAP Business Partner records with hourly CDC sync, delivering sub-second queries via Power BI Direct Lake mode and unlocking $5.8M in partner sales margin insights.")
        
        st.markdown("#### Architecture Highlights:")
        st.write("""
        1. **Ingestion (Bronze):** Ingested SAP S/4HANA & ECC tables (`BUT000`, `KNVP`, `ADRC`, `VBAK`, `BSID`) via Fabric Data Factory SAP CDC connector.
        2. **Cleansing & SCD Type 2 (Silver):** PySpark notebook deduplicating master records, harmonizing partner functions (Sold-to, Ship-to, Payer), and tracking dimension history.
        3. **Star Schema & V-Order (Gold):** Curated dimensional model with Fabric V-Order Parquet compression for high-throughput Direct Lake serving.
        4. **Executive BI:** Power BI Direct Lake semantic model with real-time DSO, partner concentration, and credit risk metrics.
        """)

        st.markdown("#### PySpark Bronze-to-Silver Merge Notebook:")
        st.code("""
from pyspark.sql import functions as F
from delta.tables import DeltaTable

# Ingest and harmonize SAP Business Partner master data
bronze_bp = spark.read.table("bronze_sap_but000").filter(F.col("_change_type") != "D")
bronze_adrc = spark.read.table("bronze_sap_adrc")

enriched_bp = bronze_bp.join(bronze_adrc, on="ADDRNUMBER", how="left").select(
    F.col("PARTNER").alias("partner_id"),
    F.concat_ws(" ", F.col("NAME_FIRST"), F.col("NAME_LAST")).alias("partner_name"),
    F.col("CITY1").alias("city"),
    F.col("COUNTRY").alias("country_code"),
    F.col("_commit_timestamp").alias("last_modified_timestamp")
)

# Delta Lake Merge into Silver Layer
silver_table = DeltaTable.forName(spark, "silver_dim_sap_partner")
silver_table.alias("t").merge(
    enriched_bp.alias("s"), "t.partner_id = s.partner_id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        """, language="python")

        st.markdown("#### Direct Lake Power BI DAX Measure:")
        st.code("""
-- Partner Revenue Concentration (Herfindahl-Hirschman Index / Pareto)
Top20_Partner_Revenue_Share = 
VAR TotalRev = [Total Partner Revenue]
VAR Top20Rev = 
    CALCULATE(
        [Total Partner Revenue],
        TOPN(
            DIVIDE(DISTINCTCOUNT('gold_dim_partner'[partner_id]), 5, 1),
            ALLSELECTED('gold_dim_partner'[partner_id]),
            [Total Partner Revenue],
            DESC
        )
    )
RETURN 
    DIVIDE(Top20Rev, TotalRev, 0)
        """, language="sql")
        
    with tab1:
        st.markdown("### Executive B2B Sales & Margins Command Center")
        st.markdown("**Platform:** Power BI • **Architecture:** Star Schema (1 Fact, 6 Dims) • **Language:** DAX, SQL")
        
        st.info("💡 **Business Impact:** Identified $4.2M in margin recovery opportunities, automated monthly executive packages saving 40 hours/month.")
        
        st.markdown("#### Sample DAX Measure:")
        st.code("""
Sales_YoY_Growth = 
VAR CurrentSales = [Total Revenue]
VAR PriorYearSales = 
    CALCULATE(
        [Total Revenue], 
        SAMEPERIODLASTYEAR('DimDate'[Date])
    )
RETURN 
    DIVIDE(CurrentSales - PriorYearSales, PriorYearSales, 0)
        """, language="sql")
        
    with tab2:
        st.markdown("### E-Commerce RFM Segmentation Engine")
        st.markdown("**Platform:** Python • **Libraries:** Pandas, Scikit-Learn, Plotly")
        st.info("💡 **Business Impact:** Clustered 180,000 customers into 5 actionable personas; lifted email retention marketing CTR by 24%.")
        
        st.markdown("#### Python K-Means Pipeline:")
        st.code("""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Compute R, F, M metrics per customer
rfm = df.groupby('customer_id').agg({
    'invoice_date': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'count',
    'total_amount': 'sum'
}).rename(columns={'invoice_date': 'Recency', 'order_id': 'Frequency', 'total_amount': 'Monetary'})

# Standardize and fit 5 clusters
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(np.log1p(rfm))
kmeans = KMeans(n_clusters=5, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
        """, language="python")

    with tab3:
        st.markdown("### Supply Chain & Stockout Prevention System")
        st.markdown("**Platform:** Power BI + Python ETL Scheduled Service")
        st.info("💡 **Business Impact:** Reduced stockouts by 32% with automated 14-day advance lead-time replenishment warnings.")

elif active_view == "Technical Skills Matrix":
    st.subheader("Technical Competencies")
    
    col_fabric, col1, col2, col3 = st.columns(4)
    with col_fabric:
        st.markdown("### ⚡ Microsoft Fabric")
        st.write("- **OneLake:** Delta Parquet storage, shortcuts")
        st.write("- **Medallion:** Bronze/Silver/Gold Lakehouse")
        st.write("- **Direct Lake:** Sub-second Power BI querying")
        st.write("- **Data Factory:** SAP CDC pipelines, ODP")

    with col1:
        st.markdown("### 📊 Power BI & BI Tools")
        st.write("- **DAX:** Dynamic CALCULATE, Iterators, RLS")
        st.write("- **Power Query (M):** ETL, API connectors")
        st.write("- **Modeling:** Star Schema, Granularity")
        st.write("- **Service:** Gateway scheduling, App deployment")
    
    with col2:
        st.markdown("### 🐍 Python & PySpark")
        st.write("- **PySpark:** Delta Lake merges, windowing")
        st.write("- **Pandas & NumPy:** In-memory transforms")
        st.write("- **Scikit-Learn:** Clustering, anomaly detection")
        st.write("- **Automation:** Selenium/Requests scrapers")

    with col3:
        st.markdown("### 🗄️ SQL & Enterprise ERP")
        st.write("- **SAP Data:** S/4HANA & ECC (BUT000, KNA1)")
        st.write("- **Dialects:** PostgreSQL, T-SQL, MySQL")
        st.write("- **Advanced SQL:** Window functions, CTEs")
        st.write("- **Warehousing:** Snowflake, BigQuery")
        st.write("- **Quality Control:** Great Expectations, schema reconciliation")

elif active_view == "Contact & Download CV":
    st.subheader("Get in Touch")
    st.write("Looking for a data analyst who can bridge deep technical modeling with crisp stakeholder presentation?")
    
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Project Scope / Inquiry")
        submitted = st.form_submit_button("Send Inquiry")
        if submitted:
            st.success(f"Thank you {name}! Your message has been logged. Alex will be in touch shortly.")

    st.markdown("---")
    st.markdown("#### Direct Contact Details")
    st.write("📧 **Email:** alex.rivera.analyst@example.com")
    st.write("🔗 **LinkedIn:** [linkedin.com/in/alex-rivera-data](https://linkedin.com)")
    st.write("💻 **GitHub:** [github.com/alexrivera-analytics](https://github.com)")
