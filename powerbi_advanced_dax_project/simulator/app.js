// ===============================================================================
// Power BI Advanced DAX Project Simulator - Application Logic
// Features: Dynamic DAX Calculation Engine, Interactive Charts, What-If Modeling
// ===============================================================================

// Baseline Monthly Enterprise Data (USD Canonical)
const MONTHLY_DATA = [
  // 2023
  { year: 2023, month: 'Jan', ym: 202301, rev: 1240000, cogs: 670000, orders: 680, na: 620000, emea: 430000, apac: 190000 },
  { year: 2023, month: 'Feb', ym: 202302, rev: 1280000, cogs: 690000, orders: 700, na: 640000, emea: 440000, apac: 200000 },
  { year: 2023, month: 'Mar', ym: 202303, rev: 1450000, cogs: 770000, orders: 790, na: 730000, emea: 500000, apac: 220000 },
  { year: 2023, month: 'Apr', ym: 202304, rev: 1390000, cogs: 740000, orders: 750, na: 690000, emea: 480000, apac: 220000 },
  { year: 2023, month: 'May', ym: 202305, rev: 1420000, cogs: 760000, orders: 770, na: 710000, emea: 490000, apac: 220000 },
  { year: 2023, month: 'Jun', ym: 202306, rev: 1560000, cogs: 820000, orders: 840, na: 780000, emea: 540000, apac: 240000 },
  { year: 2023, month: 'Jul', ym: 202307, rev: 1490000, cogs: 790000, orders: 810, na: 750000, emea: 510000, apac: 230000 },
  { year: 2023, month: 'Aug', ym: 202308, rev: 1520000, cogs: 810000, orders: 820, na: 760000, emea: 530000, apac: 230000 },
  { year: 2023, month: 'Sep', ym: 202309, rev: 1610000, cogs: 850000, orders: 870, na: 810000, emea: 550000, apac: 250000 },
  { year: 2023, month: 'Oct', ym: 202310, rev: 1680000, cogs: 890000, orders: 900, na: 840000, emea: 580000, apac: 260000 },
  { year: 2023, month: 'Nov', ym: 202311, rev: 1850000, cogs: 980000, orders: 990, na: 930000, emea: 630000, apac: 290000 },
  { year: 2023, month: 'Dec', ym: 202312, rev: 1960000, cogs: 1030000, orders: 1050, na: 990000, emea: 670000, apac: 300000 },
  // 2024
  { year: 2024, month: 'Jan', ym: 202401, rev: 1520000, cogs: 800000, orders: 810, na: 760000, emea: 520000, apac: 240000 },
  { year: 2024, month: 'Feb', ym: 202402, rev: 1580000, cogs: 830000, orders: 840, na: 790000, emea: 540000, apac: 250000 },
  { year: 2024, month: 'Mar', ym: 202403, rev: 1780000, cogs: 930000, orders: 950, na: 890000, emea: 610000, apac: 280000 },
  { year: 2024, month: 'Apr', ym: 202404, rev: 1710000, cogs: 900000, orders: 910, na: 860000, emea: 580000, apac: 270000 },
  { year: 2024, month: 'May', ym: 202405, rev: 1750000, cogs: 920000, orders: 930, na: 880000, emea: 600000, apac: 270000 },
  { year: 2024, month: 'Jun', ym: 202406, rev: 1920000, cogs: 1000000, orders: 1010, na: 960000, emea: 660000, apac: 300000 },
  { year: 2024, month: 'Jul', ym: 202407, rev: 1840000, cogs: 960000, orders: 980, na: 920000, emea: 630000, apac: 290000 },
  { year: 2024, month: 'Aug', ym: 202408, rev: 1880000, cogs: 980000, orders: 1000, na: 940000, emea: 640000, apac: 300000 },
  { year: 2024, month: 'Sep', ym: 202409, rev: 1990000, cogs: 1040000, orders: 1060, na: 1000000, emea: 680000, apac: 310000 },
  { year: 2024, month: 'Oct', ym: 202410, rev: 2080000, cogs: 1080000, orders: 1100, na: 1040000, emea: 710000, apac: 330000 },
  { year: 2024, month: 'Nov', ym: 202411, rev: 2280000, cogs: 1180000, orders: 1200, na: 1140000, emea: 780000, apac: 360000 },
  { year: 2024, month: 'Dec', ym: 202412, rev: 2410000, cogs: 1240000, orders: 1260, na: 1210000, emea: 820000, apac: 380000 },
  // 2025
  { year: 2025, month: 'Jan', ym: 202501, rev: 1880000, cogs: 970000, orders: 990, na: 940000, emea: 640000, apac: 300000 },
  { year: 2025, month: 'Feb', ym: 202502, rev: 1940000, cogs: 1000000, orders: 1020, na: 970000, emea: 660000, apac: 310000 },
  { year: 2025, month: 'Mar', ym: 202503, rev: 2180000, cogs: 1120000, orders: 1140, na: 1090000, emea: 740000, apac: 350000 },
  { year: 2025, month: 'Apr', ym: 202504, rev: 2100000, cogs: 1080000, orders: 1100, na: 1050000, emea: 710000, apac: 340000 },
  { year: 2025, month: 'May', ym: 202505, rev: 2150000, cogs: 1110000, orders: 1130, na: 1080000, emea: 730000, apac: 340000 },
  { year: 2025, month: 'Jun', ym: 202506, rev: 2360000, cogs: 1210000, orders: 1230, na: 1180000, emea: 800000, apac: 380000 },
  { year: 2025, month: 'Jul', ym: 202507, rev: 2260000, cogs: 1160000, orders: 1180, na: 1130000, emea: 770000, apac: 360000 },
  { year: 2025, month: 'Aug', ym: 202508, rev: 2310000, cogs: 1180000, orders: 1200, na: 1160000, emea: 790000, apac: 360000 },
  { year: 2025, month: 'Sep', ym: 202509, rev: 2450000, cogs: 1250000, orders: 1270, na: 1230000, emea: 830000, apac: 390000 },
  { year: 2025, month: 'Oct', ym: 202510, rev: 2560000, cogs: 1300000, orders: 1330, na: 1280000, emea: 870000, apac: 410000 },
  { year: 2025, month: 'Nov', ym: 202511, rev: 2790000, cogs: 1420000, orders: 1440, na: 1400000, emea: 950000, apac: 440000 },
  { year: 2025, month: 'Dec', ym: 202512, rev: 2950000, cogs: 1500000, orders: 1520, na: 1480000, emea: 1000000, apac: 470000 },
];

// FX Conversion Rates
const FX_RATES = {
  USD: { rate: 1.0, symbol: '$' },
  EUR: { rate: 0.92, symbol: '€' },
  GBP: { rate: 0.79, symbol: '£' },
  JPY: { rate: 152.0, symbol: '¥' },
  CAD: { rate: 1.36, symbol: 'C$' }
};

// Top 20 Customer Accounts (for Pareto)
const TOP_CUSTOMERS = [
  { name: 'Apex Global Solutions', rev: 2150000, segment: 'Enterprise', region: 'NA' },
  { name: 'Quantum Logistics GmbH', rev: 1980000, segment: 'Enterprise', region: 'EMEA' },
  { name: 'Nexus Healthcare Corp', rev: 1840000, segment: 'Enterprise', region: 'NA' },
  { name: 'Kobe Robotics KK', rev: 1720000, segment: 'Enterprise', region: 'APAC' },
  { name: 'Vortex Retail UK', rev: 1490000, segment: 'Mid-Market', region: 'EMEA' },
  { name: 'Silicon Valley Auto', rev: 1380000, segment: 'Enterprise', region: 'NA' },
  { name: 'Munich Precision Tech', rev: 1290000, segment: 'Enterprise', region: 'EMEA' },
  { name: 'Atlas Heavy Ind. Inc', rev: 1190000, segment: 'Enterprise', region: 'NA' },
  { name: 'BlueWave Cloud SA', rev: 1050000, segment: 'Mid-Market', region: 'EMEA' },
  { name: 'Sydney FinTech Ltd', rev: 980000, segment: 'Mid-Market', region: 'APAC' },
  { name: 'Nordic Renewable Oy', rev: 890000, segment: 'Enterprise', region: 'EMEA' },
  { name: 'Titan CyberSec Ltd', rev: 840000, segment: 'Mid-Market', region: 'EMEA' },
  { name: 'Lyon BioPharma SAS', rev: 790000, segment: 'Enterprise', region: 'EMEA' },
  { name: 'Tokyo Sensor Systems', rev: 740000, segment: 'Mid-Market', region: 'APAC' },
  { name: 'Toronto Digital Corp', rev: 680000, segment: 'SMB', region: 'NA' },
  { name: 'Pacific Cargo Pty', rev: 610000, segment: 'Mid-Market', region: 'APAC' },
  { name: 'Berlin Dynamics GmbH', rev: 550000, segment: 'Mid-Market', region: 'EMEA' },
  { name: 'Maple Leaf Media', rev: 490000, segment: 'SMB', region: 'NA' },
  { name: 'Sakura AI Labs', rev: 440000, segment: 'SMB', region: 'APAC' },
  { name: 'Manchester Textiles', rev: 380000, segment: 'SMB', region: 'EMEA' }
];

// Market Basket Affinity Dataset
const BASKET_AFFINITY_DATA = [
  { focus: 'Enterprise Cloud Suite ERP', comp: 'OneLake Dedicated Compute', support: 0.184, conf: 0.642, lift: 2.85, status: 'Strong Cross-Sell Bundle 🔥' },
  { focus: 'Enterprise Cloud Suite ERP', comp: 'Fabric Direct Lake Migration Pack', support: 0.142, conf: 0.495, lift: 3.12, status: 'Strong Cross-Sell Bundle 🔥' },
  { focus: 'Enterprise Cloud Suite ERP', comp: 'Identity Access Manager Pro', support: 0.165, conf: 0.575, lift: 2.21, status: 'Moderate Association 🟢' },
  { focus: 'Advanced Analytics AI Engine', comp: 'Vector DB Semantic Search Pod', support: 0.198, conf: 0.684, lift: 3.45, status: 'Strong Cross-Sell Bundle 🔥' },
  { focus: 'Advanced Analytics AI Engine', comp: 'Custom ML Model Training Sprint', support: 0.125, conf: 0.432, lift: 2.90, status: 'Strong Cross-Sell Bundle 🔥' },
  { focus: 'CyberShield Threat Sentinel', comp: 'Secure Cryptographic HSM Module', support: 0.110, conf: 0.410, lift: 2.75, status: 'Strong Cross-Sell Bundle 🔥' },
  { focus: 'Smart Edge IoT Gateway Hub', comp: 'Real-Time Event Stream Kafka', support: 0.155, conf: 0.540, lift: 2.60, status: 'Strong Cross-Sell Bundle 🔥' },
];

// DAX Library Catalog
const DAX_LIBRARY = {
  'window_offset': {
    title: 'Net Revenue Prior Month (OFFSET)',
    category: 'Time Intelligence & Window Functions',
    expression: `Net Revenue Prior Month (OFFSET) = 
CALCULATE ( 
    [Net Revenue], 
    OFFSET ( 
        -1, 
        ALLSELECTED ( 'Dim_Date'[YearMonth], 'Dim_Date'[MonthShort] ), 
        ORDERBY ( 'Dim_Date'[YearMonth], ASC ) 
    ) 
)`,
    logic: 'Evaluates the exact preceding period on any arbitrary visual axis without requiring contiguous day-level date keys.',
    engine: 'Storage Engine (SE) Cache. Avoids FILTER(ALL()) table scans, reducing memory bandwidth by up to 85% compared to PARALLELPERIOD.'
  },
  'window_rolling3m': {
    title: 'Net Revenue Rolling 3M Avg (WINDOW)',
    category: 'Time Intelligence & Window Functions',
    expression: `Net Revenue Rolling 3M Avg (WINDOW) = 
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
    )`,
    logic: 'Constructs a relative moving window frame from -2 relative (2 periods prior) to 0 relative (current period).',
    engine: 'Direct VertiPaq window evaluation. Does not instantiate materialized Cartesian tables in the Formula Engine.'
  },
  'pareto_cumulative': {
    title: 'Cumulative Revenue Pareto %',
    category: 'Pareto 80/20 & Concentration',
    expression: `Cumulative Revenue Pareto % = 
VAR _CurrentCustomerRev = [Net Revenue]
VAR _AllSelectedCustomers = 
    ADDCOLUMNS ( 
        ALLSELECTED ( 'Dim_Customer'[CustomerID] ), 
        "@CustomerRev", [Net Revenue] 
    )
VAR _CustomersHigherOrEqual = 
    FILTER ( 
        _AllSelectedCustomers, 
        [@CustomerRev] >= _CurrentCustomerRev 
    )
VAR _CumulativeRev = 
    SUMX ( _CustomersHigherOrEqual, [@CustomerRev] )
VAR _TotalRev = 
    CALCULATE ( [Net Revenue], ALLSELECTED ( 'Dim_Customer' ) )
RETURN
    DIVIDE ( _CumulativeRev, _TotalRev, BLANK () )`,
    logic: 'Calculates the cumulative percentage curve across ranked customer accounts dynamically in any filter context.',
    engine: 'Optimized with localized variable caching to prevent recalculating denominator within the iteration loop.'
  },
  'rfm_segment': {
    title: 'Dynamic RFM Customer Segment',
    category: 'Customer Intelligence & Churn',
    expression: `RFM Customer Segment = 
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
    )`,
    logic: 'Classifies every account into marketing & retention segments on-the-fly based on recency, frequency, and monetary quintiles.',
    engine: 'VertiPaq column aggregation with ALLEXCEPT to break visual date context and capture true customer lifetime activity.'
  },
  'basket_lift': {
    title: 'Basket Lift Ratio',
    category: 'Market Basket Affinity',
    expression: `Basket Lift Ratio = 
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
    DIVIDE ( _Confidence, _ComparisonSupport, BLANK () )`,
    logic: 'Evaluates association rule lift between focus product and all cross-sell catalog items. Lift > 1.0 indicates true statistical bundle affinity.',
    engine: 'Uses TREATAS and INTERSECT bitmap set operations executed natively within the VertiPaq Storage Engine.'
  },
  'dynamic_currency': {
    title: 'Converted Net Revenue',
    category: 'Multi-Currency Modeling',
    expression: `Converted Net Revenue = 
VAR _TargetCurrency = SELECTEDVALUE ( 'Param_ReportingCurrency'[CurrencyCode], "USD" )
RETURN
    IF ( 
        _TargetCurrency = "USD", 
        [Net Revenue], 
        SUMX ( 
            VALUES ( 'Dim_Date'[Date] ), 
            VAR _CurrentDate = 'Dim_Date'[Date]
            VAR _ExchangeRate = 
                CALCULATE ( 
                    MAX ( 'Dim_ExchangeRate'[LocalPerUSD] ), 
                    'Dim_ExchangeRate'[Date] = _CurrentDate, 
                    'Dim_ExchangeRate'[CurrencyCode] = _TargetCurrency 
                )
            RETURN
                [Net Revenue] * COALESCE ( _ExchangeRate, 1.0 ) 
        ) 
    )`,
    logic: 'Dynamically translates canonical USD transaction line items into selected reporting currency (USD, EUR, GBP, JPY, CAD) using daily rates.',
    engine: 'Branching IF optimization: Default USD bypasses SUMX loop entirely, executing sub-second VertiPaq column sums.'
  },
  'whatif_margin': {
    title: 'Simulated Gross Margin Delta $',
    category: 'What-If Sensitivity Modeling',
    expression: `Simulated vs Actual Margin Delta $ = 
VAR _PriceChange = SELECTEDVALUE ( 'Param_WhatIf_Price'[PriceAdjustmentPercent], 0.0 )
VAR _CostInflation = SELECTEDVALUE ( 'Param_WhatIf_Cost'[CostAdjustmentPercent], 0.0 )
VAR _SimulatedRev = [Net Revenue] * ( 1 + _PriceChange )
VAR _SimulatedCost = [Total COGS] * ( 1 + _CostInflation )
VAR _SimulatedMargin = _SimulatedRev - _SimulatedCost
RETURN
    _SimulatedMargin - [Gross Margin]`,
    logic: 'Calculates the net bottom-line financial impact of simultaneous price increases/discounts and supplier cost inflation.',
    engine: 'Lightweight scalar expression evaluated in Formula Engine in microseconds.'
  },
  'treatas_budget': {
    title: 'Target Revenue (Grain-Safe with TREATAS)',
    category: 'Budget & Granularity Alignment',
    expression: `Target Revenue (Grain-Safe) = 
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
        VAR _CategorySales = CALCULATE ( [Net Revenue], ALL ( 'Dim_Product' ), VALUES ( 'Dim_Product'[Category] ) )
        RETURN _BaseBudget * DIVIDE ( _ProductSales, _CategorySales, 0 ), 
        _BaseBudget 
    )`,
    logic: 'Bridges mismatched granularity between monthly category budgets and daily product transactions, allocating proportionately when drilled.',
    engine: 'TREATAS applies virtual lineage without physical relationship overhead, avoiding bi-directional ambiguity.'
  }
};

// Application State
let state = {
  activePage: 'executive',
  selectedYear: 'all',
  selectedRegion: 'all',
  selectedCurrency: 'USD',
  priceAdjustment: 0.0,
  costAdjustment: 0.0,
  topN: 10,
  selectedFocusProduct: 'Enterprise Cloud Suite ERP'
};

// Global Chart Instances
let trendChart = null;
let paretoChart = null;
let sensitivityChart = null;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  setupSlicers();
  setupDaxStudio();
  setupWhatIfSliders();
  renderCurrentPage();
});

// Setup Page Navigation
function setupNavigation() {
  document.querySelectorAll('.nav-page-item').forEach(item => {
    item.addEventListener('click', (e) => {
      document.querySelectorAll('.nav-page-item').forEach(n => n.classList.remove('active'));
      item.classList.add('active');
      const pageId = item.dataset.page;
      state.activePage = pageId;
      document.querySelectorAll('.report-page-view').forEach(p => p.classList.remove('active'));
      const activeEl = document.getElementById(`page-${pageId}`);
      if (activeEl) activeEl.classList.add('active');
      renderCurrentPage();
    });
  });
}

// Setup Slicers
function setupSlicers() {
  const yearSelect = document.getElementById('slicer-year');
  if (yearSelect) {
    yearSelect.addEventListener('change', (e) => {
      state.selectedYear = e.target.value;
      recalculateAndRender();
    });
  }

  const regionSelect = document.getElementById('slicer-region');
  if (regionSelect) {
    regionSelect.addEventListener('change', (e) => {
      state.selectedRegion = e.target.value;
      recalculateAndRender();
    });
  }

  const currSelect = document.getElementById('slicer-currency');
  if (currSelect) {
    currSelect.addEventListener('change', (e) => {
      state.selectedCurrency = e.target.value;
      recalculateAndRender();
    });
  }

  const topnSelect = document.getElementById('slicer-topn');
  if (topnSelect) {
    topnSelect.addEventListener('change', (e) => {
      state.topN = parseInt(e.target.value, 10);
      recalculateAndRender();
    });
  }
}

// Setup What-If Sliders
function setupWhatIfSliders() {
  const priceSlider = document.getElementById('slider-price');
  const priceVal = document.getElementById('val-price');
  if (priceSlider && priceVal) {
    priceSlider.addEventListener('input', (e) => {
      state.priceAdjustment = parseFloat(e.target.value) / 100.0;
      priceVal.textContent = (state.priceAdjustment >= 0 ? '+' : '') + Math.round(state.priceAdjustment * 100) + '%';
      recalculateWhatIf();
    });
  }

  const costSlider = document.getElementById('slider-cost');
  const costVal = document.getElementById('val-cost');
  if (costSlider && costVal) {
    costSlider.addEventListener('input', (e) => {
      state.costAdjustment = parseFloat(e.target.value) / 100.0;
      costVal.textContent = (state.costAdjustment >= 0 ? '+' : '') + Math.round(state.costAdjustment * 100) + '%';
      recalculateWhatIf();
    });
  }
}

// Format Currency
function fmtCurr(val, code = state.selectedCurrency) {
  const fx = FX_RATES[code] || FX_RATES.USD;
  const converted = val * fx.rate;
  if (Math.abs(converted) >= 1e6) {
    return fx.symbol + (converted / 1e6).toFixed(2) + 'M';
  } else if (Math.abs(converted) >= 1e3) {
    return fx.symbol + (converted / 1e3).toFixed(1) + 'K';
  }
  return fx.symbol + Math.round(converted).toLocaleString();
}

function fmtPct(val) {
  return (val * 100).toFixed(1) + '%';
}

// Calculate Filtered Metrics
function getCalculatedMetrics() {
  let rows = MONTHLY_DATA;
  if (state.selectedYear !== 'all') {
    rows = rows.filter(r => r.year === parseInt(state.selectedYear, 10));
  }

  let totalRev = 0;
  let totalCogs = 0;
  let totalOrders = 0;

  rows.forEach(r => {
    let revShare = r.rev;
    if (state.selectedRegion === 'NA') revShare = r.na;
    else if (state.selectedRegion === 'EMEA') revShare = r.emea;
    else if (state.selectedRegion === 'APAC') revShare = r.apac;

    totalRev += revShare;
    // proportional cogs & orders
    const factor = revShare / r.rev;
    totalCogs += r.cogs * factor;
    totalOrders += Math.round(r.orders * factor);
  });

  const grossMargin = totalRev - totalCogs;
  const marginPct = totalRev > 0 ? (grossMargin / totalRev) : 0;
  const aov = totalOrders > 0 ? (totalRev / totalOrders) : 0;

  // Prior Year baseline
  let pyRev = 0;
  if (state.selectedYear === '2024') {
    pyRev = 18450000;
  } else if (state.selectedYear === '2025') {
    pyRev = 22170000;
  } else if (state.selectedYear === '2023') {
    pyRev = 15800000;
  } else {
    pyRev = 40620000; // All years prior comparative baseline
  }
  const yoyPct = pyRev > 0 ? ((totalRev - pyRev) / pyRev) : 0.185;

  return {
    netRevenue: totalRev,
    grossMargin: grossMargin,
    marginPct: marginPct,
    totalOrders: totalOrders,
    aov: aov,
    yoyPct: yoyPct,
    activeAccounts: 250
  };
}

// Recalculate & Render Page
function recalculateAndRender() {
  const m = getCalculatedMetrics();
  
  // Update Header KPI Cards
  const elNetRev = document.getElementById('kpi-net-rev');
  if (elNetRev) elNetRev.textContent = fmtCurr(m.netRevenue);

  const elMargin = document.getElementById('kpi-gross-margin');
  if (elMargin) elMargin.textContent = fmtCurr(m.grossMargin);

  const elMarginPct = document.getElementById('kpi-margin-pct');
  if (elMarginPct) elMarginPct.textContent = fmtPct(m.marginPct);

  const elYoY = document.getElementById('kpi-yoy-pct');
  if (elYoY) elYoY.textContent = (m.yoyPct >= 0 ? '+' : '') + fmtPct(m.yoyPct);

  const elOrders = document.getElementById('kpi-orders');
  if (elOrders) elOrders.textContent = m.totalOrders.toLocaleString();

  const elAOV = document.getElementById('kpi-aov');
  if (elAOV) elAOV.textContent = fmtCurr(m.aov);

  renderCurrentPage();
}

function renderCurrentPage() {
  if (state.activePage === 'executive') {
    renderTrendChart();
    renderRegionalTable();
  } else if (state.activePage === 'pareto') {
    renderPareto();
  } else if (state.activePage === 'rfm') {
    renderRFM();
  } else if (state.activePage === 'whatif') {
    recalculateWhatIf();
  } else if (state.activePage === 'basket') {
    renderBasketAffinity();
  }
}

// Render Executive Trend Chart
function renderTrendChart() {
  const canvas = document.getElementById('chart-trend');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let rows = MONTHLY_DATA;
  if (state.selectedYear !== 'all') {
    rows = rows.filter(r => r.year === parseInt(state.selectedYear, 10));
  } else {
    // Show 2024-2025 by default for clarity
    rows = rows.filter(r => r.year >= 2024);
  }

  const labels = rows.map(r => `${r.month} '${String(r.year).slice(2)}`);
  const revData = rows.map(r => r.rev * (FX_RATES[state.selectedCurrency] || FX_RATES.USD).rate / 1000);
  
  // Calculate 3M Rolling window
  const rollingData = revData.map((val, idx, arr) => {
    if (idx === 0) return val;
    if (idx === 1) return (arr[0] + arr[1]) / 2;
    return (arr[idx - 2] + arr[idx - 1] + arr[idx]) / 3;
  });

  if (trendChart) trendChart.destroy();

  trendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: `Net Revenue (${state.selectedCurrency} K)`,
          data: revData,
          borderColor: '#118dff',
          backgroundColor: 'rgba(17, 141, 255, 0.1)',
          fill: true,
          tension: 0.3,
          borderWidth: 2.5
        },
        {
          label: 'Rolling 3M Avg (WINDOW DAX)',
          data: rollingData,
          borderColor: '#f2c811',
          borderDash: [5, 5],
          fill: false,
          tension: 0.3,
          borderWidth: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { font: { family: 'Segoe UI', size: 11 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${FX_RATES[state.selectedCurrency].symbol}${ctx.parsed.y.toLocaleString()}K`
          }
        }
      },
      scales: {
        y: {
          ticks: {
            callback: (v) => `${FX_RATES[state.selectedCurrency].symbol}${v}K`,
            font: { family: 'Segoe UI', size: 10 }
          },
          grid: { color: '#f0f0f0' }
        },
        x: {
          ticks: { font: { family: 'Segoe UI', size: 10 } },
          grid: { display: false }
        }
      }
    }
  });
}

// Render Regional Performance Breakdown
function renderRegionalTable() {
  const tbody = document.getElementById('table-region-body');
  if (!tbody) return;

  const m = getCalculatedMetrics();
  const regions = [
    { name: 'North America (NA)', share: 0.50, rep: 'Sarah Jenkins', vp: 'David Vance', target: 1.04 },
    { name: 'Europe, Middle East, Africa (EMEA)', share: 0.34, rep: 'Hans Becker', vp: 'Klaus Richter', target: 0.99 },
    { name: 'Asia Pacific (APAC)', share: 0.16, rep: 'Kenji Sato', vp: 'Mei Lin', target: 1.08 },
  ];

  tbody.innerHTML = regions.map(r => {
    const rev = m.netRevenue * r.share;
    const margin = m.grossMargin * r.share;
    const marginPct = rev > 0 ? (margin / rev) : 0;
    const badge = r.target >= 1.0 ? '<span class="badge badge-green">🟢 On Track</span>' : '<span class="badge badge-yellow">🟡 At Risk</span>';
    return `
      <tr>
        <td><strong>${r.name}</strong><br><span style="color:#605e5c;font-size:10px;">VP: ${r.vp}</span></td>
        <td class="num"><strong>${fmtCurr(rev)}</strong></td>
        <td class="num">${fmtCurr(margin)}</td>
        <td class="num">${fmtPct(marginPct)}</td>
        <td class="num">${fmtPct(r.share)}</td>
        <td>${badge}</td>
      </tr>
    `;
  }).join('');
}

// Render Pareto 80/20 & Top N
function renderPareto() {
  const tbody = document.getElementById('table-pareto-body');
  const cutoff = state.topN;
  let runningSum = 0;
  const totalRev = TOP_CUSTOMERS.reduce((a, b) => a + b.rev, 0);

  const enriched = TOP_CUSTOMERS.map((c, idx) => {
    runningSum += c.rev;
    const cumPct = runningSum / totalRev;
    const tier = cumPct <= 0.80 ? 'Tier A (Core 80%)' : (cumPct <= 0.95 ? 'Tier B (Growth 15%)' : 'Tier C (Long Tail 5%)');
    const color = cumPct <= 0.80 ? 'var(--pbi-green)' : (cumPct <= 0.95 ? 'var(--pbi-blue)' : 'var(--pbi-red)');
    return { ...c, rank: idx + 1, cumPct: cumPct, tier: tier, color: color };
  });

  if (tbody) {
    tbody.innerHTML = enriched.slice(0, cutoff).map(c => `
      <tr>
        <td><strong>#${c.rank}</strong></td>
        <td><strong>${c.name}</strong><br><span style="color:#605e5c;font-size:10px;">${c.segment} • ${c.region}</span></td>
        <td class="num"><strong>${fmtCurr(c.rev)}</strong></td>
        <td class="num">${fmtPct(c.cumPct)}</td>
        <td><span style="color:${c.color};font-weight:700;font-size:11px;">● ${c.tier}</span></td>
      </tr>
    `).join('');
  }

  // Render Pareto Chart
  const canvas = document.getElementById('chart-pareto');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  if (paretoChart) paretoChart.destroy();

  const chartCusts = enriched.slice(0, 15);
  paretoChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartCusts.map(c => c.name.split(' ')[0]),
      datasets: [
        {
          type: 'bar',
          label: `Customer Net Revenue (${state.selectedCurrency} K)`,
          data: chartCusts.map(c => c.rev * (FX_RATES[state.selectedCurrency] || FX_RATES.USD).rate / 1000),
          backgroundColor: '#118dff',
          yAxisID: 'y'
        },
        {
          type: 'line',
          label: 'Cumulative Pareto % (80/20 DAX)',
          data: chartCusts.map(c => Math.round(c.cumPct * 100)),
          borderColor: '#d83b01',
          borderWidth: 2.5,
          pointRadius: 4,
          fill: false,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          type: 'linear',
          position: 'left',
          ticks: { callback: v => `${v}K` }
        },
        y1: {
          type: 'linear',
          position: 'right',
          max: 100,
          min: 0,
          ticks: { callback: v => `${v}%` },
          grid: { display: false }
        }
      }
    }
  });

  // Update Pareto Metric Cards
  const topNShareEl = document.getElementById('kpi-topn-share');
  if (topNShareEl) {
    const topNRev = enriched.slice(0, cutoff).reduce((a, b) => a + b.rev, 0);
    topNShareEl.textContent = fmtPct(topNRev / totalRev);
  }
}

// Render RFM Cohorts & Customer Movement
function renderRFM() {
  const tbody = document.getElementById('table-rfm-body');
  if (!tbody) return;

  const rfmCohorts = [
    { segment: 'Champions', count: 42, ltv: 6850000, r: 5, f: 5, m: 5, action: 'Dedicated Executive Sponsor & Early Roadmap' },
    { segment: 'Loyal Enterprise', count: 86, ltv: 11200000, r: 4, f: 4, m: 4, action: 'Cross-sell Cloud Compute & Services' },
    { segment: 'Recent / Expanding', count: 54, ltv: 4320000, r: 5, f: 2, m: 3, action: 'Onboarding Check-in & Customer Success' },
    { segment: 'At-Risk High-Value', count: 28, ltv: 3100000, r: 2, f: 4, m: 4, action: 'Immediate Churn Intervention & QBR' },
    { segment: 'Hibernating / Dormant', count: 26, ltv: 1150000, r: 1, f: 2, m: 2, action: 'Automated Re-engagement Campaign' },
    { segment: 'Lost / Churned', count: 14, ltv: 580000, r: 1, f: 1, m: 1, action: 'Exit Interview & Win-back Analysis' },
  ];

  tbody.innerHTML = rfmCohorts.map(c => `
    <tr>
      <td><strong>${c.segment}</strong></td>
      <td class="num"><strong>${c.count}</strong></td>
      <td class="num">${fmtCurr(c.ltv)}</td>
      <td class="num" style="font-family:var(--font-mono);font-weight:700;">${c.r}-${c.f}-${c.m}</td>
      <td><span style="font-size:11px;color:#201f1e;">${c.action}</span></td>
    </tr>
  `).join('');
}

// Recalculate What-If Scenario Analysis
function recalculateWhatIf() {
  const m = getCalculatedMetrics();
  const priceAdj = state.priceAdjustment;
  const costAdj = state.costAdjustment;

  const simRev = m.netRevenue * (1 + priceAdj);
  const simCogs = (m.netRevenue - m.grossMargin) * (1 + costAdj);
  const simMargin = simRev - simCogs;
  const simMarginPct = simRev > 0 ? (simMargin / simRev) : 0;
  const marginDelta = simMargin - m.grossMargin;
  const bpsDelta = Math.round((simMarginPct - m.marginPct) * 10000);

  // Update What-If UI elements
  const elSimRev = document.getElementById('wi-sim-rev');
  if (elSimRev) elSimRev.textContent = fmtCurr(simRev);

  const elSimMargin = document.getElementById('wi-sim-margin');
  if (elSimMargin) elSimMargin.textContent = fmtCurr(simMargin);

  const elSimMarginPct = document.getElementById('wi-sim-pct');
  if (elSimMarginPct) elSimMarginPct.textContent = fmtPct(simMarginPct);

  const elDelta = document.getElementById('wi-sim-delta');
  if (elDelta) {
    elDelta.textContent = (marginDelta >= 0 ? '+' : '') + fmtCurr(marginDelta);
    elDelta.style.color = marginDelta >= 0 ? 'var(--pbi-green)' : 'var(--pbi-red)';
  }

  const elBps = document.getElementById('wi-sim-bps');
  if (elBps) {
    elBps.textContent = (bpsDelta >= 0 ? '+' : '') + bpsDelta + ' bps';
    elBps.style.color = bpsDelta >= 0 ? 'var(--pbi-green)' : 'var(--pbi-red)';
  }

  const elNarrative = document.getElementById('wi-narrative');
  if (elNarrative) {
    elNarrative.textContent = `Scenario Outcome: A ${(priceAdj >= 0 ? '+' : '') + Math.round(priceAdj * 100)}% price adjustment combined with a ${(costAdj >= 0 ? '+' : '') + Math.round(costAdj * 100)}% supplier inflation yields a ${marginDelta >= 0 ? 'net gain of ' : 'net contraction of '}${fmtCurr(Math.abs(marginDelta))} in Gross Margin (${(bpsDelta >= 0 ? '+' : '') + bpsDelta} bps).`;
  }

  renderWhatIfSensitivityChart(m.grossMargin, simMargin, marginDelta);
}

function renderWhatIfSensitivityChart(actualMargin, simMargin, delta) {
  const canvas = document.getElementById('chart-sensitivity');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  if (sensitivityChart) sensitivityChart.destroy();

  const fxRate = (FX_RATES[state.selectedCurrency] || FX_RATES.USD).rate;
  sensitivityChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Baseline Actual Margin', 'Scenario Simulated Margin', 'Net Margin Delta ($)'],
      datasets: [{
        label: `Amount (${state.selectedCurrency} K)`,
        data: [
          actualMargin * fxRate / 1000,
          simMargin * fxRate / 1000,
          delta * fxRate / 1000
        ],
        backgroundColor: [
          '#118dff',
          '#107c41',
          delta >= 0 ? '#107c41' : '#d83b01'
        ]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          ticks: { callback: v => `${FX_RATES[state.selectedCurrency].symbol}${v}K` }
        }
      }
    }
  });
}

// Render Basket Affinity
function renderBasketAffinity() {
  const tbody = document.getElementById('table-basket-body');
  if (!tbody) return;

  tbody.innerHTML = BASKET_AFFINITY_DATA.map(item => `
    <tr>
      <td><strong>${item.focus}</strong></td>
      <td><strong>${item.comp}</strong></td>
      <td class="num">${fmtPct(item.support)}</td>
      <td class="num"><strong>${fmtPct(item.conf)}</strong></td>
      <td class="num"><strong style="color:var(--pbi-accent);">${item.lift.toFixed(2)}x</strong></td>
      <td><span class="dax-badge-pill">${item.status}</span></td>
    </tr>
  `).join('');
}

// DAX Studio Code Explorer
function setupDaxStudio() {
  const measureBtns = document.querySelectorAll('.dax-measure-btn');
  const daxNameEl = document.getElementById('dax-active-name');
  const daxCatEl = document.getElementById('dax-active-cat');
  const daxCodeEl = document.getElementById('dax-code-content');
  const daxLogicEl = document.getElementById('dax-logic-text');
  const daxEngineEl = document.getElementById('dax-engine-text');

  measureBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      measureBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const key = btn.dataset.key;
      const data = DAX_LIBRARY[key];
      if (data) {
        if (daxNameEl) daxNameEl.textContent = data.title;
        if (daxCatEl) daxCatEl.textContent = data.category;
        if (daxCodeEl) daxCodeEl.textContent = data.expression;
        if (daxLogicEl) daxLogicEl.textContent = data.logic;
        if (daxEngineEl) daxEngineEl.textContent = data.engine;
      }
    });
  });

  // Copy DAX Button
  const copyBtn = document.getElementById('btn-copy-dax');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const code = daxCodeEl.textContent;
      navigator.clipboard.writeText(code).then(() => {
        const orig = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        setTimeout(() => copyBtn.textContent = orig, 2000);
      });
    });
  }
}
