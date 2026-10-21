-- =====================================================================================
-- Microsoft Fabric SQL Analytics Endpoint / Warehouse Views
-- Database / Lakehouse: presales_lakehouse
-- Description: Business abstraction layer exposing Gold Star Schema tables via clean SQL views.
-- =====================================================================================

-- 1. View: Pre-Sales Executive KPI Summary
CREATE OR ALTER VIEW vw_presales_executive_kpis AS
SELECT
    d.year,
    d.quarter,
    d.year_month,
    a.region,
    p.product_category,
    COUNT(f.opportunity_sk) AS total_opportunities,
    SUM(CASE WHEN f.is_closed = 1 THEN 1 ELSE 0 END) AS total_closed_deals,
    SUM(CASE WHEN f.is_won = 1 THEN 1 ELSE 0 END) AS total_won_deals,
    SUM(CASE WHEN f.is_lost = 1 THEN 1 ELSE 0 END) AS total_lost_deals,
    -- Win Rates
    ROUND(100.0 * SUM(CASE WHEN f.is_won = 1 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN f.is_closed = 1 THEN 1 ELSE 0 END), 0), 2) AS overall_win_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN f.is_won = 1 AND f.is_presales_engaged = 1 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN f.is_closed = 1 AND f.is_presales_engaged = 1 THEN 1 ELSE 0 END), 0), 2) AS presales_assisted_win_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN f.is_won = 1 AND f.is_presales_engaged = 0 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN f.is_closed = 1 AND f.is_presales_engaged = 0 THEN 1 ELSE 0 END), 0), 2) AS unassisted_win_rate_pct,
    -- Financial Values
    SUM(f.annual_contract_value_usd) AS total_pipeline_acv,
    SUM(CASE WHEN f.is_won = 1 THEN f.annual_contract_value_usd ELSE 0 END) AS won_acv,
    SUM(CASE WHEN f.is_won = 1 AND f.is_presales_engaged = 1 THEN f.annual_contract_value_usd ELSE 0 END) AS presales_influenced_won_acv,
    AVG(CASE WHEN f.is_closed = 1 THEN f.sales_cycle_days ELSE NULL END) AS avg_sales_cycle_days
FROM gold_fact_opportunity_snapshot f
INNER JOIN gold_dim_date d ON f.created_date_key = d.date_key
INNER JOIN gold_dim_account a ON f.account_sk = a.account_sk
INNER JOIN gold_dim_product p ON f.product_sk = p.product_sk
GROUP BY
    d.year,
    d.quarter,
    d.year_month,
    a.region,
    p.product_category;
GO

-- 2. View: Proof of Concept (POC) Performance & Conversion
CREATE OR ALTER VIEW vw_poc_performance_analytics AS
SELECT
    poc.poc_id,
    o.opportunity_name,
    a.account_name,
    a.region,
    a.industry,
    p.product_name,
    se.se_name AS lead_se_name,
    se.seniority_level AS se_seniority,
    d_start.full_date AS poc_start_date,
    d_end.full_date AS poc_end_date,
    poc.duration_calendar_days,
    poc.poc_status,
    poc.complexity_level,
    poc.technical_criteria_total,
    poc.technical_criteria_met,
    poc.criteria_success_rate_pct,
    poc.is_technical_win,
    f_opp.is_won AS is_commercial_win,
    f_opp.annual_contract_value_usd AS deal_acv,
    poc.total_se_hours_spent,
    poc.cloud_lab_infra_cost_usd,
    poc.total_poc_investment_usd,
    -- Outcome Classification
    CASE 
        WHEN poc.is_technical_win = 1 AND f_opp.is_won = 1 THEN 'Double Win (Tech & Commercial)'
        WHEN poc.is_technical_win = 1 AND f_opp.is_lost = 1 THEN 'Tech Win, Commercial Loss'
        WHEN poc.is_technical_win = 0 AND f_opp.is_lost = 1 THEN 'Complete Loss (Tech Blocker)'
        ELSE 'In Flight / Pending'
    END AS poc_outcome_category,
    poc.technical_blocker_summary
FROM gold_fact_poc poc
INNER JOIN gold_dim_opportunity o ON poc.opportunity_sk = o.opportunity_sk
INNER JOIN gold_dim_account a ON poc.account_sk = a.account_sk
INNER JOIN gold_dim_solution_engineer se ON poc.lead_se_sk = se.se_sk
INNER JOIN gold_dim_product p ON poc.product_sk = p.product_sk
INNER JOIN gold_dim_date d_start ON poc.start_date_key = d_start.date_key
INNER JOIN gold_dim_date d_end ON poc.end_date_key = d_end.date_key
LEFT JOIN gold_fact_opportunity_snapshot f_opp ON poc.opportunity_sk = f_opp.opportunity_sk;
GO

-- 3. View: Solution Engineer Workload & Activity Effort
CREATE OR ALTER VIEW vw_se_workload_capacity AS
SELECT
    d.year,
    d.year_month,
    se.se_id,
    se.se_name,
    se.region,
    se.seniority_level,
    se.specialization,
    se.target_weekly_hours,
    se.hourly_cost_rate_usd,
    COUNT(act.activity_sk) AS total_activities_conducted,
    SUM(act.duration_hours) AS total_delivery_hours,
    SUM(act.prep_hours) AS total_prep_hours,
    SUM(act.total_effort_hours) AS total_effort_hours,
    SUM(act.activity_cost_usd) AS total_engagement_cost_usd,
    AVG(act.customer_attendees_count) AS avg_attendees_per_session,
    SUM(CASE WHEN t.activity_name = 'Standard Product Demo' THEN 1 ELSE 0 END) AS count_standard_demos,
    SUM(CASE WHEN t.activity_name = 'Custom Tailored Demo' THEN 1 ELSE 0 END) AS count_custom_demos,
    SUM(CASE WHEN t.activity_name = 'Architecture Design Session (ADS)' THEN 1 ELSE 0 END) AS count_ads_sessions,
    SUM(CASE WHEN t.activity_name = 'Hands-on Technical Workshop' THEN 1 ELSE 0 END) AS count_workshops
FROM gold_fact_presales_activity act
INNER JOIN gold_dim_date d ON act.activity_date_key = d.date_key
INNER JOIN gold_dim_solution_engineer se ON act.se_sk = se.se_sk
INNER JOIN gold_dim_activity_type t ON act.activity_type_sk = t.activity_type_sk
GROUP BY
    d.year,
    d.year_month,
    se.se_id,
    se.se_name,
    se.region,
    se.seniority_level,
    se.specialization,
    se.target_weekly_hours,
    se.hourly_cost_rate_usd;
GO

-- 4. View: Technical Win/Loss & Competitor Displacement
CREATE OR ALTER VIEW vw_technical_win_loss_analysis AS
SELECT
    p.product_name,
    p.product_category,
    o.competitor_name,
    o.win_loss_reason,
    o.is_technical_loss,
    COUNT(f.opportunity_sk) AS deal_count,
    SUM(f.annual_contract_value_usd) AS total_acv_impact,
    AVG(f.sales_cycle_days) AS avg_sales_cycle_days
FROM gold_fact_opportunity_snapshot f
INNER JOIN gold_dim_opportunity o ON f.opportunity_sk = o.opportunity_sk
INNER JOIN gold_dim_product p ON f.product_sk = p.product_sk
WHERE f.is_lost = 1
GROUP BY
    p.product_name,
    p.product_category,
    o.competitor_name,
    o.win_loss_reason,
    o.is_technical_loss;
GO
