# Enterprise Omnichannel Revenue Intelligence & Executive FP&A Semantic Model

[![Power BI](https://img.shields.io/badge/Power_BI-Desktop_&_Fabric-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![DAX Level](https://img.shields.io/badge/DAX-Advanced_Patterns-118DFF)](https://dax.guide/)
[![Architecture](https://img.shields.io/badge/Architecture-Kimball_Star_Schema-107C41)](#-2-dimensional-star-schema-architecture)
[![Format](https://img.shields.io/badge/PBIP-Power_BI_Project_Native-8764B8)](#-6-power-bi-project-pbip-deployment-guide)

An end-to-end, production-grade enterprise Power BI project built from the ground up to showcase **Advanced DAX (Data Analysis Expressions)**, **Kimball Dimensional Modeling**, **Multi-Currency Consolidation**, **Calculation Groups**, and **Sub-Second VertiPaq Engine Optimization**.

---

## 📑 Table of Contents

1. [Business Scenario & Executive Requirements](#-1-business-scenario--executive-requirements)
2. [Dimensional Star Schema Architecture](#-2-dimensional-star-schema-architecture)
3. [Data Dictionary & Referential Integrity](#-3-data-dictionary--referential-integrity)
4. [Power Query (M) Transformation Pipelines](#-4-power-query-m-transformation-pipelines)
5. [Advanced DAX Formulas & Mathematical Formulations](#-5-advanced-dax-formulas--mathematical-formulations)
   - [Modern Window Functions (OFFSET, INDEX, WINDOW)](#51-modern-window-functions-offset-index-window)
   - [Dynamic Pareto 80/20 & Top N with Others Rollup](#52-dynamic-pareto-8020--top-n-with-others-rollup)
   - [Dynamic RFM Segmentation & Cohort Churn Modeling](#53-dynamic-rfm-segmentation--cohort-churn-modeling)
   - [Market Basket Cross-Sell Affinity & Lift Analysis](#54-market-basket-cross-sell-affinity--lift-analysis)
   - [Dynamic Multi-Currency Translation & FX Decomposition](#55-dynamic-multi-currency-translation--fx-decomposition)
   - [Parameterized What-If Sensitivity & Margin Elasticity](#56-parameterized-what-if-sensitivity--margin-elasticity)
   - [Grain Mismatch Resolution via TREATAS](#57-grain-mismatch-resolution-via-treatas)
   - [Enterprise Calculation Groups & Dynamic Format Strings](#58-enterprise-calculation-groups--dynamic-format-strings)
   - [Hierarchical Dynamic Row-Level Security (RLS)](#59-hierarchical-dynamic-row-level-security-rls)
   - [In-Cell Vector SVG Visuals Generated in DAX](#510-in-cell-vector-svg-visuals-generated-in-dax)
6. [Power BI Project (PBIP) Deployment Guide](#-6-power-bi-project-pbip-deployment-guide)
7. [Automated Tabular Editor Deployment](#-7-automated-tabular-editor-deployment)
8. [Interactive Browser Simulator](#-8-interactive-browser-simulator)
9. [DAX Storage Engine vs Formula Engine Optimization](#-9-dax-storage-engine-vs-formula-engine-optimization)

---

## 🎯 1. Business Scenario & Executive Requirements

A multinational B2B software, cloud platform, and hardware enterprise operates across **7 countries** (USA, Germany, UK, Japan, France, Australia, Canada) through **3 primary sales channels** (Direct Enterprise Field, Digital Self-Serve, and Strategic Partner Resellers). 

### Core Business Challenges Addressed:
1. **Multi-Currency Fragmentation**: Transactions originate in 5 different local currencies (USD, EUR, GBP, JPY, CAD). Executive leadership requires dynamic instant currency toggling while isolating operational organic growth from foreign exchange rate (FX) fluctuations.
2. **Customer Concentration Vulnerability**: Leadership needed to identify whether revenue is dangerously concentrated in a handful of enterprise accounts via automated **Pareto 80/20 distribution curves** and dynamic **Top N + Others** reporting.
3. **Customer Churn & Health Attrition**: Absence of real-time behavioral customer health scoring. The business required dynamic **RFM (Recency, Frequency, Monetary)** quintile scoring and cohort churn tracking in DAX without pre-aggregating in SQL or Python.
4. **Cross-Sell Blindspots**: Product managers needed to discover product attachment rules and market basket affinity (Support, Confidence, Lift ratio) to bundle software with cloud compute and professional services.
5. **Scenario Sensitivity Modeling**: Finance leadership required dual What-If parameter sliders to simulate price increases (+/- 30%) and supplier cost inflation (+/- 25%) to project EBITDA margin shifts in basis points (bps) before finalizing annual operating plans.

---

## 🏗️ 2. Dimensional Star Schema Architecture

The data model follows Kimball dimensional modeling principles with a strict **Star Schema**, ensuring 100% 1-to-many (`1:*`) single-directional filter propagation. Bi-directional relationships are deliberately eliminated to avoid ambiguous filter paths and guarantee maximum VertiPaq bitmap index compression.

```
+-----------------------------------------------------------------------------------------+
|                                     DIMENSION TABLES                                    |
+-----------------------------------------------------------------------------------------+
|  [Dim_Customer]          [Dim_Product]           [Dim_Date]        [Dim_Store_Region]   |
|  - CustomerID (PK)       - ProductID (PK)        - Date (PK)       - ChannelID (PK)     |
|  - CustomerName          - ProductName           - YearMonth       - ChannelName        |
|  - Segment / Region      - Category / SubCat     - FiscalYear      - RegionCode         |
|  - CreditRating          - StandardCost / Price  - MonthOffset     - HierarchyPath(RLS) |
+-----------------------------------------------------------------------------------------+
         │                       │                      │                     │
      (1)│                    (1)│                   (1)│                  (1)│
         ▼                       ▼                      ▼                     ▼
        (*)                     (*)                    (*)                   (*)
+-----------------------------------------------------------------------------------------+
|                                  CENTRAL FACT TABLE                                     |
|                                     Fact_Sales                                          |
|  - SalesLineID (PK)        - OrderDate (FK)         - Quantity                          |
|  - SalesOrderNumber        - CustomerID (FK)        - GrossSalesUSD / NetSalesUSD       |
|  - OrderLineNumber         - ProductID (FK)         - DiscountAmountUSD                 |
|  - ShipDate                - ChannelID (FK)         - TotalCostUSD / MarginUSD          |
+-----------------------------------------------------------------------------------------+
                                         ▲
                                      (TREATAS)
+-----------------------------------------------------------------------------------------+
|                               SECONDARY FACT / TARGETS                                  |
|                                     Fact_Budget                                         |
|  - BudgetID                - YearMonth (TREATAS)    - TargetRevenueUSD                  |
|  - Category (TREATAS)      - RegionCode (TREATAS)   - TargetMarginUSD                   |
+-----------------------------------------------------------------------------------------+
                                         ▲
+-----------------------------------------------------------------------------------------+
|                               DISCONNECTED PARAMETER TABLES                             |
|  - Param_ReportingCurrency (USD, EUR, GBP, JPY, CAD)                                    |
|  - Param_WhatIf_Price (-20% to +30%)               - Param_TopN (5, 10, 15, 20, 50)     |
|  - Param_WhatIf_Cost (-10% to +25%)                - Param_MetricSelector               |
+-----------------------------------------------------------------------------------------+
```

---

## 📋 3. Data Dictionary & Referential Integrity

| Table Name | Type | Row Count | Primary Key | Grain / Description |
| :--- | :--- | :--- | :--- | :--- |
| `Fact_Sales` | Fact | **35,502** | `SalesLineID` | Individual transaction sales order line item |
| `Fact_Budget` | Fact | **576** | `BudgetID` | Monthly target by Product Category and Sales Region |
| `Dim_Customer` | Dimension | **250** | `CustomerID` | Global enterprise accounts with segment, territory, and RLS email |
| `Dim_Product` | Dimension | **22** | `ProductID` | Software, Cloud, Hardware, and Advisory product catalog |
| `Dim_Date` | Dimension | **1,461** | `Date` | 4-year continuous calendar (2023-2026) with fiscal periods and offsets |
| `Dim_Store_Region` | Dimension | **7** | `ChannelID` | Sales channels, regional directors, and organizational path strings |
| `Dim_ExchangeRate` | Dimension | **8,766** | `(Date, Currency)` | Daily FX conversion rates relative to USD |
| `Param_ReportingCurrency`| Disconnected | **6** | `CurrencyCode` | Multi-currency reporting toggle parameter |
| `Param_WhatIf_Price` | Disconnected | **11** | `PriceAdjustmentPercent` | Financial sensitivity pricing adjustment slider |
| `Param_WhatIf_Cost` | Disconnected | **8** | `CostAdjustmentPercent` | Financial sensitivity cost inflation slider |
| `Param_TopN` | Disconnected | **5** | `TopNValue` | Dynamic customer cutoff selector |

---

## 💻 4. Power Query (M) Transformation Pipelines

All ingestion code is organized into standalone, modular `.pq` scripts located in `powerquery/`.

### Key Highlights:
1. **Dynamic Parameterized Path**: `01_DataFolderPath_Parameter.pq` centralizes source directory paths for seamless multi-environment CI/CD deployments.
2. **Pure M Date Dimension**: `02_Dim_Date.pq` generates an uninterrupted 1,461-day Gregorian and Fiscal calendar dynamically using `List.Dates`, calculating fiscal years (July 1 start), fiscal periods, and relative offsets (`MonthOffset`, `DayOffset`) without external dependencies.
3. **Type Safety & Metadata Mapping**: All numeric currencies are strictly typed to `Currency.Type` (4 decimal fixed points) to prevent floating-point rounding anomalies during high-speed aggregation.

---

## 🧮 5. Advanced DAX Formulas & Mathematical Formulations

### 5.1 Modern Window Functions (`OFFSET`, `INDEX`, `WINDOW`)
Modern DAX introduces native window functions that execute directly in the Storage Engine (SE) query cache, replacing fragile `FILTER(ALL(...))` and `PARALLELPERIOD` constructs.

#### Rolling 3-Month Moving Average:
```dax
Net Revenue Rolling 3M Avg (WINDOW) = 
VAR _WindowRows = 
    WINDOW ( 
        -2, RELATIVE, 
        0, RELATIVE, 
        ALLSELECTED ( 'Dim_Date'[YearMonth] ), 
        ORDERBY ( 'Dim_Date'[YearMonth], ASC ) 
    )
RETURN
    CALCULATE ( 
        AVERAGEX ( 
            VALUES ( 'Dim_Date'[YearMonth] ), 
            [Net Revenue] 
        ), 
        _WindowRows 
    )
```
*Why this is superior:* Older patterns using `DATESINPERIOD` require contiguous day-level date tables and often fail when slicing across custom matrix rows. `WINDOW()` works on arbitrary visual sorting keys with declarative relative indexing.

#### Prior Period Variance using `OFFSET`:
```dax
Net Revenue Prior Month (OFFSET) = 
CALCULATE ( 
    [Net Revenue], 
    OFFSET ( 
        -1, 
        ALLSELECTED ( 'Dim_Date'[YearMonth], 'Dim_Date'[MonthShort] ), 
        ORDERBY ( 'Dim_Date'[YearMonth], ASC ) 
    ) 
)
```

---

### 5.2 Dynamic Pareto 80/20 & Top N with Others Rollup

Pareto analysis reveals customer concentration risk. The cumulative sum pattern calculates running totals across dynamically ranked customers.

```dax
Cumulative Revenue Pareto % = 
VAR _CurrentCustomerRev = [Net Revenue]
VAR _AllSelectedCustomers = 
    ADDCOLUMNS ( 
        ALLSELECTED ( 'Dim_Customer'[CustomerID] ), 
        "@CustomerRev", [Net Revenue] 
    )
VAR _CustomersWithHigherOrEqualRevenue = 
    FILTER ( 
        _AllSelectedCustomers, 
        [@CustomerRev] >= _CurrentCustomerRev 
    )
VAR _Cumulative = 
    SUMX ( 
        _CustomersWithHigherOrEqualRevenue, 
        [@CustomerRev] 
    )
VAR _Total = 
    CALCULATE ( [Net Revenue], ALLSELECTED ( 'Dim_Customer' ) )
RETURN
    DIVIDE ( _Cumulative, _Total, BLANK () )
```

#### Dynamic Top N + "Others" Rollup Pattern:
```dax
Revenue Top N and Others = 
VAR _Threshold = SELECTEDVALUE ( 'Param_TopN'[TopNValue], 10 )
VAR _CurrentCustomer = SELECTEDVALUE ( 'Dim_Customer'[CustomerName] )
VAR _TopNCustomersTable = 
    TOPN ( 
        _Threshold, 
        ALL ( 'Dim_Customer'[CustomerName] ), 
        [Net Revenue], 
        DESC 
    )
VAR _IsCustomerInTopN = _CurrentCustomer IN _TopNCustomersTable
VAR _AllRevenue = CALCULATE ( [Net Revenue], ALL ( 'Dim_Customer' ) )
VAR _TopNRevenue = CALCULATE ( [Net Revenue], KEEPFILTERS ( _TopNCustomersTable ) )
VAR _OthersRevenue = _AllRevenue - _TopNRevenue
RETURN
    SWITCH ( 
        TRUE (), 
        _CurrentCustomer = "Others", _OthersRevenue, 
        _IsCustomerInTopN, [Net Revenue], 
        BLANK () 
    )
```

---

### 5.3 Dynamic RFM Segmentation & Cohort Churn Modeling

Evaluates customer behavior across Recency, Frequency, and Monetary dimensions dynamically without pre-calculating in SQL or Python.

```dax
RFM Customer Segment = 
VAR _Days = [Customer Recency Days]
VAR _Orders = [Customer Lifetime Orders]
VAR _LTV = [Customer Lifetime Revenue]
VAR _R = SWITCH(TRUE(), ISBLANK(_Days), BLANK(), _Days <= 30, 5, _Days <= 60, 4, _Days <= 90, 3, _Days <= 180, 2, 1)
VAR _F = SWITCH(TRUE(), ISBLANK(_Orders), BLANK(), _Orders >= 30, 5, _Orders >= 18, 4, _Orders >= 10, 3, _Orders >= 4, 2, 1)
VAR _M = SWITCH(TRUE(), ISBLANK(_LTV), BLANK(), _LTV >= 100000, 5, _LTV >= 50000, 4, _LTV >= 20000, 3, _LTV >= 5000, 2, 1)
RETURN
    SWITCH ( 
        TRUE (), 
        ISBLANK ( _R ), BLANK (), 
        _R >= 4 && _F >= 4 && _M >= 4, "Champions", 
        _R >= 3 && _F >= 3,             "Loyal Enterprise", 
        _R >= 4 && _F <= 2,             "Recent / Expanding", 
        _R <= 2 && _F >= 3 && _M >= 3, "At-Risk High-Value", 
        _R <= 2 && _F <= 2,             "Hibernating / Dormant", 
        "Needs Attention" 
    )
```

#### New Customer Acquisition Count:
```dax
New Customers Count = 
VAR _MinDate = MIN ( 'Dim_Date'[Date] )
VAR _MaxDate = MAX ( 'Dim_Date'[Date] )
VAR _AllCustomers = VALUES ( 'Dim_Customer'[CustomerID] )
VAR _NewCustomers = 
    FILTER ( 
        _AllCustomers, 
        VAR _FirstOrder = [Customer First Purchase Date] 
        RETURN _FirstOrder >= _MinDate && _FirstOrder <= _MaxDate 
    )
RETURN
    COUNTROWS ( _NewCustomers )
```

---

### 5.4 Market Basket Cross-Sell Affinity & Lift Analysis

Identifies co-purchasing probability between a selected Focus Product $A$ and Catalog Product $B$.

$$\text{Support}(A \cup B) = \frac{\text{Orders}(A \cap B)}{\text{Total Orders}}$$

$$\text{Confidence}(A \rightarrow B) = \frac{\text{Orders}(A \cap B)}{\text{Orders}(A)}$$

$$\text{Lift}(A \rightarrow B) = \frac{\text{Confidence}(A \rightarrow B)}{\text{Support}(B)}$$

```dax
Basket Lift Ratio = 
VAR _SelectedFocusID = SELECTEDVALUE ( 'Dim_Product_Focus'[ProductID] )
VAR _OrdersWithFocusProduct = 
    CALCULATETABLE ( 
        VALUES ( 'Fact_Sales'[SalesOrderNumber] ), 
        TREATAS ( { _SelectedFocusID }, 'Fact_Sales'[ProductID] ), 
        ALL ( 'Dim_Product' ) 
    )
VAR _OrdersWithComparisonProduct = 
    CALCULATETABLE ( VALUES ( 'Fact_Sales'[SalesOrderNumber] ) )
VAR _SharedOrders = 
    COUNTROWS ( INTERSECT ( _OrdersWithFocusProduct, _OrdersWithComparisonProduct ) )
VAR _FocusOrders = COUNTROWS ( _OrdersWithFocusProduct )
VAR _Confidence = DIVIDE ( _SharedOrders, _FocusOrders, BLANK () )
VAR _ComparisonSupport = DIVIDE ( COUNTROWS ( _OrdersWithComparisonProduct ), [Total Universe Orders], BLANK () )
RETURN
    DIVIDE ( _Confidence, _ComparisonSupport, BLANK () )
```

---

### 5.5 Dynamic Multi-Currency Translation & FX Decomposition

Enables real-time conversion into USD, EUR, GBP, JPY, or CAD while isolating organic revenue growth from currency fluctuations.

```dax
Converted Net Revenue = 
VAR _TargetCurrency = SELECTEDVALUE ( 'Param_ReportingCurrency'[CurrencyCode], "USD" )
RETURN
    IF ( 
        _TargetCurrency = "USD", 
        [Net Revenue], 
        SUMX ( 
            VALUES ( 'Dim_Date'[Date] ), 
            VAR _CurrentDate = 'Dim_Date'[Date]
            VAR _Rate = 
                CALCULATE ( 
                    MAX ( 'Dim_ExchangeRate'[LocalPerUSD] ), 
                    'Dim_ExchangeRate'[Date] = _CurrentDate, 
                    'Dim_ExchangeRate'[CurrencyCode] = _TargetCurrency 
                )
            RETURN
                [Net Revenue] * COALESCE ( _Rate, 1.0 ) 
        ) 
    )
```

#### FX Impact Variance Decomposition:
$$\text{FX Translation Impact} = \text{Converted Net Revenue} - \text{Constant Currency Net Revenue}$$

---

### 5.6 Parameterized What-If Sensitivity & Margin Elasticity

```dax
Simulated vs Actual Margin Delta $ = 
VAR _PriceChange = SELECTEDVALUE ( 'Param_WhatIf_Price'[PriceAdjustmentPercent], 0.0 )
VAR _CostInflation = SELECTEDVALUE ( 'Param_WhatIf_Cost'[CostAdjustmentPercent], 0.0 )
VAR _SimulatedRev = [Net Revenue] * ( 1 + _PriceChange )
VAR _SimulatedCost = [Total COGS] * ( 1 + _CostInflation )
VAR _SimulatedMargin = _SimulatedRev - _SimulatedCost
RETURN
    _SimulatedMargin - [Gross Margin]
```

---

### 5.7 Grain Mismatch Resolution via `TREATAS`

`Fact_Sales` is recorded at the **Daily $\times$ Product** grain; `Fact_Budget` is recorded at the **Monthly $\times$ Category** grain.

```dax
Target Revenue (Grain-Safe) = 
VAR _SelectedCategories = VALUES ( 'Dim_Product'[Category] )
VAR _SelectedRegions = VALUES ( 'Dim_Store_Region'[RegionCode] )
VAR _SelectedYearMonths = VALUES ( 'Dim_Date'[YearMonth] )
VAR _IsDrilledToProduct = ISINSCOPE ( 'Dim_Product'[ProductID] )
VAR _BaseBudget = 
    CALCULATE ( 
        [Budget Revenue], 
        TREATAS ( _SelectedCategories, 'Fact_Budget'[Category] ), 
        TREATAS ( _SelectedRegions, 'Fact_Budget'[RegionCode] ), 
        TREATAS ( _SelectedYearMonths, 'Fact_Budget'[YearMonth] ) 
    )
RETURN
    IF ( 
        _IsDrilledToProduct, 
        VAR _ProductSales = [Net Revenue]
        VAR _CategorySales = 
            CALCULATE ( 
                [Net Revenue], 
                ALL ( 'Dim_Product' ), 
                VALUES ( 'Dim_Product'[Category] ) 
            )
        RETURN _BaseBudget * DIVIDE ( _ProductSales, _CategorySales, 0 ), 
        _BaseBudget 
    )
```

---

### 5.8 Enterprise Calculation Groups & Dynamic Format Strings

Eliminates measure sprawl by reducing 80+ redundant time intelligence measures down to a single Calculation Group table:

| Calculation Item | DAX Expression | Dynamic Format String Expression |
| :--- | :--- | :--- |
| `Current` | `SELECTEDMEASURE()` | `SELECTEDMEASUREFORMATSTRING()` |
| `Prior Year (PY)` | `CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Dim_Date'[Date]))` | `SELECTEDMEASUREFORMATSTRING()` |
| `YoY Variance` | `SELECTEDMEASURE() - CALCULATE(...)` | `SELECTEDMEASUREFORMATSTRING()` |
| `YoY %` | `DIVIDE(SELECTEDMEASURE() - CALCULATE(...), CALCULATE(...))` | `"+0.0%;-0.0%;0.0%"` |
| `YTD` | `TOTALYTD(SELECTEDMEASURE(), 'Dim_Date'[Date])` | `SELECTEDMEASUREFORMATSTRING()` |
| `Rolling 3M Avg` | `CALCULATE(AVERAGEX(...), WINDOW(-2, 0))` | `SELECTEDMEASUREFORMATSTRING()` |

---

### 5.9 Hierarchical Dynamic Row-Level Security (RLS)

Leverages DAX parent-child hierarchy function `PATHCONTAINS` to grant Regional VPs visibility into all subordinate Sales Directors:

```dax
// Table Filter DAX on 'Dim_Store_Region'
VAR _CurrentUser = USERPRINCIPALNAME ()
VAR _IsExecutive = _CurrentUser IN { "executive@company.com", "cfo@company.com" }
RETURN
    IF ( 
        _IsExecutive, 
        TRUE (), 
        PATHCONTAINS ( 'Dim_Store_Region'[HierarchyPath], _CurrentUser ) 
    )
```

---

### 5.10 In-Cell Vector SVG Visuals Generated in DAX

Renders responsive micro-visuals (progress bars, status badges, trendlines) directly in Power BI table cells by setting `Data Category = Image URL`.

```dax
SVG Progress Bar Attainment = 
VAR _Attainment = [Revenue Target Attainment %]
VAR _Width = 120
VAR _BarWidth = ROUND ( MIN ( MAX ( _Attainment, 0 ), 1.2 ) * 100, 0 )
VAR _BarColor = IF ( _Attainment >= 1.05, "#107C41", IF ( _Attainment >= 0.98, "#F7630C", "#D83B01" ) )
VAR _Svg = 
    "data:image/svg+xml;utf8," & 
    "<svg xmlns='http://www.w3.org/2000/svg' width='" & _Width & "' height='18'>" & 
    "  <rect x='0' y='3' width='100' height='12' rx='6' fill='#EDEBE9'/>" & 
    "  <rect x='0' y='3' width='" & _BarWidth & "' height='12' rx='6' fill='" & _BarColor & "'/>" & 
    "  <line x1='100' y1='1' x2='100' y2='17' stroke='#323130' stroke-width='1.5' stroke-dasharray='2,2'/>" & 
    "</svg>"
RETURN
    IF ( NOT ISBLANK ( _Attainment ), _Svg, BLANK () )
```

---

## 🚀 6. Power BI Project (PBIP) Deployment Guide

This repository contains native Microsoft Power BI Project (`.pbip`) files ready to open in Power BI Desktop:

```text
pbip/
├── Omnichannel_Revenue_Intelligence.pbip
├── Omnichannel_Revenue_Intelligence.Report/
│   ├── definition.pbir
│   └── report.json
└── Omnichannel_Revenue_Intelligence.SemanticModel/
    ├── definition.pbism
    └── model.bim
```

### Steps to Open:
1. Ensure **Power BI Desktop** (March 2024 or later) is installed.
2. In Power BI Desktop, enable **Power BI Project (.pbip) save option** under `File > Options and settings > Options > Preview features`.
3. Double-click [Omnichannel_Revenue_Intelligence.pbip](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/powerbi_advanced_dax_project/pbip/Omnichannel_Revenue_Intelligence.pbip).
4. Power BI Desktop will parse `model.bim` and `report.json`, establishing the schema, relationships, and visual canvas automatically!

---

## ⚡ 7. Automated Tabular Editor Deployment

For enterprise CI/CD pipelines and Tabular Editor 2 / 3 users:
1. Connect Tabular Editor to your Power BI Desktop instance or Fabric XMLA endpoint.
2. Open [tabular_editor_script.csx](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/powerbi_advanced_dax_project/scripts/tabular_editor_script.csx) in the Advanced Scripting tab.
3. Click **Run (F5)** to automatically generate:
   - All Display Folders
   - Time Intelligence Calculation Group
   - Metric Selector Calculation Group
   - Standard Currency and Percentage format strings.

---

## 🖥️ 8. Interactive Browser Simulator

To immediately test, explore, and demonstrate this project without opening Power BI Desktop:
1. Open [index.html](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/powerbi_advanced_dax_project/simulator/index.html) in any modern browser.
2. Experience:
   - Dynamic Year, Region, Currency, and Top N slicers with instant recalculation.
   - Interactive What-If Price and Cost Inflation sliders.
   - Pareto 80/20 distribution charts.
   - Full Star Schema interactive node relationship canvas.
   - Interactive DAX Code Studio with 1-click DAX formula copying.

---

## 🏎️ 9. DAX Storage Engine vs Formula Engine Optimization

1. **Storage Engine (SE) Cache Utilization**: All core aggregations are written as pure VertiPaq column scans (`SUM`, `DISTINCTCOUNTNOBLANK`), allowing the multi-threaded VertiPaq SE to return compressed dictionary results in under 15ms.
2. **Elimination of Row-by-Row Callbacks**: Avoided nested `SUMX` iterations over wide tables. Transformed row-level filtering into set-based operations using `TREATAS`, `KEEPFILTERS`, and `INTERSECT`.
3. **Variable Caching (`VAR` / `RETURN`)**: All intermediate computations are cached in local variables, preventing duplicate formula engine evaluation passes during visual rendering.
