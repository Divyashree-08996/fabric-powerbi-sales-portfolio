"""
Microsoft Fabric & Power BI - Pre-Sales Analytics Synthetic Data Generator
Generates realistic enterprise B2B Pre-Sales datasets:
- Accounts (CRM)
- Products / Solutions
- Solution Engineers (SEs / Presales Architects)
- Opportunities (CRM Deals with SE involvement & Win/Loss telemetry)
- Pre-Sales Activities (Demos, Deep Dives, Workshops, Effort hours)
- Proof of Concept (POC / POV projects, success criteria, technical win)
- RFP Requests (Turnaround times, compliance scores, effort)
"""

import os
import csv
import random
import datetime
from pathlib import Path

# Seed for reproducible realistic data
random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "sample_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# 1. GENERATE PRODUCTS
# ---------------------------------------------------------
PRODUCTS = [
    {
        "product_id": "PRD-101",
        "product_name": "Fabric Unified Lakehouse Engine",
        "product_category": "Data & Analytics",
        "deployment_model": "SaaS Multi-Tenant",
        "base_annual_license_usd": 120000,
        "standard_poc_duration_days": 21,
    },
    {
        "product_id": "PRD-102",
        "product_name": "Autonomous AI Copilot Studio",
        "product_category": "Artificial Intelligence",
        "deployment_model": "Hybrid Cloud",
        "base_annual_license_usd": 180000,
        "standard_poc_duration_days": 14,
    },
    {
        "product_id": "PRD-103",
        "product_name": "Zero-Trust Security & Identity Mesh",
        "product_category": "Cybersecurity",
        "deployment_model": "SaaS Multi-Tenant",
        "base_annual_license_usd": 95000,
        "standard_poc_duration_days": 28,
    },
    {
        "product_id": "PRD-104",
        "product_name": "Real-Time Event Streaming Hub",
        "product_category": "Data & Analytics",
        "deployment_model": "Dedicated Cloud",
        "base_annual_license_usd": 140000,
        "standard_poc_duration_days": 18,
    },
    {
        "product_id": "PRD-105",
        "product_name": "Enterprise API & App Integration Cloud",
        "product_category": "Integration & Middleware",
        "deployment_model": "Hybrid Cloud",
        "base_annual_license_usd": 75000,
        "standard_poc_duration_days": 14,
    },
    {
        "product_id": "PRD-106",
        "product_name": "Omnichannel Customer 360 Graph",
        "product_category": "Business Applications",
        "deployment_model": "SaaS Multi-Tenant",
        "base_annual_license_usd": 110000,
        "standard_poc_duration_days": 21,
    },
    {
        "product_id": "PRD-107",
        "product_name": "FinOps Cloud Cost Optimization Engine",
        "product_category": "Cloud Infrastructure",
        "deployment_model": "SaaS Multi-Tenant",
        "base_annual_license_usd": 60000,
        "standard_poc_duration_days": 10,
    },
    {
        "product_id": "PRD-108",
        "product_name": "Industrial IoT & Edge Telemetry Platform",
        "product_category": "IoT & Edge",
        "deployment_model": "Edge & Cloud Hybrid",
        "base_annual_license_usd": 220000,
        "standard_poc_duration_days": 35,
    },
]

def write_products():
    path = DATA_DIR / "products.csv"
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(PRODUCTS[0].keys()))
        writer.writeheader()
        writer.writerows(PRODUCTS)
    print(f"-> Generated {len(PRODUCTS)} products at {path}")

# ---------------------------------------------------------
# 2. GENERATE SOLUTION ENGINEERS (SEs)
# ---------------------------------------------------------
SE_NAMES = [
    ("Marcus", "Vance", "North America", "Lead Solution Architect", "Data & Analytics", 165),
    ("Elena", "Rostova", "EMEA", "Principal SE", "Artificial Intelligence", 150),
    ("Rajesh", "Kulkarni", "APAC", "Senior SE", "Data & Analytics", 125),
    ("Sarah", "Jenkins", "North America", "Senior SE", "Cybersecurity", 130),
    ("Hiroshi", "Tanaka", "APAC", "Principal SE", "Integration & Middleware", 145),
    ("Mateo", "Silva", "LATAM", "Senior SE", "Business Applications", 120),
    ("Amira", "El-Sayed", "EMEA", "Lead Solution Architect", "Cybersecurity", 160),
    ("David", "Kowalski", "EMEA", "Associate SE", "Cloud Infrastructure", 95),
    ("Chloe", "Dupont", "EMEA", "Senior SE", "Artificial Intelligence", 135),
    ("Liam", "O'Connor", "North America", "Principal SE", "Data & Analytics", 150),
    ("Priya", "Nair", "APAC", "Associate SE", "Artificial Intelligence", 95),
    ("Lucas", "Meyer", "EMEA", "Senior SE", "IoT & Edge", 135),
    ("Jessica", "Taylor", "North America", "Associate SE", "Business Applications", 95),
    ("Carlos", "Mendoza", "LATAM", "Principal SE", "Data & Analytics", 145),
    ("Wei", "Zhang", "APAC", "Lead Solution Architect", "Cloud Infrastructure", 165),
    ("Sophia", "Alvarez", "North America", "Senior SE", "Artificial Intelligence", 130),
    ("Julian", "Brandt", "EMEA", "Associate SE", "Integration & Middleware", 95),
    ("Ananya", "Sharma", "APAC", "Senior SE", "Cybersecurity", 130),
    ("Daniel", "Kim", "North America", "Principal SE", "IoT & Edge", 155),
    ("Grace", "Hopper", "North America", "Lead Solution Architect", "Data & Analytics", 170),
]

def generate_solution_engineers():
    ses = []
    for i, (first, last, region, seniority, spec, rate) in enumerate(SE_NAMES, start=1):
        se_id = f"SE-{i:03d}"
        ses.append({
            "se_id": se_id,
            "se_name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}@enterprise-cloud.io",
            "region": region,
            "seniority_level": seniority,
            "specialization": spec,
            "target_weekly_hours": 40,
            "target_utilization_pct": 75.0, # 75% customer-facing effort
            "hourly_cost_rate_usd": rate
        })
    path = DATA_DIR / "solution_engineers.csv"
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(ses[0].keys()))
        writer.writeheader()
        writer.writerows(ses)
    print(f"-> Generated {len(ses)} Solution Engineers at {path}")
    return ses

# ---------------------------------------------------------
# 3. GENERATE ACCOUNTS
# ---------------------------------------------------------
INDUSTRIES = ["Financial Services", "Healthcare & Life Sciences", "Retail & eCommerce", "Manufacturing & Supply Chain", "Technology & SaaS", "Telecommunications", "Energy & Utilities"]
COUNTRIES_BY_REGION = {
    "North America": [("United States", "USA"), ("Canada", "CAN")],
    "EMEA": [("United Kingdom", "GBR"), ("Germany", "DEU"), ("France", "FRA"), ("Netherlands", "NLD"), ("Switzerland", "CHE")],
    "APAC": [("Singapore", "SGP"), ("Australia", "AUS"), ("Japan", "JPN"), ("India", "IND")],
    "LATAM": [("Brazil", "BRA"), ("Mexico", "MEX"), ("Chile", "CHL")]
}

ACCOUNT_NAMES_PREFIX = ["Apex", "Quantum", "Hyperion", "Nexus", "Starlight", "Crestview", "Vanguard", "Pinnacle", "Aegis", "Synergy", "Beacon", "Vertex", "Solstice", "Horizon", "Orion", "Titan", "Spectra", "Novus", "Valence", "Echo"]
ACCOUNT_NAMES_SUFFIX = ["Holdings", "Technologies", "Global Logistics", "Health", "Capital Partners", "Financial Group", "Manufacturing", "Energy Corp", "Communications", "Cloud Systems", "BioPharma", "Retail Network", "Solutions", "Enterprises"]

def generate_accounts(num_accounts=250):
    accounts = []
    for i in range(1, num_accounts + 1):
        acc_id = f"ACC-{1000 + i}"
        name = f"{random.choice(ACCOUNT_NAMES_PREFIX)} {random.choice(ACCOUNT_NAMES_SUFFIX)}"
        region = random.choices(["North America", "EMEA", "APAC", "LATAM"], weights=[0.45, 0.30, 0.18, 0.07])[0]
        country_name, country_code = random.choice(COUNTRIES_BY_REGION[region])
        industry = random.choice(INDUSTRIES)
        tier = random.choices(["Enterprise", "Strategic", "Mid-Market"], weights=[0.35, 0.20, 0.45])[0]
        
        if tier == "Strategic":
            rev = random.randint(1_500_000_000, 25_000_000_000)
            emp = random.randint(10_000, 120_000)
        elif tier == "Enterprise":
            rev = random.randint(250_000_000, 1_499_000_000)
            emp = random.randint(2_000, 9_999)
        else:
            rev = random.randint(40_000_000, 249_000_000)
            emp = random.randint(300, 1_999)

        accounts.append({
            "account_id": acc_id,
            "account_name": name,
            "industry": industry,
            "account_tier": tier,
            "annual_revenue_usd": rev,
            "employee_count": emp,
            "country_name": country_name,
            "country_code": country_code,
            "region": region,
            "created_date": (datetime.date(2023, 1, 1) + datetime.timedelta(days=random.randint(0, 400))).isoformat()
        })
    path = DATA_DIR / "crm_accounts.csv"
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(accounts[0].keys()))
        writer.writeheader()
        writer.writerows(accounts)
    print(f"-> Generated {len(accounts)} Accounts at {path}")
    return accounts

# ---------------------------------------------------------
# 4. GENERATE OPPORTUNITIES
# ---------------------------------------------------------
AE_NAMES = [
    "Jordan Mitchell", "Samantha Reed", "Carlos Rivera", "Emma Thompson",
    "Alexander Wright", "Nina Patel", "Oliver Fischer", "Isabella Santos",
    "Benjamin Hayes", "Hannah Becker", "Lucas Van Der Berg", "Mia Chen"
]

COMPETITORS = ["Snowflake Inc.", "Databricks", "AWS Cloud", "Google Cloud", "Salesforce", "ServiceNow", "In-house Custom Build", "Competitor None"]
LOSS_REASONS = [
    "Technical Feature Gap",
    "Competitor Architectural Advantage",
    "Performance & Scalability Latency",
    "Security & Compliance Non-Conformance",
    "Commercial - Excessive Pricing / TCO",
    "Client Deferred Project / Budget Freeze",
    "Integration Complexity with Legacy ERP",
    "Executive Sponsor Departed"
]
WIN_REASONS = [
    "Superior Architecture & Microsoft Fabric Integration",
    "POC Validated Performance & Low Latency",
    "Comprehensive Security & Governance",
    "Total Cost of Ownership (TCO) Advantage",
    "Exceptional Pre-Sales Demonstration & Technical Trust",
    "Executive Alignment & Roadmap Vision"
]

def generate_opportunities(accounts, solution_engineers, num_opps=800):
    opps = []
    start_date_range = datetime.date(2024, 1, 1)
    end_date_range = datetime.date(2026, 9, 30)
    delta_days = (end_date_range - start_date_range).days

    for i in range(1, num_opps + 1):
        opp_id = f"OPP-2024-{1000 + i}"
        account = random.choice(accounts)
        product = random.choice(PRODUCTS)
        ae = random.choice(AE_NAMES)
        
        # Created Date
        created = start_date_range + datetime.timedelta(days=random.randint(0, delta_days - 60))
        
        # Deal size based on account tier
        base_license = product["base_annual_license_usd"]
        if account["account_tier"] == "Strategic":
            acv = int(base_license * random.uniform(2.5, 6.0))
        elif account["account_tier"] == "Enterprise":
            acv = int(base_license * random.uniform(1.2, 3.0))
        else:
            acv = int(base_license * random.uniform(0.6, 1.4))
        
        deal_type = random.choices(["New Logo", "Expansion / Cross-Sell", "Upgrade / Tier Bump"], weights=[0.55, 0.35, 0.10])[0]
        contract_years = random.choices([1, 2, 3], weights=[0.30, 0.40, 0.30])[0]
        tcv = acv * contract_years

        # Pre-Sales Engagement Decision (Larger deals almost always engage SEs)
        if acv > 250000:
            is_presales_engaged = random.random() < 0.95
        elif acv > 100000:
            is_presales_engaged = random.random() < 0.80
        else:
            is_presales_engaged = random.random() < 0.45

        # Filter SEs in same region or specialized
        matching_ses = [se for se in solution_engineers if se["region"] == account["region"]]
        if not matching_ses:
            matching_ses = solution_engineers
        assigned_se = random.choice(matching_ses) if is_presales_engaged else None

        # Deal Duration
        cycle_days = random.randint(30, 180)
        close_target = created + datetime.timedelta(days=cycle_days)
        
        # Determine Status (Historical deals close; recent deals might be open)
        today = datetime.date(2026, 10, 1)
        if close_target > today:
            stage = random.choices(
                ["1 - Discovery", "2 - Technical Evaluation", "3 - Solution Scoping", "4 - Proof of Concept", "5 - Proposal & RFP", "6 - Negotiation"],
                weights=[0.10, 0.20, 0.25, 0.25, 0.12, 0.08]
            )[0]
            deal_status = "Open"
            actual_close = None
            win_loss_reason = None
            competitor = random.choice(COMPETITORS) if random.random() < 0.7 else "None"
            poc_conducted = True if stage in ["4 - Proof of Concept", "5 - Proposal & RFP", "6 - Negotiation"] and is_presales_engaged and random.random() < 0.65 else False
        else:
            # Deal is closed
            actual_close = close_target + datetime.timedelta(days=random.randint(-15, 25))
            # Win probability is significantly higher when Pre-Sales is involved and POC was done!
            poc_chance = 0.55 if is_presales_engaged else 0.05
            poc_conducted = (random.random() < poc_chance) and is_presales_engaged

            win_probability = 0.22 # baseline unassisted
            if is_presales_engaged:
                win_probability += 0.26 # jumps to ~48%
            if poc_conducted:
                win_probability += 0.22 # jumps to ~70%
            
            is_won = random.random() < win_probability
            if is_won:
                deal_status = "Closed Won"
                stage = "7 - Closed Won"
                win_loss_reason = random.choice(WIN_REASONS)
                competitor = random.choice(COMPETITORS) if random.random() < 0.6 else "None"
            else:
                deal_status = "Closed Lost"
                stage = "8 - Closed Lost"
                win_loss_reason = random.choice(LOSS_REASONS)
                competitor = random.choice(COMPETITORS)

        opps.append({
            "opportunity_id": opp_id,
            "account_id": account["account_id"],
            "opportunity_name": f"{account['account_name']} - {product['product_name']} {deal_type}",
            "ae_owner_name": ae,
            "product_id": product["product_id"],
            "deal_type": deal_type,
            "created_date": created.isoformat(),
            "target_close_date": close_target.isoformat(),
            "actual_close_date": actual_close.isoformat() if actual_close else "",
            "deal_stage": stage,
            "deal_status": deal_status,
            "annual_contract_value_usd": acv,
            "total_contract_value_usd": tcv,
            "se_assigned_id": assigned_se["se_id"] if assigned_se else "",
            "is_presales_engaged": is_presales_engaged,
            "poc_conducted": poc_conducted,
            "competitor_name": competitor,
            "win_loss_reason": win_loss_reason or "",
            "is_technical_loss": True if (deal_status == "Closed Lost" and win_loss_reason in [
                "Technical Feature Gap",
                "Competitor Architectural Advantage",
                "Performance & Scalability Latency",
                "Security & Compliance Non-Conformance",
                "Integration Complexity with Legacy ERP"
            ]) else False
        })

    path = DATA_DIR / "crm_opportunities.csv"
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(opps[0].keys()))
        writer.writeheader()
        writer.writerows(opps)
    print(f"-> Generated {len(opps)} Opportunities at {path}")
    return opps

# ---------------------------------------------------------
# 5. GENERATE PRE-SALES ACTIVITIES
# ---------------------------------------------------------
ACTIVITY_TYPES = [
    ("Standard Product Demo", 1.5, 1.0, "Demonstration"),
    ("Custom Tailored Demo", 2.5, 4.0, "Demonstration"),
    ("Technical Discovery Call", 1.0, 0.5, "Discovery"),
    ("Architecture Design Session (ADS)", 4.0, 3.5, "Architecture"),
    ("Security & Compliance Deep Dive", 2.0, 2.0, "Technical Validation"),
    ("Executive Briefing Center (EBC) Pitch", 3.0, 3.0, "Executive Engagement"),
    ("Hands-on Technical Workshop", 4.5, 4.0, "Technical Validation"),
    ("RFP Clarification Call", 1.5, 1.5, "Proposal Support")
]

CUSTOMER_SENTIMENTS = ["Highly Positive", "Positive & Receptive", "Neutral / Undecided", "Skeptical / Critical"]
TECHNICAL_OBJECTIONS = [
    "None / Smooth Alignment",
    "Data Residency & Regional Compliance",
    "Sub-second Query Latency SLA",
    "API Rate Limits & Throughput Quota",
    "Integration with Legacy On-Premises DB",
    "Data Governance & Role-Based Security",
    "Migration Overhead & Cutover Risk"
]

def generate_presales_activities(opportunities, solution_engineers):
    activities = []
    act_counter = 1

    for opp in opportunities:
        if not opp["is_presales_engaged"]:
            continue
        
        se_id = opp["se_assigned_id"]
        if not se_id:
            se_id = random.choice(solution_engineers)["se_id"]

        opp_created = datetime.date.fromisoformat(opp["created_date"])
        # Number of activities based on deal size
        if opp["annual_contract_value_usd"] > 250000:
            num_acts = random.randint(4, 9)
        elif opp["annual_contract_value_usd"] > 100000:
            num_acts = random.randint(2, 5)
        else:
            num_acts = random.randint(1, 3)

        current_day_offset = random.randint(2, 10)
        for _ in range(num_acts):
            act_type, base_dur, base_prep, category = random.choice(ACTIVITY_TYPES)
            act_date = opp_created + datetime.timedelta(days=current_day_offset)
            current_day_offset += random.randint(5, 20)

            dur_hours = round(max(0.5, random.gauss(base_dur, 0.4)), 1)
            prep_hours = round(max(0.5, random.gauss(base_prep, 0.8)), 1)
            total_hours = round(dur_hours + prep_hours, 1)

            activities.append({
                "activity_id": f"ACT-{act_counter:06d}",
                "opportunity_id": opp["opportunity_id"],
                "se_id": se_id,
                "activity_name": act_type,
                "activity_category": category,
                "activity_date": act_date.isoformat(),
                "duration_hours": dur_hours,
                "prep_hours": prep_hours,
                "total_effort_hours": total_hours,
                "customer_attendees_count": random.randint(2, 14),
                "customer_sentiment": random.choice(CUSTOMER_SENTIMENTS),
                "technical_objection": random.choice(TECHNICAL_OBJECTIONS),
                "follow_up_required": random.choice([True, False, True])
            })
            act_counter += 1

    path = DATA_DIR / "presales_activities.csv"
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(activities[0].keys()))
        writer.writeheader()
        writer.writerows(activities)
    print(f"-> Generated {len(activities)} Pre-Sales Activities at {path}")
    return activities

# ---------------------------------------------------------
# 6. GENERATE PROOF OF CONCEPTS (POC / POV)
# ---------------------------------------------------------
BLOCKERS = [
    "None - Criteria Cleared Successfully",
    "Customer VPN & Firewall Ingress Blocked",
    "Test Data Sanitization Delayed by Legal",
    "Custom Connector Driver Incompatibility",
    "SSO / SAML Identity Token Failure",
    "Performance Bottleneck under High Concurrency",
    "Customer Sponsor Reassigned During POC"
]

def generate_pocs(opportunities, solution_engineers):
    pocs = []
    poc_counter = 1

    for opp in opportunities:
        if not opp["poc_conducted"]:
            continue
        
        se_id = opp["se_assigned_id"] or random.choice(solution_engineers)["se_id"]
        opp_created = datetime.date.fromisoformat(opp["created_date"])
        start_date = opp_created + datetime.timedelta(days=random.randint(14, 45))
        duration_days = random.randint(14, 42)
        end_date = start_date + datetime.timedelta(days=duration_days)

        criteria_total = random.randint(5, 12)
        
        # Outcome correlation
        if opp["deal_status"] == "Closed Won":
            criteria_met = criteria_total
            tech_win = True
            poc_status = "Completed"
            blocker = "None - Criteria Cleared Successfully"
        elif opp["deal_status"] == "Closed Lost":
            if opp["is_technical_loss"]:
                criteria_met = random.randint(1, max(1, criteria_total - 2))
                tech_win = False
                poc_status = random.choice(["Completed", "Abandoned"])
                blocker = random.choice(BLOCKERS[1:])
            else:
                # Lost commercially, but won technically!
                criteria_met = criteria_total
                tech_win = True
                poc_status = "Completed"
                blocker = "None - Criteria Cleared Successfully"
        else: # Open
            criteria_met = random.randint(2, criteria_total - 1)
            tech_win = False
            poc_status = random.choice(["In Progress", "In Progress", "Scope Paused"])
            blocker = random.choice(BLOCKERS)

        total_hours = round(random.uniform(25.0, 95.0) + (criteria_total * 4.5), 1)
        infra_cost = round(random.uniform(350, 4800), 2)
        complexity = "High Enterprise" if criteria_total >= 10 else ("Medium" if criteria_total >= 7 else "Standard")

        pocs.append({
            "poc_id": f"POC-{poc_counter:05d}",
            "opportunity_id": opp["opportunity_id"],
            "lead_se_id": se_id,
            "poc_name": f"POV - {opp['opportunity_name'][:40]}",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "duration_calendar_days": duration_days,
            "poc_status": poc_status,
            "complexity_level": complexity,
            "technical_criteria_total": criteria_total,
            "technical_criteria_met": criteria_met,
            "criteria_success_rate_pct": round((criteria_met / criteria_total) * 100, 1),
            "is_technical_win": tech_win,
            "total_se_hours_spent": total_hours,
            "cloud_lab_infra_cost_usd": infra_cost,
            "technical_blocker_summary": blocker
        })
        poc_counter += 1

    path = DATA_DIR / "poc_projects.csv"
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(pocs[0].keys()))
        writer.writeheader()
        writer.writerows(pocs)
    print(f"-> Generated {len(pocs)} POC Projects at {path}")
    return pocs

# ---------------------------------------------------------
# 7. GENERATE RFP / SECURITY QUESTIONNAIRES
# ---------------------------------------------------------
def generate_rfps(opportunities, solution_engineers):
    rfps = []
    rfp_counter = 1

    for opp in opportunities:
        # RFPs typically in Enterprise/Strategic or large deals
        if opp["annual_contract_value_usd"] < 120000 and random.random() > 0.15:
            continue
        if random.random() > 0.40:
            continue

        se_id = opp["se_assigned_id"] or random.choice(solution_engineers)["se_id"]
        opp_created = datetime.date.fromisoformat(opp["created_date"])
        req_date = opp_created + datetime.timedelta(days=random.randint(10, 30))
        turnaround_days = random.randint(7, 24)
        due_date = req_date + datetime.timedelta(days=turnaround_days)
        sub_date = due_date - datetime.timedelta(days=random.randint(0, 3))

        questions = random.randint(45, 320)
        compliance_pct = round(random.uniform(78.5, 99.2), 1)
        hours = round(questions * random.uniform(0.12, 0.25), 1)

        if opp["deal_status"] == "Closed Won":
            status = "Won"
        elif opp["deal_status"] == "Closed Lost":
            status = "Lost" if random.random() < 0.75 else "Disqualified"
        else:
            status = "In Review"

        rfps.append({
            "rfp_id": f"RFP-{rfp_counter:05d}",
            "opportunity_id": opp["opportunity_id"],
            "assigned_se_id": se_id,
            "rfp_title": f"RFP Submission - {opp['opportunity_name'][:35]}",
            "request_date": req_date.isoformat(),
            "due_date": due_date.isoformat(),
            "submission_date": sub_date.isoformat(),
            "turnaround_days": turnaround_days,
            "questions_count": questions,
            "compliance_score_pct": compliance_pct,
            "rfp_status": status,
            "se_effort_hours": hours
        })
        rfp_counter += 1

    path = DATA_DIR / "rfp_requests.csv"
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rfps[0].keys()))
        writer.writeheader()
        writer.writerows(rfps)
    print(f"-> Generated {len(rfps)} RFP Requests at {path}")
    return rfps

# ---------------------------------------------------------
# MAIN ORCHESTRATOR
# ---------------------------------------------------------
def main():
    print("=" * 60)
    print("Generating Enterprise Pre-Sales Analytics Synthetic Data...")
    print("=" * 60)
    write_products()
    ses = generate_solution_engineers()
    accounts = generate_accounts(num_accounts=220)
    opps = generate_opportunities(accounts, ses, num_opps=750)
    generate_presales_activities(opps, ses)
    generate_pocs(opps, ses)
    generate_rfps(opps, ses)
    print("=" * 60)
    print("[OK] All Pre-Sales datasets generated successfully in sample_data/!")
    print("=" * 60)

if __name__ == "__main__":
    main()
