#!/usr/bin/env python3
"""
Enterprise Power BI Dataset Generator
Generates realistic, referentially-intact Kimball Star Schema CSV datasets
for Omnichannel Enterprise Sales, Margins, and Customer Lifetime Value Analytics.
"""

import os
import csv
import random
import math
from datetime import date, datetime, timedelta

# Fix seed for reproducible, deterministic enterprise data
random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. Dim_Customer
# -------------------------------------------------------------
print("Generating Dim_Customer...")
customers = []
customer_names = [
    ("Apex Global Solutions", "Enterprise", "USA", "North America", "AAA", "sarah.jenkins@company.com"),
    ("Quantum Logistics GmbH", "Enterprise", "Germany", "EMEA", "AAA", "hans.becker@company.com"),
    ("Nexus Healthcare Corp", "Enterprise", "USA", "North America", "AA", "sarah.jenkins@company.com"),
    ("Vortex Retail UK", "Mid-Market", "UK", "EMEA", "AA", "elizabeth.ward@company.com"),
    ("Kobe Robotics KK", "Enterprise", "Japan", "APAC", "AAA", "kenji.sato@company.com"),
    ("BlueWave Cloud SA", "Mid-Market", "France", "EMEA", "A", "pierre.dubois@company.com"),
    ("Maple Leaf Media", "SMB", "Canada", "North America", "A", "sarah.jenkins@company.com"),
    ("Sydney FinTech Ltd", "Mid-Market", "Australia", "APAC", "AA", "kenji.sato@company.com"),
    ("Nordic Renewable Oy", "Enterprise", "Germany", "EMEA", "AAA", "hans.becker@company.com"),
    ("Atlas Heavy Ind. Inc", "Enterprise", "USA", "North America", "BBB", "sarah.jenkins@company.com"),
    ("Titan CyberSec Ltd", "Mid-Market", "UK", "EMEA", "AA", "elizabeth.ward@company.com"),
    ("Sakura AI Labs", "SMB", "Japan", "APAC", "A", "kenji.sato@company.com"),
    ("Pacific Cargo Pty", "Mid-Market", "Australia", "APAC", "BBB", "kenji.sato@company.com"),
    ("Berlin Dynamics GmbH", "Mid-Market", "Germany", "EMEA", "AA", "hans.becker@company.com"),
    ("Lyon BioPharma SAS", "Enterprise", "France", "EMEA", "AAA", "pierre.dubois@company.com"),
    ("Toronto Digital Corp", "SMB", "Canada", "North America", "A", "sarah.jenkins@company.com"),
    ("Silicon Valley Auto", "Enterprise", "USA", "North America", "AAA", "sarah.jenkins@company.com"),
    ("Tokyo Sensor Systems", "Mid-Market", "Japan", "APAC", "AA", "kenji.sato@company.com"),
    ("Manchester Textiles", "SMB", "UK", "EMEA", "BBB", "elizabeth.ward@company.com"),
    ("Munich Precision Tech", "Enterprise", "Germany", "EMEA", "AAA", "hans.becker@company.com"),
]

# Expand to 250 realistic customer records
full_customers = []
prefixes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Omega", "Sigma", "Hyper", "Terra", "Nova", "Stellar", "Core", "Prime", "Vertex", "Summit", "Beacon", "Pinnacle", "Aero", "Synapse"]
suffixes = ["Systems", "Dynamics", "Technologies", "Logistics", "Ventures", "Partners", "Holdings", "Networks", "Solutions", "Global", "Analytics", "Capital", "Health", "Engineering", "Digital"]
countries_info = [
    ("USA", "North America", "sarah.jenkins@company.com"),
    ("Germany", "EMEA", "hans.becker@company.com"),
    ("UK", "EMEA", "elizabeth.ward@company.com"),
    ("Japan", "APAC", "kenji.sato@company.com"),
    ("France", "EMEA", "pierre.dubois@company.com"),
    ("Australia", "APAC", "kenji.sato@company.com"),
    ("Canada", "North America", "sarah.jenkins@company.com"),
]
segments = ["Enterprise", "Mid-Market", "SMB", "Strategic Partner"]
segment_weights = [0.25, 0.40, 0.30, 0.05]
credit_tiers = ["AAA", "AA", "A", "BBB"]

# First add the fixed 20 named accounts
for idx, c in enumerate(customer_names, start=1):
    cid = f"CUST-{idx:04d}"
    join_date = date(2022, 1, 1) + timedelta(days=random.randint(0, 700))
    full_customers.append({
        "CustomerID": cid,
        "CustomerName": c[0],
        "CustomerSegment": c[1],
        "Country": c[2],
        "Region": c[3],
        "CreditRating": c[4],
        "AccountManagerEmail": c[5],
        "CustomerJoinDate": join_date.strftime("%Y-%m-%d"),
        "IsStrategicAccount": 1 if c[1] in ["Enterprise", "Strategic Partner"] else 0
    })

# Add remaining up to 250
for idx in range(21, 251):
    cid = f"CUST-{idx:04d}"
    c_name = f"{random.choice(prefixes)} {random.choice(suffixes)} {random.choice(['Inc', 'Corp', 'LLC', 'AG', 'GmbH', 'Ltd'])}"
    seg = random.choices(segments, weights=segment_weights)[0]
    country, region, email = random.choice(countries_info)
    credit = random.choices(credit_tiers, weights=[0.2, 0.4, 0.3, 0.1])[0]
    join_date = date(2022, 1, 1) + timedelta(days=random.randint(0, 1000))
    full_customers.append({
        "CustomerID": cid,
        "CustomerName": c_name,
        "CustomerSegment": seg,
        "Country": country,
        "Region": region,
        "CreditRating": credit,
        "AccountManagerEmail": email,
        "CustomerJoinDate": join_date.strftime("%Y-%m-%d"),
        "IsStrategicAccount": 1 if seg in ["Enterprise", "Strategic Partner"] else 0
    })

customer_csv = os.path.join(DATA_DIR, "Dim_Customer.csv")
with open(customer_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(full_customers[0].keys()))
    writer.writeheader()
    writer.writerows(full_customers)

# -------------------------------------------------------------
# 2. Dim_Product
# -------------------------------------------------------------
print("Generating Dim_Product...")
products_data = [
    # Software Licenses
    ("PROD-101", "Enterprise Cloud Suite ERP", "Software Licenses", "Enterprise ERP", 450.00, 1200.00),
    ("PROD-102", "Advanced Analytics AI Engine", "Software Licenses", "AI & ML", 320.00, 850.00),
    ("PROD-103", "CyberShield Threat Sentinel", "Software Licenses", "Security", 210.00, 580.00),
    ("PROD-104", "Identity Access Manager Pro", "Software Licenses", "Security", 140.00, 390.00),
    ("PROD-105", "Automated Compliance Auditor", "Software Licenses", "Governance", 180.00, 480.00),
    ("PROD-106", "Financial Consolidation Hub", "Software Licenses", "Finance & FP&A", 380.00, 950.00),
    # Cloud Services & API Subscriptions
    ("PROD-201", "Elastic API Gateway Tier-1", "Cloud Services", "API Infrastructure", 80.00, 240.00),
    ("PROD-202", "Real-Time Event Stream Kafka", "Cloud Services", "Streaming", 190.00, 520.00),
    ("PROD-203", "OneLake Lakehouse Dedicated Compute", "Cloud Services", "Data Platform", 650.00, 1600.00),
    ("PROD-204", "Vector DB Semantic Search Pod", "Cloud Services", "AI & ML", 240.00, 680.00),
    ("PROD-205", "Encrypted Cold Storage 100TB", "Cloud Services", "Storage", 50.00, 150.00),
    ("PROD-206", "Edge CDN Global Accelerator", "Cloud Services", "Networking", 110.00, 310.00),
    # Hardware & Edge Devices
    ("PROD-301", "Smart Edge IoT Gateway Hub", "Hardware", "Edge Devices", 280.00, 620.00),
    ("PROD-302", "Biometric Terminal Scanner X9", "Hardware", "Peripherals", 190.00, 450.00),
    ("PROD-303", "High-Throughput Barcode Scanner Pro", "Hardware", "Peripherals", 95.00, 220.00),
    ("PROD-304", "Rugged Warehouse Tablet RT-12", "Hardware", "Mobile Devices", 410.00, 890.00),
    ("PROD-305", "Secure Cryptographic HSM Module", "Hardware", "Security Hardware", 850.00, 1950.00),
    # Professional & Managed Services
    ("PROD-401", "Architecture Blueprint & Advisory", "Professional Services", "Advisory", 1800.00, 3600.00),
    ("PROD-402", "Fabric Direct Lake Migration Pack", "Professional Services", "Implementation", 2800.00, 5800.00),
    ("PROD-403", "24/7 Premium Mission-Critical Support", "Professional Services", "Managed Care", 900.00, 2100.00),
    ("PROD-404", "Custom ML Model Training Sprint", "Professional Services", "Implementation", 3200.00, 6500.00),
    ("PROD-405", "Data Governance & Cataloging Audit", "Professional Services", "Advisory", 1500.00, 3200.00),
]

products = []
for p in products_data:
    products.append({
        "ProductID": p[0],
        "ProductName": p[1],
        "Category": p[2],
        "SubCategory": p[3],
        "StandardCost": p[4],
        "ListPrice": p[5],
        "StandardMarginPercent": round((p[5] - p[4]) / p[5], 4),
        "IsActive": 1
    })

product_csv = os.path.join(DATA_DIR, "Dim_Product.csv")
with open(product_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(products[0].keys()))
    writer.writeheader()
    writer.writerows(products)

# -------------------------------------------------------------
# 3. Dim_Store_Region (Sales Channels & Organizational Hierarchy)
# -------------------------------------------------------------
print("Generating Dim_Store_Region...")
stores = [
    {
        "ChannelID": "CH-01",
        "ChannelName": "Direct Enterprise Sales",
        "RegionCode": "NA",
        "RegionName": "North America",
        "Country": "USA",
        "RegionalVP": "David Vance",
        "SalesDirector": "Sarah Jenkins",
        "HierarchyPath": "David Vance|Sarah Jenkins",
        "ChannelType": "Field Direct",
        "CommissionTier": "Tier 1"
    },
    {
        "ChannelID": "CH-02",
        "ChannelName": "Digital Cloud Marketplace",
        "RegionCode": "NA",
        "RegionName": "North America",
        "Country": "USA",
        "RegionalVP": "David Vance",
        "SalesDirector": "Alex Rivera",
        "HierarchyPath": "David Vance|Alex Rivera",
        "ChannelType": "Digital Self-Serve",
        "CommissionTier": "Tier 3"
    },
    {
        "ChannelID": "CH-03",
        "ChannelName": "EMEA Strategic Partners",
        "RegionCode": "EMEA",
        "RegionName": "Europe, Middle East, Africa",
        "Country": "Germany",
        "RegionalVP": "Klaus Richter",
        "SalesDirector": "Hans Becker",
        "HierarchyPath": "Klaus Richter|Hans Becker",
        "ChannelType": "Partner Reseller",
        "CommissionTier": "Tier 2"
    },
    {
        "ChannelID": "CH-04",
        "ChannelName": "UK & Northern Europe Field",
        "RegionCode": "EMEA",
        "RegionName": "Europe, Middle East, Africa",
        "Country": "UK",
        "RegionalVP": "Klaus Richter",
        "SalesDirector": "Elizabeth Ward",
        "HierarchyPath": "Klaus Richter|Elizabeth Ward",
        "ChannelType": "Field Direct",
        "CommissionTier": "Tier 1"
    },
    {
        "ChannelID": "CH-05",
        "ChannelName": "France & Southern Europe",
        "RegionCode": "EMEA",
        "RegionName": "Europe, Middle East, Africa",
        "Country": "France",
        "RegionalVP": "Klaus Richter",
        "SalesDirector": "Pierre Dubois",
        "HierarchyPath": "Klaus Richter|Pierre Dubois",
        "ChannelType": "Field Direct",
        "CommissionTier": "Tier 2"
    },
    {
        "ChannelID": "CH-06",
        "ChannelName": "APAC Enterprise Alliance",
        "RegionCode": "APAC",
        "RegionName": "Asia Pacific",
        "Country": "Japan",
        "RegionalVP": "Mei Lin",
        "SalesDirector": "Kenji Sato",
        "HierarchyPath": "Mei Lin|Kenji Sato",
        "ChannelType": "Strategic Alliance",
        "CommissionTier": "Tier 1"
    },
    {
        "ChannelID": "CH-07",
        "ChannelName": "Australia & Oceania Hub",
        "RegionCode": "APAC",
        "RegionName": "Asia Pacific",
        "Country": "Australia",
        "RegionalVP": "Mei Lin",
        "SalesDirector": "Kenji Sato",
        "HierarchyPath": "Mei Lin|Kenji Sato",
        "ChannelType": "Partner Reseller",
        "CommissionTier": "Tier 2"
    },
]

store_csv = os.path.join(DATA_DIR, "Dim_Store_Region.csv")
with open(store_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(stores[0].keys()))
    writer.writeheader()
    writer.writerows(stores)

# -------------------------------------------------------------
# 4. Dim_Date (Rich Calendar with Fiscal Year & Relative Offsets)
# -------------------------------------------------------------
print("Generating Dim_Date...")
start_dt = date(2023, 1, 1)
end_dt = date(2026, 12, 31)
total_days = (end_dt - start_dt).days + 1
benchmark_dt = date(2025, 12, 31) # Benchmark current reference date

date_records = []
for i in range(total_days):
    cur_dt = start_dt + timedelta(days=i)
    y = cur_dt.year
    m = cur_dt.month
    d = cur_dt.day
    dow = cur_dt.isoweekday() # 1=Mon, 7=Sun
    q = (m - 1) // 3 + 1
    
    # Fiscal Year (starts July 1)
    if m >= 7:
        fy = y + 1
        fq = (m - 7) // 3 + 1
        fp = m - 6
    else:
        fy = y
        fq = (m + 5) // 3 + 1
        fp = m + 6
        
    m_offset = (y - benchmark_dt.year) * 12 + (m - benchmark_dt.month)
    d_offset = (cur_dt - benchmark_dt).days
    
    date_records.append({
        "Date": cur_dt.strftime("%Y-%m-%d"),
        "DateKey": int(cur_dt.strftime("%Y%m%d")),
        "Year": y,
        "YearMonth": int(f"{y}{m:02d}"),
        "MonthName": cur_dt.strftime("%B"),
        "MonthShort": cur_dt.strftime("%b"),
        "MonthNumber": m,
        "Quarter": f"Q{q}",
        "YearQuarter": f"{y}-Q{q}",
        "QuarterNumber": q,
        "DayOfMonth": d,
        "DayOfWeekNumber": dow,
        "DayOfWeekName": cur_dt.strftime("%A"),
        "DayOfWeekShort": cur_dt.strftime("%a"),
        "IsWeekend": 1 if dow in [6, 7] else 0,
        "IsWorkday": 0 if dow in [6, 7] else 1,
        "FiscalYear": f"FY{fy}",
        "FiscalQuarter": f"FQ{fq}",
        "FiscalYearQuarter": f"FY{fy}-FQ{fq}",
        "FiscalPeriod": fp,
        "MonthOffset": m_offset,
        "DayOffset": d_offset
    })

date_csv = os.path.join(DATA_DIR, "Dim_Date.csv")
with open(date_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(date_records[0].keys()))
    writer.writeheader()
    writer.writerows(date_records)

# -------------------------------------------------------------
# 5. Dim_ExchangeRate (Daily Exchange Rates to USD)
# -------------------------------------------------------------
print("Generating Dim_ExchangeRate...")
currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]
# Base rates relative to 1 USD
base_rates = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 152.0,
    "CAD": 1.36,
    "AUD": 1.51
}

rates_records = []
for r in date_records:
    dt_str = r["Date"]
    # Slight continuous drift
    drift = math.sin(r["DateKey"] / 1000.0) * 0.03
    for c in currencies:
        if c == "USD":
            rate_to_usd = 1.0 # 1 USD = 1.0 USD
            usd_per_unit = 1.0
        elif c == "EUR":
            rate_to_usd = round(base_rates["EUR"] * (1.0 + drift), 4)
            usd_per_unit = round(1.0 / rate_to_usd, 4)
        elif c == "GBP":
            rate_to_usd = round(base_rates["GBP"] * (1.0 + drift * 0.8), 4)
            usd_per_unit = round(1.0 / rate_to_usd, 4)
        elif c == "JPY":
            rate_to_usd = round(base_rates["JPY"] * (1.0 + drift * 1.5), 2)
            usd_per_unit = round(1.0 / rate_to_usd, 6)
        elif c == "CAD":
            rate_to_usd = round(base_rates["CAD"] * (1.0 - drift * 0.5), 4)
            usd_per_unit = round(1.0 / rate_to_usd, 4)
        elif c == "AUD":
            rate_to_usd = round(base_rates["AUD"] * (1.0 + drift * 0.6), 4)
            usd_per_unit = round(1.0 / rate_to_usd, 4)
            
        rates_records.append({
            "Date": dt_str,
            "CurrencyCode": c,
            "LocalPerUSD": rate_to_usd,      # e.g., 0.92 EUR per 1 USD
            "USDPerLocal": usd_per_unit      # e.g., 1.087 USD per 1 EUR
        })

fx_csv = os.path.join(DATA_DIR, "Dim_ExchangeRate.csv")
with open(fx_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rates_records[0].keys()))
    writer.writeheader()
    writer.writerows(rates_records)

# -------------------------------------------------------------
# 6. Fact_Sales (Order Line Items with Dynamic Cohorts & Seasonality)
# -------------------------------------------------------------
print("Generating Fact_Sales (approx 20,000 transactions)...")
country_currency_map = {
    "USA": "USD",
    "Germany": "EUR",
    "France": "EUR",
    "UK": "GBP",
    "Japan": "JPY",
    "Canada": "CAD",
    "Australia": "AUD"
}

country_channel_map = {
    "USA": ["CH-01", "CH-02"],
    "Germany": ["CH-03"],
    "France": ["CH-05", "CH-03"],
    "UK": ["CH-04", "CH-03"],
    "Japan": ["CH-06"],
    "Canada": ["CH-01", "CH-02"],
    "Australia": ["CH-07", "CH-06"]
}

# Create lookup dictionaries for product pricing
prod_dict = {p["ProductID"]: p for p in products}
cust_dict = {c["CustomerID"]: c for c in full_customers}

# Build exchange rate lookup for USD calculation
fx_lookup = {}
for rx in rates_records:
    fx_lookup[(rx["Date"], rx["CurrencyCode"])] = rx["USDPerLocal"]

sales_lines = []
order_counter = 10001
line_counter = 1

# Simulation window: 2023-01-01 to 2025-12-31 (3 years)
sim_start = date(2023, 1, 1)
sim_end = date(2025, 12, 31)
sim_days = (sim_end - sim_start).days + 1

# Customer activity profiling:
# Pareto skew: Top 20% of customers place 70% of orders!
customer_pool = []
for idx, c in enumerate(full_customers):
    weight = 10 if idx < 30 else (4 if idx < 80 else 1)
    customer_pool.extend([c["CustomerID"]] * weight)

# Generate transactions
for day_idx in range(sim_days):
    curr_date = sim_start + timedelta(days=day_idx)
    date_str = curr_date.strftime("%Y-%m-%d")
    dow = curr_date.isoweekday()
    m = curr_date.month
    y = curr_date.year
    
    # Seasonality factor: Q4 bump, Black Friday / Year-end IT budget spend
    seasonality = 1.0 + (0.25 if m in [11, 12] else (0.1 if m in [6, 9] else -0.05))
    # Growth trend over years: 2023 baseline, 2024 +18%, 2025 +35%
    growth = 1.0 + (0.18 if y == 2024 else (0.38 if y == 2025 else 0.0))
    # Weekend reduction: B2B purchases drop on weekends
    dow_factor = 0.3 if dow in [6, 7] else 1.15
    
    expected_orders = int(18 * seasonality * growth * dow_factor * random.uniform(0.75, 1.25))
    
    for _ in range(expected_orders):
        order_no = f"SO-{order_counter}"
        order_counter += 1
        
        cust_id = random.choice(customer_pool)
        cust = cust_dict[cust_id]
        c_country = cust["Country"]
        c_currency = country_currency_map.get(c_country, "USD")
        c_channel = random.choice(country_channel_map.get(c_country, ["CH-01"]))
        
        # Ship date is 1 to 5 days after order date
        ship_date = curr_date + timedelta(days=random.randint(1, 5))
        ship_date_str = ship_date.strftime("%Y-%m-%d")
        
        # Order contains 1 to 4 line items
        num_items = random.choices([1, 2, 3, 4], weights=[0.55, 0.28, 0.12, 0.05])[0]
        selected_prods = random.sample(list(prod_dict.keys()), num_items)
        
        for item_no, pid in enumerate(selected_prods, start=1):
            p_info = prod_dict[pid]
            base_price = p_info["ListPrice"]
            base_cost = p_info["StandardCost"]
            
            # Quantity depending on category
            if p_info["Category"] == "Software Licenses":
                qty = random.choices([1, 2, 5, 10, 25], weights=[0.4, 0.3, 0.18, 0.08, 0.04])[0]
            elif p_info["Category"] == "Cloud Services":
                qty = random.choices([1, 2, 3, 6, 12], weights=[0.5, 0.25, 0.15, 0.07, 0.03])[0]
            elif p_info["Category"] == "Hardware":
                qty = random.choices([2, 5, 10, 20, 50], weights=[0.3, 0.35, 0.2, 0.1, 0.05])[0]
            else: # Professional Services
                qty = random.choices([1, 2, 3], weights=[0.75, 0.2, 0.05])[0]
                
            # Discount depending on customer tier & quantity
            disc_pct = 0.0
            if cust["CustomerSegment"] == "Enterprise":
                disc_pct = random.choice([0.05, 0.10, 0.15, 0.20])
            elif cust["CustomerSegment"] == "Strategic Partner":
                disc_pct = random.choice([0.15, 0.20, 0.25])
            elif qty >= 10:
                disc_pct = 0.08
            else:
                disc_pct = random.choice([0.0, 0.0, 0.0, 0.05])
                
            unit_price_usd = base_price * (1.0 + random.uniform(-0.03, 0.03))
            unit_cost_usd = base_cost * (1.0 + random.uniform(-0.02, 0.02))
            
            # Local currency conversion for local transaction billing
            usd_to_local_rate = 1.0 / fx_lookup.get((date_str, c_currency), 1.0)
            local_unit_price = round(unit_price_usd * usd_to_local_rate, 2)
            local_gross = round(local_unit_price * qty, 2)
            local_disc = round(local_gross * disc_pct, 2)
            local_net = round(local_gross - local_disc, 2)
            
            # Canonical USD amounts for high-performance Star Schema aggregation
            gross_usd = round(qty * unit_price_usd, 2)
            disc_usd = round(gross_usd * disc_pct, 2)
            net_usd = round(gross_usd - disc_usd, 2)
            cost_usd = round(qty * unit_cost_usd, 2)
            margin_usd = round(net_usd - cost_usd, 2)
            
            sales_lines.append({
                "SalesLineID": line_counter,
                "SalesOrderNumber": order_no,
                "OrderLineNumber": item_no,
                "OrderDate": date_str,
                "ShipDate": ship_date_str,
                "CustomerID": cust_id,
                "ProductID": pid,
                "ChannelID": c_channel,
                "TransactionCurrency": c_currency,
                "Quantity": qty,
                "LocalGrossSales": local_gross,
                "LocalDiscount": local_disc,
                "LocalNetSales": local_net,
                "GrossSalesUSD": gross_usd,
                "DiscountAmountUSD": disc_usd,
                "NetSalesUSD": net_usd,
                "TotalCostUSD": cost_usd,
                "MarginUSD": margin_usd,
                "OrderStatus": random.choices(["Completed", "Shipped", "Processing"], weights=[0.92, 0.06, 0.02])[0]
            })
            line_counter += 1

print(f"Total Sales Lines Generated: {len(sales_lines)}")
fact_sales_csv = os.path.join(DATA_DIR, "Fact_Sales.csv")
with open(fact_sales_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(sales_lines[0].keys()))
    writer.writeheader()
    writer.writerows(sales_lines)

# -------------------------------------------------------------
# 7. Fact_Budget (Category & Regional Monthly Financial Targets)
# -------------------------------------------------------------
print("Generating Fact_Budget (Monthly targets 2023-2026)...")
# Categories from Dim_Product
categories = list(set(p["Category"] for p in products))
regions = ["NA", "EMEA", "APAC"]
months_list = []

for y in range(2023, 2027):
    for m in range(1, 13):
        first_of_month = date(y, m, 1)
        months_list.append((y, m, first_of_month.strftime("%Y-%m-%d"), int(f"{y}{m:02d}")))

# Calculate realistic base revenue targets per category & region
cat_weights = {
    "Software Licenses": 180000,
    "Cloud Services": 140000,
    "Professional Services": 95000,
    "Hardware": 65000
}
reg_weights = {
    "NA": 1.25,
    "EMEA": 0.95,
    "APAC": 0.65
}

budget_records = []
b_id = 1
for y, m, dt_str, ym in months_list:
    # Target growth: 12% annual growth
    year_mult = 1.0 + (y - 2023) * 0.12
    # Monthly seasonality
    season_m = 1.0 + (0.22 if m in [11, 12] else (0.1 if m in [6, 9] else -0.05))
    
    for cat in categories:
        for reg in regions:
            base_rev = cat_weights[cat] * reg_weights[reg] * year_mult * season_m * random.uniform(0.96, 1.05)
            # Standard margin target ~ 45% - 55%
            margin_rate = 0.52 if "Software" in cat else (0.45 if "Cloud" in cat else (0.40 if "Professional" in cat else 0.32))
            base_margin = base_rev * margin_rate
            
            budget_records.append({
                "BudgetID": b_id,
                "BudgetMonthDate": dt_str,
                "YearMonth": ym,
                "Category": cat,
                "RegionCode": reg,
                "TargetRevenueUSD": round(base_rev, 2),
                "TargetMarginUSD": round(base_margin, 2)
            })
            b_id += 1

budget_csv = os.path.join(DATA_DIR, "Fact_Budget.csv")
with open(budget_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(budget_records[0].keys()))
    writer.writeheader()
    writer.writerows(budget_records)

# -------------------------------------------------------------
# 8. Disconnected Parameter & Configuration Tables
# -------------------------------------------------------------
print("Generating Disconnected Parameter Tables...")

# Param_ReportingCurrency
currencies_table = [
    {"CurrencyCode": "USD", "CurrencyName": "US Dollar", "CurrencySymbol": "$", "IsDefault": 1},
    {"CurrencyCode": "EUR", "CurrencyName": "Euro", "CurrencySymbol": "€", "IsDefault": 0},
    {"CurrencyCode": "GBP", "CurrencyName": "British Pound", "CurrencySymbol": "£", "IsDefault": 0},
    {"CurrencyCode": "JPY", "CurrencyName": "Japanese Yen", "CurrencySymbol": "¥", "IsDefault": 0},
    {"CurrencyCode": "CAD", "CurrencyName": "Canadian Dollar", "CurrencySymbol": "C$", "IsDefault": 0},
    {"CurrencyCode": "AUD", "CurrencyName": "Australian Dollar", "CurrencySymbol": "A$", "IsDefault": 0},
]
curr_csv = os.path.join(DATA_DIR, "Param_ReportingCurrency.csv")
with open(curr_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(currencies_table[0].keys()))
    writer.writeheader()
    writer.writerows(currencies_table)

# Param_WhatIf_Price
price_steps = [round(x * 0.05, 2) for x in range(-4, 7)] # -20% to +30%
price_table = [{"PriceAdjustmentPercent": p, "PriceAdjustmentLabel": f"{int(p*100):+d}%"} for p in price_steps]
price_csv = os.path.join(DATA_DIR, "Param_WhatIf_Price.csv")
with open(price_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(price_table[0].keys()))
    writer.writeheader()
    writer.writerows(price_table)

# Param_WhatIf_Cost
cost_steps = [round(x * 0.05, 2) for x in range(-2, 6)] # -10% to +25%
cost_table = [{"CostAdjustmentPercent": c, "CostAdjustmentLabel": f"{int(c*100):+d}%"} for c in cost_steps]
cost_csv = os.path.join(DATA_DIR, "Param_WhatIf_Cost.csv")
with open(cost_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(cost_table[0].keys()))
    writer.writeheader()
    writer.writerows(cost_table)

# Param_TopN
topn_table = [
    {"TopNValue": 5, "TopNLabel": "Top 5 Accounts"},
    {"TopNValue": 10, "TopNLabel": "Top 10 Accounts"},
    {"TopNValue": 15, "TopNLabel": "Top 15 Accounts"},
    {"TopNValue": 25, "TopNLabel": "Top 25 Accounts"},
    {"TopNValue": 50, "TopNLabel": "Top 50 Accounts"},
]
topn_csv = os.path.join(DATA_DIR, "Param_TopN.csv")
with open(topn_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(topn_table[0].keys()))
    writer.writeheader()
    writer.writerows(topn_table)

# Param_MetricSelector
metric_table = [
    {"MetricID": 1, "MetricName": "Net Revenue ($)", "DisplayOrder": 1, "FormatType": "Currency"},
    {"MetricID": 2, "MetricName": "Gross Margin ($)", "DisplayOrder": 2, "FormatType": "Currency"},
    {"MetricID": 3, "MetricName": "Gross Margin (%)", "DisplayOrder": 3, "FormatType": "Percent"},
    {"MetricID": 4, "MetricName": "Order Count", "DisplayOrder": 4, "FormatType": "Integer"},
    {"MetricID": 5, "MetricName": "Units Sold", "DisplayOrder": 5, "FormatType": "Integer"},
    {"MetricID": 6, "MetricName": "Average Order Value ($)", "DisplayOrder": 6, "FormatType": "Currency"},
]
metric_csv = os.path.join(DATA_DIR, "Param_MetricSelector.csv")
with open(metric_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(metric_table[0].keys()))
    writer.writeheader()
    writer.writerows(metric_table)

print("\nAll datasets generated successfully in:", DATA_DIR)
