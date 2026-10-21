# 📊 Power BI Dashboard Design & Visual Specifications
## Microsoft Fabric End-to-End Pre-Sales Analytics

This document provides a detailed blueprint for building a 4-page enterprise Power BI report powered by **Microsoft Fabric Direct Lake**.

---

## 🎨 Design Philosophy & UX Standards
- **Grid Layout**: 1920x1080 (16:9 widescreen) canvas.
- **Top Bar**: Global Title, Breadcrumbs, Last Refreshed (from Fabric OneLake commit timestamp), and Help Tooltip.
- **Left Collapsible Slicer Panel**: Date Range (Fiscal Year / Quarter), Region, Product Category, Account Tier, Deal Size Tier.
- **Visual Container Cards**: 8px corner radius, `#EDEBE9` subtle border, 16px internal padding, no visual headers.
- **Color Coding**:
  - Primary / Pre-Sales Influenced: `#0078D4` (Microsoft Blue)
  - Success / Closed Won: `#107C41` (Fluent Green)
  - Loss / Unassisted: `#D83B01` (Orange-Red)
  - Neutral / Benchmarks: `#605E5C` (Slate Gray)

---

## 🖥️ Page 1: Pre-Sales Executive Command Center
**Target Audience**: VP of Pre-Sales, Chief Revenue Officer (CRO), VP of Global Sales.  
**Objective**: Demonstrate the bottom-line ROI and revenue lift driven by the Solutions Engineering organization.

### 1. Wireframe Layout
```
+----------------------------------------------------------------------------------------------------+
| 🌐 LOGO | PRE-SALES EXECUTIVE COMMAND CENTER | Direct Lake | Last Refreshed: [Commit Timestamp]   |
+----------------------------------------------------------------------------------------------------+
| [ KPI 1 ]            | [ KPI 2 ]            | [ KPI 3 ]            | [ KPI 4 ]          | [ KPI 5 ] |
| Pre-Sales Influenced | Pre-Sales Win Rate   | Win Rate Lift vs     | Total POCs         | Overall   |
| Won ACV ($106.7M)    | Assisted (60.0%)     | Baseline (+34.8%)    | Conducted (318)    | Win Rate  |
+---------------------------------------------+------------------------------------------------------+
| 📈 Trend Analysis (Area / Line Chart)       | 📊 Win Rate Comparison by Deal Size Tier (Clustered) |
| Monthly Won ACV: Assisted vs Unassisted     | Comparing Assisted (60%) vs Unassisted (25%)         |
| [X: Year-Month | Y: Won ACV | Legend: SE]   | [X: Deal Tier | Y: Win Rate % | Series: SE/No SE]    |
+---------------------------------------------+------------------------------------------------------+
| 🍩 Pre-Sales Revenue by Product Category     | 📋 Regional SE Performance Matrix (Matrix Table)     |
| Donut: Fabric ($42M), AI Studio ($31M), etc | Region | Pipeline | Won ACV | Win % | SE Hours | ROI|
+----------------------------------------------------------------------------------------------------+
```

### 2. Visual Component Details

#### Top KPI Cards (New Card Visual)
1. **Card 1: Pre-Sales Influenced Won ACV**
   - Measure: `[Pre-Sales Influenced Won ACV]`
   - Reference Label: `[Pre-Sales Revenue Contribution Pct]` (e.g., `85.4% of total Won ARR`)
   - Accent Bar: `#0078D4` (Blue)
2. **Card 2: Pre-Sales Assisted Win Rate**
   - Measure: `[Pre-Sales Assisted Win Rate Pct]` (Format: `0.0%`)
   - Comparison Target: `[Overall Win Rate Pct]`
3. **Card 3: Win Rate Lift (The Value Multiplier)**
   - Measure: `[Pre-Sales Win Rate Lift]` (Format: `+0.0%`)
   - Conditional Color: Green if $> 15\%$, Amber if $> 5\%$, Red if $\le 0\%$
4. **Card 4: Total POC Volume & Success**
   - Measure: `[Total POCs Count]`
   - Sub-label: `[Technical Win Rate Pct]` (e.g., `82.4% Technical Win`)
5. **Card 5: Pre-Sales Revenue Productivity**
   - Measure: `[ACV Influenced Per SE Hour]` (Format: `$#,##0 / Hr`)

#### Visual 1: Monthly Won ACV (Stacked Area Chart)
- **X-Axis**: `gold_dim_date[year_month]`
- **Y-Axis**: `[Closed Won ACV]`
- **Legend**: `gold_dim_opportunity[presales_touch_level]`
- **Insight**: Highlights the compounding growth of High Touch (POC) and Medium Touch (SE) revenue over time compared to transactional unassisted deals.

#### Visual 2: Win Rate by Deal Size Tier (Clustered Column Chart)
- **X-Axis**: `gold_dim_opportunity[deal_size_tier]` (Sorted by size)
- **Y-Axis**: 
  - Measure 1: `[Pre-Sales Assisted Win Rate Pct]`
  - Measure 2: `[Unassisted Win Rate Pct]`
- **Data Labels**: Positioned outside end, with difference callouts.

---

## 🔬 Page 2: Proof of Concept (POC) Control Tower & Velocity
**Target Audience**: Head of Solutions Architecture, POC Managers, Senior SEs.  
**Objective**: Track POC pipelines, identify aging POCs, measure conversion from technical win to commercial close.

### 1. Wireframe Layout
```
+----------------------------------------------------------------------------------------------------+
| 🚀 PROOF OF CONCEPT (POC) CONTROL TOWER & VELOCITY TRACKER                                         |
+----------------------------------------------------------------------------------------------------+
| [ Active POCs: 48 ] | [ Avg Duration: 27 Days ] | [ Tech Win Rate: 84.1% ] | [ Lab Cost: $340k ]   |
+----------------------------------------------------+-----------------------------------------------+
| 🌊 Technical Win to Commercial Funnel (Funnel)    | ⏱️ POC Duration Distribution (Histogram/Boxplot)|
| POCs Started -> Criteria Met -> Tech Win -> Won ACV| Standard vs Enterprise High Complexity Days   |
+----------------------------------------------------+-----------------------------------------------+
| 🔍 Technical Blocker & Inactive Alert Table                                                        |
| Opportunity | Account | Lead SE | Days Active | Criteria Met % | Status | Key Technical Blocker    |
+----------------------------------------------------------------------------------------------------+
```

### 2. Visual Component Details

#### Visual 1: POC Conversion Funnel (Funnel Visual)
- **Stages**:
  1. Total POCs Initiated (`[Total POCs Count]`)
  2. Technical Criteria Met $> 80\%$ (`[Technical Won POCs Count]`)
  3. Commercial Proposal Submitted
  4. Closed Won Revenue Realized (`[POC Influenced Won ACV]`)
- **Key Metric Callout**: `[Commercial Conversion from Technical Win Pct]`. Shows where deals stall due to commercial/pricing friction despite technical victory.

#### Visual 2: POC Scatter / Quadrant Chart (Scatter Plot)
- **X-Axis**: `gold_fact_poc[duration_calendar_days]` (Days in field)
- **Y-Axis**: `gold_fact_poc[criteria_success_rate_pct]` (% Criteria passed)
- **Bubble Size**: `gold_fact_opportunity_snapshot[annual_contract_value_usd]`
- **Legend**: `gold_dim_product[product_category]`
- **Quadrant Lines**: X-Threshold = 30 days, Y-Threshold = 80%
  - Top-Left: **Fast Track Wins** (<30 days, >80% criteria)
  - Bottom-Right: **Danger Zone / Scope Creep** (>30 days, <80% criteria)

---

## 👥 Page 3: Solutions Engineering Workload & Capacity
**Target Audience**: SE Managers, Resource Coordinators, Operations Leads.  
**Objective**: Optimize SE allocation, balance customer delivery with prep, prevent burnout.

### 1. Wireframe Layout
```
+----------------------------------------------------------------------------------------------------+
| ⚖️ SOLUTIONS ENGINEERING WORKLOAD & RESOURCE ALLOCATION                                            |
+----------------------------------------------------------------------------------------------------+
| [ Total SE Hours: 14.8k ] | [ Utilization: 74.2% ] | [ Prep/Delivery: 1.1x ] | [ Active SEs: 20 ]  |
+----------------------------------------------------+-----------------------------------------------+
| 📊 Hours Logged by Activity Type (Bar Chart)       | 📈 SE Productivity Matrix: Hours vs Won ACV   |
| Demos vs Workshops vs ADS vs RFP Support           | X: Total SE Hours | Y: Won ACV Influenced     |
+----------------------------------------------------+-----------------------------------------------+
| 🗺️ SE Utilization Heatmap (Matrix Visual)                                                          |
| SE Name | Region | Weekly Target | Customer Hours | Prep Hours | Total % | Capacity Variance    |
+----------------------------------------------------------------------------------------------------+
```

### 2. Visual Component Details

#### Visual 1: Activity Category Breakdown (Stacked Bar Chart)
- **Y-Axis**: `gold_dim_activity_type[activity_category]`
- **X-Axis**: `[Total SE Effort Hours]`
- **Sub-breakdown**: `gold_dim_activity_type[activity_name]`
- **Data Labels**: Total hours and % of overall SE time.

#### Visual 2: SE Productivity Matrix (Scatter Chart)
- **X-Axis**: `[Total SE Effort Hours]`
- **Y-Axis**: `[Pre-Sales Influenced Won ACV]`
- **Details**: `gold_dim_solution_engineer[se_name]`
- **Legend**: `gold_dim_solution_engineer[region]`
- **Trend Line**: Linear regression illustrating output efficiency per engineer.

---

## 🛡️ Page 4: Technical Win/Loss & Competitive Product Gap Analysis
**Target Audience**: Product Management, Head of Solutions Architecture, Competitive Intelligence.  
**Objective**: Quantify the ARR impact of technical product gaps and competitor capabilities.

### 1. Wireframe Layout
```
+----------------------------------------------------------------------------------------------------+
| 🛡️ TECHNICAL WIN/LOSS & PRODUCT GAP FEEDBACK LOOP                                                  |
+----------------------------------------------------------------------------------------------------+
| [ Tech Loss Deals: 88 ] | [ Tech Loss ARR: $26.4M ] | [ Tech Loss %: 34.2% ] | [ Top Rival: Snow ] |
+----------------------------------------------------+-----------------------------------------------+
| 📉 Loss Reason Pareto Chart (Pareto Column + Line) | ⚔️ Competitor Displacement Matrix             |
| Feature Gap, Latency SLA, Security, Migration      | Competitor | Lost ARR | Won Against ARR | Ratio|
+----------------------------------------------------+-----------------------------------------------+
| 📋 Technical Loss Incident Log (Table with Drillthrough to CRM Deal)                               |
| Account | Product | Competitor | Primary Technical Blocker | ACV | SE Notes & Customer Objection |
+----------------------------------------------------------------------------------------------------+
```

### 2. Visual Component Details

#### Visual 1: Technical Loss Pareto (Combo Chart)
- **X-Axis**: `gold_dim_opportunity[win_loss_reason]` (Filtered to Closed Lost & Technical Loss)
- **Column Y-Axis**: `[Technical Loss ACV]`
- **Line Y-Axis**: Cumulative % of Lost ARR
- **Takeaway**: Directly informs Product Roadmaps on which features unlock the highest ARR.

---

## ⚡ 5. Drill-Through and Slicer Architecture
1. **SE Profile Drill-Through**:
   - Right-click any SE name on any page $\rightarrow$ Drill-through to **SE Detailed Profile**:
     - Current pipeline deals supported
     - Recent customer sentiment scores
     - Detailed activity timesheet
2. **Account 360 Drill-Through**:
   - Right-click any Account $\rightarrow$ Drill-through to **Account Pre-Sales History**:
     - All past demos, workshops, POC results, and AE notes.
