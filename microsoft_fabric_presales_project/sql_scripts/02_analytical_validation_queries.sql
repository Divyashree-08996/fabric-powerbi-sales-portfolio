-- =====================================================================================
-- Microsoft Fabric Pre-Sales Analytics - Validation & Deep Dive Queries
-- Run against: Fabric SQL Analytics Endpoint or Fabric Warehouse
-- =====================================================================================

-- QUERY 1: Pre-Sales Engagement ROI & Win Rate Lift Analysis
-- Evaluates the business impact of Solution Engineering involvement across Deal Size Tiers
SELECT 
    o.deal_size_tier,
    COUNT(f.opportunity_sk) AS total_closed_deals,
    -- Pre-Sales Involved
    SUM(CASE WHEN f.is_presales_engaged = 1 THEN 1 ELSE 0 END) AS presales_deals_count,
    ROUND(100.0 * SUM(CASE WHEN f.is_presales_engaged = 1 AND f.is_won = 1 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN f.is_presales_engaged = 1 THEN 1 ELSE 0 END), 0), 1) AS presales_win_rate_pct,
    -- Unassisted / No Pre-Sales
    SUM(CASE WHEN f.is_presales_engaged = 0 THEN 1 ELSE 0 END) AS unassisted_deals_count,
    ROUND(100.0 * SUM(CASE WHEN f.is_presales_engaged = 0 AND f.is_won = 1 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN f.is_presales_engaged = 0 THEN 1 ELSE 0 END), 0), 1) AS unassisted_win_rate_pct,
    -- Win Rate Lift
    ROUND(
        (100.0 * SUM(CASE WHEN f.is_presales_engaged = 1 AND f.is_won = 1 THEN 1 ELSE 0 END) / 
         NULLIF(SUM(CASE WHEN f.is_presales_engaged = 1 THEN 1 ELSE 0 END), 0)) -
        (100.0 * SUM(CASE WHEN f.is_presales_engaged = 0 AND f.is_won = 1 THEN 1 ELSE 0 END) / 
         NULLIF(SUM(CASE WHEN f.is_presales_engaged = 0 THEN 1 ELSE 0 END), 0)), 1
    ) AS win_rate_lift_points,
    -- Total Won ACV
    SUM(CASE WHEN f.is_won = 1 THEN f.annual_contract_value_usd ELSE 0 END) AS total_won_acv,
    SUM(CASE WHEN f.is_won = 1 AND f.is_presales_engaged = 1 THEN f.annual_contract_value_usd ELSE 0 END) AS presales_influenced_won_acv
FROM gold_fact_opportunity_snapshot f
INNER JOIN gold_dim_opportunity o ON f.opportunity_sk = o.opportunity_sk
WHERE f.is_closed = 1
GROUP BY o.deal_size_tier
ORDER BY total_won_acv DESC;


-- QUERY 2: Proof of Concept (POC) Funnel & Technical Win vs. Commercial Conversion
-- Analyzes whether technical validation leads to actual revenue realization
SELECT 
    p.product_category,
    COUNT(poc.poc_sk) AS total_pocs,
    SUM(CASE WHEN poc.is_technical_win = 1 THEN 1 ELSE 0 END) AS technical_wins,
    ROUND(100.0 * SUM(CASE WHEN poc.is_technical_win = 1 THEN 1 ELSE 0 END) / COUNT(poc.poc_sk), 1) AS technical_win_rate_pct,
    SUM(CASE WHEN poc.is_technical_win = 1 AND f.is_won = 1 THEN 1 ELSE 0 END) AS tech_and_commercial_wins,
    ROUND(100.0 * SUM(CASE WHEN poc.is_technical_win = 1 AND f.is_won = 1 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN poc.is_technical_win = 1 THEN 1 ELSE 0 END), 0), 1) AS tech_to_commercial_conversion_pct,
    ROUND(AVG(poc.duration_calendar_days), 1) AS avg_poc_duration_days,
    ROUND(AVG(poc.total_se_hours_spent), 1) AS avg_se_hours_per_poc,
    SUM(poc.total_poc_investment_usd) AS total_poc_cost_usd,
    SUM(CASE WHEN f.is_won = 1 THEN f.annual_contract_value_usd ELSE 0 END) AS won_acv_from_pocs
FROM gold_fact_poc poc
INNER JOIN gold_dim_product p ON poc.product_sk = p.product_sk
LEFT JOIN gold_fact_opportunity_snapshot f ON poc.opportunity_sk = f.opportunity_sk
GROUP BY p.product_category
ORDER BY total_pocs DESC;


-- QUERY 3: Solution Engineer Individual Utilization & Pre-Sales Productivity
-- Calculates SE customer-facing hours, won revenue influenced, and effort efficiency
SELECT 
    se.se_name,
    se.region,
    se.seniority_level,
    se.specialization,
    COUNT(DISTINCT act.activity_sk) AS total_activities,
    ROUND(SUM(act.total_effort_hours), 1) AS total_se_hours_logged,
    ROUND(SUM(act.duration_hours), 1) AS customer_facing_hours,
    ROUND(SUM(act.prep_hours), 1) AS prep_hours,
    COUNT(DISTINCT act.opportunity_sk) AS opportunities_supported,
    SUM(CASE WHEN f.is_won = 1 THEN f.annual_contract_value_usd ELSE 0 END) AS total_won_acv_influenced,
    ROUND(
        SUM(CASE WHEN f.is_won = 1 THEN f.annual_contract_value_usd ELSE 0 END) / 
        NULLIF(SUM(act.total_effort_hours), 0), 2
    ) AS acv_generated_per_se_hour
FROM gold_dim_solution_engineer se
LEFT JOIN gold_fact_presales_activity act ON se.se_sk = act.se_sk
LEFT JOIN gold_fact_opportunity_snapshot f ON act.opportunity_sk = f.opportunity_sk AND f.is_closed = 1
WHERE se.se_id <> 'UNASSIGNED'
GROUP BY 
    se.se_name,
    se.region,
    se.seniority_level,
    se.specialization
ORDER BY total_won_acv_influenced DESC;


-- QUERY 4: Competitor Displacement & Technical Product Gap Loss Pareto
-- Critical feedback loop for Product Management and Pre-Sales Leadership
SELECT 
    o.competitor_name,
    o.win_loss_reason,
    COUNT(f.opportunity_sk) AS lost_deals_count,
    SUM(f.annual_contract_value_usd) AS lost_acv_usd,
    ROUND(100.0 * SUM(f.annual_contract_value_usd) / 
          SUM(SUM(f.annual_contract_value_usd)) OVER(), 2) AS pct_of_total_lost_pipeline
FROM gold_fact_opportunity_snapshot f
INNER JOIN gold_dim_opportunity o ON f.opportunity_sk = o.opportunity_sk
WHERE f.is_lost = 1 AND o.is_technical_loss = 1
GROUP BY 
    o.competitor_name,
    o.win_loss_reason
ORDER BY lost_acv_usd DESC;


-- QUERY 5: RFP Response Efficiency & Compliance Score Impact on Win Rate
-- Correlates RFP turnaround time and compliance score with win probability
SELECT 
    CASE 
        WHEN r.compliance_score_pct >= 95.0 THEN 'Tier 1: High Compliance (>=95%)'
        WHEN r.compliance_score_pct >= 88.0 THEN 'Tier 2: Medium Compliance (88-94%)'
        ELSE 'Tier 3: Low Compliance (<88%)'
    END AS compliance_tier,
    COUNT(r.rfp_sk) AS total_rfps,
    ROUND(AVG(r.turnaround_days), 1) AS avg_turnaround_days,
    ROUND(AVG(r.questions_count), 0) AS avg_questions_count,
    ROUND(AVG(r.se_effort_hours), 1) AS avg_se_hours,
    SUM(CASE WHEN r.rfp_status = 'Won' THEN 1 ELSE 0 END) AS won_rfps,
    ROUND(100.0 * SUM(CASE WHEN r.rfp_status = 'Won' THEN 1 ELSE 0 END) / COUNT(r.rfp_sk), 1) AS rfp_win_rate_pct
FROM gold_fact_rfp r
GROUP BY 
    CASE 
        WHEN r.compliance_score_pct >= 95.0 THEN 'Tier 1: High Compliance (>=95%)'
        WHEN r.compliance_score_pct >= 88.0 THEN 'Tier 2: Medium Compliance (88-94%)'
        ELSE 'Tier 3: Low Compliance (<88%)'
    END
ORDER BY rfp_win_rate_pct DESC;
