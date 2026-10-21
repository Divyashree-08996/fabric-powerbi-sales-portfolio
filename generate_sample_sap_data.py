#!/usr/bin/env python3
"""
Generate Realistic SAP Business Partner Sample Datasets for Microsoft Fabric.
Uses standard Python library (zero third-party dependencies required).

Tables Generated:
  1. sap_but000.csv - S/4HANA Business Partner Master General Data
  2. sap_adrc.csv   - Central Address Master Data
  3. sap_knvp.csv   - Customer Partner Functions (Sold-to, Ship-to, Bill-to, Payer)
  4. sap_vbak.csv   - Sales Document Header (Orders)
  5. sap_vbap.csv   - Sales Document Item (Line Items)
  6. sap_bsid.csv   - Open Customer Line Items (Accounts Receivable & Aging)
"""

import os
import csv
import random
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Seed for reproducibility
random.seed(42)

NUM_PARTNERS = 500
NUM_ORDERS = 2500

CITIES_COUNTRIES = [
    ("New York", "US", "NY", "10001"),
    ("Chicago", "US", "IL", "60601"),
    ("San Francisco", "US", "CA", "94105"),
    ("Frankfurt", "DE", "HE", "60311"),
    ("Munich", "DE", "BY", "80331"),
    ("London", "GB", "LND", "EC1A 1BB"),
    ("Paris", "FR", "IDF", "75001"),
    ("Tokyo", "JP", "TYO", "100-0001"),
    ("Singapore", "SG", "SG", "018989"),
    ("Toronto", "CA", "ON", "M5H 2N2")
]

COMPANIES = [
    "Nexus Logistics Global", "Apex Industrial Tech", "Vanguard Retailers",
    "OmniSupply Systems", "Horizon Energy Corp", "Cascade Health Solutions",
    "Starlight Electronics", "Meridian Chemical Group", "Pinnacle Auto Works",
    "Titan Heavy Equipment", "Aura Consumer Goods", "Solstice Media & Print",
    "Beacon Aerospace", "Velocity Transport AG", "Summit Materials GmbH",
    "BlueWave Distribution", "Atlas Renewable Power", "Frontier Data Systems"
]

FIRST_NAMES = ["Liam", "Emma", "Noah", "Olivia", "Ethan", "Sophia", "Lucas", "Mia", "Alexander", "Isabella"]
LAST_NAMES = ["Smith", "Müller", "Johnson", "Schneider", "Brown", "Fischer", "Davis", "Weber", "Wilson", "Schmidt"]
SALES_ORGS = ["1000", "2000", "3000"]
DIST_CHANNELS = ["10", "20"]
DIVISIONS = ["00", "01"]

# -------------------------------------------------------------
# 1. BUT000: Business Partner General Master Data & ADRC
# -------------------------------------------------------------
print("Generating SAP BUT000 & ADRC...")
bp_records = []
adrc_records = []
partner_ids = []

start_date = datetime(2023, 1, 1)

for i in range(1, NUM_PARTNERS + 1):
    bp_id = f"001000{i:04d}"
    partner_ids.append(bp_id)
    addr_num = f"ADR{i:06d}"
    bp_type = "2" if random.random() < 0.75 else "1"  # 75% Organizations, 25% Persons
    
    city, country, region, postal = random.choice(CITIES_COUNTRIES)
    street = f"{random.randint(10, 999)} {random.choice(['Main St', 'Industrial Parkway', 'Central Ave', 'Market St', 'Bahnhofstrasse', 'High Street'])}"
    
    if bp_type == "2":
        name_org = f"{random.choice(COMPANIES)} #{i}"
        name_first = ""
        name_last = ""
    else:
        name_org = ""
        name_first = random.choice(FIRST_NAMES)
        name_last = random.choice(LAST_NAMES)
        
    created_date = (start_date + timedelta(days=random.randint(0, 700))).strftime("%Y-%m-%d")
    commit_time = datetime.now() - timedelta(hours=random.randint(1, 100))
    change_type = "U" if random.random() < 0.2 else "I"
    
    bp_records.append({
        "PARTNER": bp_id,
        "TYPE": bp_type,
        "NAME_ORG1": name_org,
        "NAME_FIRST": name_first,
        "NAME_LAST": name_last,
        "ADDRNUMBER": addr_num,
        "CRDAT": created_date,
        "_change_type": change_type,
        "_commit_timestamp": commit_time.isoformat()
    })
    
    adrc_records.append({
        "ADDRNUMBER": addr_num,
        "STREET": street,
        "CITY1": city,
        "POST_CODE1": postal,
        "COUNTRY": country,
        "REGION": region
    })

def write_csv(filename, fieldnames, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv("sap_but000.csv", ["PARTNER", "TYPE", "NAME_ORG1", "NAME_FIRST", "NAME_LAST", "ADDRNUMBER", "CRDAT", "_change_type", "_commit_timestamp"], bp_records)
write_csv("sap_adrc.csv", ["ADDRNUMBER", "STREET", "CITY1", "POST_CODE1", "COUNTRY", "REGION"], adrc_records)

# -------------------------------------------------------------
# 2. KNVP: Customer Partner Functions
# -------------------------------------------------------------
print("Generating SAP KNVP (Partner Functions)...")
knvp_records = []

for bp_id in partner_ids:
    sales_org = random.choice(SALES_ORGS)
    dist_ch = random.choice(DIST_CHANNELS)
    div = random.choice(DIVISIONS)
    
    knvp_records.append({"KUNNR": bp_id, "VKORG": sales_org, "VTWEG": dist_ch, "SPART": div, "PARVW": "SP", "KUNN2": bp_id})
    knvp_records.append({"KUNNR": bp_id, "VKORG": sales_org, "VTWEG": dist_ch, "SPART": div, "PARVW": "SH", "KUNN2": bp_id})
    knvp_records.append({"KUNNR": bp_id, "VKORG": sales_org, "VTWEG": dist_ch, "SPART": div, "PARVW": "BP", "KUNN2": random.choice(partner_ids)})
    knvp_records.append({"KUNNR": bp_id, "VKORG": sales_org, "VTWEG": dist_ch, "SPART": div, "PARVW": "PY", "KUNN2": random.choice(partner_ids)})

write_csv("sap_knvp.csv", ["KUNNR", "VKORG", "VTWEG", "SPART", "PARVW", "KUNN2"], knvp_records)

# -------------------------------------------------------------
# 3. VBAK & VBAP: Sales Orders Header & Line Items
# -------------------------------------------------------------
print("Generating SAP VBAK & VBAP (Sales Transactions)...")
vbak_records = []
vbap_records = []

order_start = datetime(2025, 1, 1)

for order_num in range(100000, 100000 + NUM_ORDERS):
    vbeln = f"{order_num}"
    partner = random.choice(partner_ids)
    order_date = order_start + timedelta(days=random.randint(0, 500))
    sales_org = random.choice(SALES_ORGS)
    
    num_items = random.randint(1, 4)
    total_net_val = 0.0
    
    for item_idx in range(1, num_items + 1):
        posnr = f"{item_idx * 10:04d}"
        qty = random.randint(1, 50)
        unit_price = round(random.uniform(50.0, 1200.0), 2)
        net_val = round(qty * unit_price, 2)
        margin_pct = round(random.uniform(0.18, 0.48), 3)
        margin_val = round(net_val * margin_pct, 2)
        total_net_val += net_val
        
        vbap_records.append({
            "VBELN": vbeln,
            "POSNR": posnr,
            "MATNR": f"MAT-{random.randint(100, 999)}",
            "KWMENG": qty,
            "NETWR": f"{net_val:.2f}",
            "MARGIN_VAL": f"{margin_val:.2f}",
            "WAERK": "USD"
        })
        
    vbak_records.append({
        "VBELN": vbeln,
        "ERDAT": order_date.strftime("%Y-%m-%d"),
        "KUNNR": partner,
        "VKORG": sales_org,
        "NETWR": f"{total_net_val:.2f}",
        "WAERK": "USD",
        "ABSTK": random.choice(["A", "B", "C"])
    })

write_csv("sap_vbak.csv", ["VBELN", "ERDAT", "KUNNR", "VKORG", "NETWR", "WAERK", "ABSTK"], vbak_records)
write_csv("sap_vbap.csv", ["VBELN", "POSNR", "MATNR", "KWMENG", "NETWR", "MARGIN_VAL", "WAERK"], vbap_records)

# -------------------------------------------------------------
# 4. BSID: Open Customer Line Items (Finance & Credit Exposure)
# -------------------------------------------------------------
print("Generating SAP BSID (Open AR & Aging)...")
bsid_records = []

for inv_id in range(500000, 500000 + 1200):
    belnr = f"{inv_id}"
    partner = random.choice(partner_ids)
    doc_date = datetime.now() - timedelta(days=random.randint(5, 180))
    due_days_offset = random.choice([30, 60, 90])
    due_date = doc_date + timedelta(days=due_days_offset)
    amount = round(random.uniform(500.0, 45000.0), 2)
    
    days_past_due = max(0, (datetime.now() - due_date).days)
    
    bsid_records.append({
        "BUKRS": "1000",
        "KUNNR": partner,
        "BELNR": belnr,
        "BLDAT": doc_date.strftime("%Y-%m-%d"),
        "ZFBDT": due_date.strftime("%Y-%m-%d"),
        "WRBTR": f"{amount:.2f}",
        "WAERS": "USD",
        "DAYS_PAST_DUE": days_past_due
    })

write_csv("sap_bsid.csv", ["BUKRS", "KUNNR", "BELNR", "BLDAT", "ZFBDT", "WRBTR", "WAERS", "DAYS_PAST_DUE"], bsid_records)

print(f"\nAll SAP sample datasets successfully created in: {OUTPUT_DIR}")
for f in os.listdir(OUTPUT_DIR):
    size_kb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
    print(f"  - {f} ({size_kb:.1f} KB)")
