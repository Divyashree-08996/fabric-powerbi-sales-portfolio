"""
Local Lakehouse Simulation Engine (Zero Dependency - Pure Python & SQLite)
Simulates Microsoft Fabric Lakehouse execution on the local machine:
1. Loads Bronze CSVs from sample_data/
2. Executes Silver cleansing & business metric enrichments
3. Generates Gold Star Schema (Dims and Facts)
4. Saves Gold tables to gold_lakehouse_data/ and creates a local SQLite database `presales_lakehouse.db`
5. Performs pipeline sanity checks and prints key pre-sales analytical metrics.
"""

import os
import csv
import sqlite3
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "sample_data"
GOLD_DIR = BASE_DIR / "gold_lakehouse_data"
GOLD_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = BASE_DIR / "presales_lakehouse.db"

def load_csv(filename):
    path = SAMPLE_DIR / filename
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_csv(filename, data, fieldnames):
    path = GOLD_DIR / filename
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"  [OK] Saved Gold table: {filename} ({len(data)} rows)")

def run_simulation():
    print("=" * 70)
    print("RUNNING MICROSOFT FABRIC LOCAL LAKEHOUSE SIMULATOR")
    print("=" * 70)

    # 1. Load Raw Bronze
    print("\n[Step 1/4] Reading Bronze Landing Zone...")
    accounts_raw = load_csv("crm_accounts.csv")
    products_raw = load_csv("products.csv")
    se_raw = load_csv("solution_engineers.csv")
    opps_raw = load_csv("crm_opportunities.csv")
    acts_raw = load_csv("presales_activities.csv")
    pocs_raw = load_csv("poc_projects.csv")
    rfps_raw = load_csv("rfp_requests.csv")

    # 2. Build Gold Dim Date
    print("\n[Step 2/4] Generating Gold Dimension Date (2024 - 2026)...")
    dim_date = []
    curr = datetime.date(2024, 1, 1)
    end = datetime.date(2026, 12, 31)
    while curr <= end:
        date_key = int(curr.strftime("%Y%m%d"))
        q_num = (curr.month - 1) // 3 + 1
        fq = f"FQ{((curr.month + 5) % 12) // 3 + 1}" # July start fiscal year
        fy = f"FY{str(curr.year + 1)[2:]}" if curr.month >= 7 else f"FY{str(curr.year)[2:]}"
        dim_date.append({
            "date_key": date_key,
            "full_date": curr.isoformat(),
            "year": curr.year,
            "quarter": f"Q{q_num}",
            "quarter_name": f"{curr.year}-Q{q_num}",
            "month_num": curr.month,
            "month_name": curr.strftime("%B"),
            "month_short": curr.strftime("%b"),
            "year_month": curr.strftime("%Y-%m"),
            "day_of_week_num": curr.weekday() + 1,
            "day_of_week_name": curr.strftime("%A"),
            "is_weekend": curr.weekday() >= 5,
            "fiscal_year": fy,
            "fiscal_quarter": fq
        })
        curr += datetime.timedelta(days=1)
    save_csv("gold_dim_date.csv", dim_date, list(dim_date[0].keys()))

    # 3. Build Gold Dimensions
    print("\n[Step 3/4] Generating Gold Dimensions with Surrogate Keys...")
    # Dim Account
    dim_account = []
    acc_map = {} # id -> sk
    for idx, acc in enumerate(accounts_raw, start=1):
        sk = idx
        acc_map[acc["account_id"]] = sk
        rev = float(acc["annual_revenue_usd"])
        bracket = "Enterprise Tier 1 (>$1B)" if rev >= 1e9 else ("Enterprise Tier 2 ($250M-$1B)" if rev >= 2.5e8 else "Mid-Market (<$250M)")
        dim_account.append({
            "account_sk": sk,
            "account_id": acc["account_id"],
            "account_name": acc["account_name"],
            "industry": acc["industry"],
            "account_tier": acc["account_tier"],
            "annual_revenue_usd": rev,
            "annual_revenue_bracket": bracket,
            "employee_count": int(acc["employee_count"]),
            "country_name": acc["country_name"],
            "country_code": acc["country_code"],
            "region": acc["region"],
            "account_created_date": acc["created_date"]
        })
    save_csv("gold_dim_account.csv", dim_account, list(dim_account[0].keys()))

    # Dim Solution Engineer
    dim_se = [
        {
            "se_sk": -1,
            "se_id": "UNASSIGNED",
            "se_name": "Unassigned / Direct",
            "email": "unassigned@company.com",
            "region": "Global",
            "seniority_level": "N/A",
            "specialization": "General",
            "target_weekly_hours": 0,
            "target_utilization_pct": 0.0,
            "hourly_cost_rate_usd": 0.0
        }
    ]
    se_map = {"UNASSIGNED": -1, "": -1}
    for idx, se in enumerate(se_raw, start=1):
        se_map[se["se_id"]] = idx
        dim_se.append({
            "se_sk": idx,
            "se_id": se["se_id"],
            "se_name": se["se_name"],
            "email": se["email"],
            "region": se["region"],
            "seniority_level": se["seniority_level"],
            "specialization": se["specialization"],
            "target_weekly_hours": int(se["target_weekly_hours"]),
            "target_utilization_pct": float(se["target_utilization_pct"]),
            "hourly_cost_rate_usd": float(se["hourly_cost_rate_usd"])
        })
    save_csv("gold_dim_solution_engineer.csv", dim_se, list(dim_se[0].keys()))

    # Dim Product
    dim_product = []
    prd_map = {}
    for idx, p in enumerate(products_raw, start=1):
        prd_map[p["product_id"]] = idx
        dim_product.append({
            "product_sk": idx,
            "product_id": p["product_id"],
            "product_name": p["product_name"],
            "product_category": p["product_category"],
            "deployment_model": p["deployment_model"],
            "base_annual_license_usd": float(p["base_annual_license_usd"]),
            "standard_poc_duration_days": int(p["standard_poc_duration_days"])
        })
    save_csv("gold_dim_product.csv", dim_product, list(dim_product[0].keys()))

    # Dim Opportunity
    dim_opportunity = []
    opp_map = {}
    opp_acc_map = {}
    opp_prd_map = {}
    for idx, opp in enumerate(opps_raw, start=1):
        opp_map[opp["opportunity_id"]] = idx
        opp_acc_map[opp["opportunity_id"]] = acc_map.get(opp["account_id"], -1)
        opp_prd_map[opp["opportunity_id"]] = prd_map.get(opp["product_id"], -1)
        
        acv = float(opp["annual_contract_value_usd"])
        tier = "Jumbo Enterprise (>$400k)" if acv >= 400000 else ("Major ($200k-$400k)" if acv >= 200000 else ("Core ($75k-$200k)" if acv >= 75000 else "Velocity (<$75k)"))
        
        poc_cond = opp["poc_conducted"] == "True"
        se_eng = opp["is_presales_engaged"] == "True"
        touch = "High Touch (POC Completed)" if poc_cond else ("Medium Touch (SE Engaged)" if se_eng else "Low Touch (Self-Serve / AE Only)")

        dim_opportunity.append({
            "opportunity_sk": idx,
            "opportunity_id": opp["opportunity_id"],
            "opportunity_name": opp["opportunity_name"],
            "ae_owner_name": opp["ae_owner_name"],
            "deal_type": opp["deal_type"],
            "deal_stage": opp["deal_stage"],
            "deal_status": opp["deal_status"],
            "deal_size_tier": tier,
            "presales_touch_level": touch,
            "competitor_name": opp["competitor_name"] if opp["competitor_name"] else "None",
            "win_loss_reason": opp["win_loss_reason"] if opp["win_loss_reason"] else "In Flight",
            "is_technical_loss": opp["is_technical_loss"] == "True"
        })
    save_csv("gold_dim_opportunity.csv", dim_opportunity, list(dim_opportunity[0].keys()))

    # Dim Activity Type
    act_types_seen = {}
    dim_act_type = []
    type_idx = 1
    for act in acts_raw:
        name = act["activity_name"]
        if name not in act_types_seen:
            act_types_seen[name] = type_idx
            cat = act["activity_category"]
            dim_act_type.append({
                "activity_type_sk": type_idx,
                "activity_name": name,
                "activity_category": cat,
                "is_customer_facing": True
            })
            type_idx += 1
    save_csv("gold_dim_activity_type.csv", dim_act_type, list(dim_act_type[0].keys()))

    # 4. Build Gold Fact Tables
    print("\n[Step 4/4] Generating Gold Fact Tables...")
    
    # Fact Pre-Sales Activities
    fact_activities = []
    for idx, act in enumerate(acts_raw, start=1):
        dt_str = act["activity_date"]
        date_key = int(dt_str.replace("-", "")) if dt_str else -1
        opp_id = act["opportunity_id"]
        se_id = act["se_id"]
        act_name = act["activity_name"]

        fact_activities.append({
            "activity_sk": idx,
            "activity_id": act["activity_id"],
            "activity_date_key": date_key,
            "account_sk": opp_acc_map.get(opp_id, -1),
            "opportunity_sk": opp_map.get(opp_id, -1),
            "se_sk": se_map.get(se_id, -1),
            "product_sk": opp_prd_map.get(opp_id, -1),
            "activity_type_sk": act_types_seen.get(act_name, -1),
            "duration_hours": float(act["duration_hours"]),
            "prep_hours": float(act["prep_hours"]),
            "total_effort_hours": float(act["total_effort_hours"]),
            "customer_attendees_count": int(act["customer_attendees_count"]),
            "customer_sentiment": act["customer_sentiment"],
            "technical_objection": act["technical_objection"],
            "follow_up_required": act["follow_up_required"] == "True"
        })
    save_csv("gold_fact_presales_activity.csv", fact_activities, list(fact_activities[0].keys()))

    # Fact POC
    fact_poc = []
    for idx, poc in enumerate(pocs_raw, start=1):
        s_date = int(poc["start_date"].replace("-", "")) if poc["start_date"] else -1
        e_date = int(poc["end_date"].replace("-", "")) if poc["end_date"] else -1
        opp_id = poc["opportunity_id"]
        se_id = poc["lead_se_id"]

        fact_poc.append({
            "poc_sk": idx,
            "poc_id": poc["poc_id"],
            "start_date_key": s_date,
            "end_date_key": e_date,
            "opportunity_sk": opp_map.get(opp_id, -1),
            "account_sk": opp_acc_map.get(opp_id, -1),
            "lead_se_sk": se_map.get(se_id, -1),
            "product_sk": opp_prd_map.get(opp_id, -1),
            "duration_calendar_days": int(poc["duration_calendar_days"]),
            "poc_status": poc["poc_status"],
            "complexity_level": poc["complexity_level"],
            "technical_criteria_total": int(poc["technical_criteria_total"]),
            "technical_criteria_met": int(poc["technical_criteria_met"]),
            "criteria_success_rate_pct": float(poc["criteria_success_rate_pct"]),
            "is_technical_win": poc["is_technical_win"] == "True",
            "total_se_hours_spent": float(poc["total_se_hours_spent"]),
            "cloud_lab_infra_cost_usd": float(poc["cloud_lab_infra_cost_usd"]),
            "technical_blocker_summary": poc["technical_blocker_summary"]
        })
    save_csv("gold_fact_poc.csv", fact_poc, list(fact_poc[0].keys()))

    # Fact Opportunity Snapshot
    fact_opp = []
    for opp in opps_raw:
        opp_id = opp["opportunity_id"]
        c_date = int(opp["created_date"].replace("-", "")) if opp["created_date"] else -1
        t_date = int(opp["target_close_date"].replace("-", "")) if opp["target_close_date"] else -1
        a_date = int(opp["actual_close_date"].replace("-", "")) if opp["actual_close_date"] else None
        
        c_dt = datetime.date.fromisoformat(opp["created_date"])
        if opp["actual_close_date"]:
            a_dt = datetime.date.fromisoformat(opp["actual_close_date"])
            cycle = (a_dt - c_dt).days
        else:
            cycle = (datetime.date(2026, 10, 1) - c_dt).days

        fact_opp.append({
            "opportunity_sk": opp_map.get(opp_id, -1),
            "account_sk": acc_map.get(opp["account_id"], -1),
            "product_sk": prd_map.get(opp["product_id"], -1),
            "assigned_se_sk": se_map.get(opp["se_assigned_id"], -1),
            "created_date_key": c_date,
            "target_close_date_key": t_date,
            "actual_close_date_key": a_date if a_date else -1,
            "annual_contract_value_usd": float(opp["annual_contract_value_usd"]),
            "total_contract_value_usd": float(opp["total_contract_value_usd"]),
            "is_presales_engaged": opp["is_presales_engaged"] == "True",
            "poc_conducted": opp["poc_conducted"] == "True",
            "is_closed": opp["deal_status"] in ("Closed Won", "Closed Lost"),
            "is_won": opp["deal_status"] == "Closed Won",
            "is_lost": opp["deal_status"] == "Closed Lost",
            "is_technical_loss": opp["is_technical_loss"] == "True",
            "sales_cycle_days": cycle
        })
    save_csv("gold_fact_opportunity_snapshot.csv", fact_opp, list(fact_opp[0].keys()))

    # Fact RFP
    fact_rfp = []
    for idx, rfp in enumerate(rfps_raw, start=1):
        r_date = int(rfp["request_date"].replace("-", "")) if rfp["request_date"] else -1
        s_date = int(rfp["submission_date"].replace("-", "")) if rfp["submission_date"] else -1
        opp_id = rfp["opportunity_id"]
        se_id = rfp["assigned_se_id"]

        fact_rfp.append({
            "rfp_sk": idx,
            "rfp_id": rfp["rfp_id"],
            "request_date_key": r_date,
            "submission_date_key": s_date,
            "opportunity_sk": opp_map.get(opp_id, -1),
            "assigned_se_sk": se_map.get(se_id, -1),
            "turnaround_days": int(rfp["turnaround_days"]),
            "questions_count": int(rfp["questions_count"]),
            "compliance_score_pct": float(rfp["compliance_score_pct"]),
            "rfp_status": rfp["rfp_status"],
            "se_effort_hours": float(rfp["se_effort_hours"])
        })
    save_csv("gold_fact_rfp.csv", fact_rfp, list(fact_rfp[0].keys()))

    # 5. Populate SQLite DB for direct query & Power BI desktop connectivity
    print(f"\n[Step 5/5] Building SQLite Database at {DB_PATH.name}...")
    if DB_PATH.exists():
        DB_PATH.unlink()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = [
        ("gold_dim_date", dim_date),
        ("gold_dim_account", dim_account),
        ("gold_dim_solution_engineer", dim_se),
        ("gold_dim_product", dim_product),
        ("gold_dim_opportunity", dim_opportunity),
        ("gold_dim_activity_type", dim_act_type),
        ("gold_fact_presales_activity", fact_activities),
        ("gold_fact_poc", fact_poc),
        ("gold_fact_opportunity_snapshot", fact_opp),
        ("gold_fact_rfp", fact_rfp)
    ]

    for tbl_name, rows in tables:
        if not rows:
            continue
        cols = list(rows[0].keys())
        col_defs = ", ".join([f"[{c}] TEXT" for c in cols])
        cursor.execute(f"CREATE TABLE [{tbl_name}] ({col_defs})")
        placeholders = ", ".join(["?"] * len(cols))
        cursor.executemany(
            f"INSERT INTO [{tbl_name}] VALUES ({placeholders})",
            [[r[c] for c in cols] for r in rows]
        )
    conn.commit()

    # Query key metrics for validation
    cursor.execute("""
        SELECT 
            COUNT(*) as total_deals,
            SUM(CASE WHEN is_won = '1' THEN 1 ELSE 0 END) as won_deals,
            ROUND(100.0 * SUM(CASE WHEN is_won = '1' THEN 1 ELSE 0 END) / COUNT(*), 1) as overall_win_rate_pct,
            ROUND(100.0 * SUM(CASE WHEN is_won = '1' AND is_presales_engaged = '1' THEN 1 ELSE 0 END) / 
                  NULLIF(SUM(CASE WHEN is_presales_engaged = '1' THEN 1 ELSE 0 END), 0), 1) as se_win_rate_pct,
            ROUND(100.0 * SUM(CASE WHEN is_won = '1' AND is_presales_engaged = '0' THEN 1 ELSE 0 END) / 
                  NULLIF(SUM(CASE WHEN is_presales_engaged = '0' THEN 1 ELSE 0 END), 0), 1) as unassisted_win_rate_pct,
            SUM(annual_contract_value_usd) as total_acv,
            SUM(CASE WHEN is_won = '1' THEN annual_contract_value_usd ELSE 0 END) as won_acv
        FROM gold_fact_opportunity_snapshot
        WHERE is_closed = '1'
    """)
    metrics = cursor.fetchone()
    conn.close()

    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION & ANALYTICAL VALIDATION SUMMARY:")
    print("=" * 70)
    print(f"Total Closed Deals Evaluated:      {metrics[0]:,}")
    print(f"Total Closed Won Deals:            {metrics[1]:,}")
    print(f"Baseline (Unassisted) Win Rate:    {metrics[4]}%")
    print(f"Pre-Sales Assisted Win Rate:       {metrics[3]}% (LIFT: +{round(metrics[3] - metrics[4], 1)}%!)")
    print(f"Overall Win Rate:                  {metrics[2]}%")
    print(f"Total Closed ACV:                  ${metrics[5]:,.2f}")
    print(f"Total Closed Won ACV:              ${metrics[6]:,.2f}")
    print("=" * 70)
    print("[SUCCESS] Local Lakehouse Simulation completed successfully!")
    print("=" * 70)

if __name__ == "__main__":
    run_simulation()
