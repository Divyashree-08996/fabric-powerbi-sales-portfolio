-- Microsoft Fabric SQL Analytics Endpoint: 01_create_star_schema_views.sql
-- Lakehouse: lh_sales_analytics
-- Target: Clean consumption views for Power BI Direct Lake / SQL DirectQuery

-- 1. Date Dimension View
CREATE OR ALTER VIEW v_dim_date AS
SELECT 
    DateKey,
    [Date],
    [Year],
    [Quarter],
    MonthNum,
    MonthName,
    YearMonth,
    DayOfWeek,
    IsWeekend,
    FiscalYear,
    FiscalQuarter
FROM gold_dim_date;
GO

-- 2. Customer Dimension View
CREATE OR ALTER VIEW v_dim_customer AS
SELECT 
    CustomerKey,
    CustomerID,
    CustomerName,
    CustomerSegment,
    Country,
    Region,
    CreditRating,
    AccountManagerEmail,
    CustomerJoinDate,
    IsStrategicAccount
FROM gold_dim_customer;
GO

-- 3. Product Dimension View
CREATE OR ALTER VIEW v_dim_product AS
SELECT 
    ProductKey,
    ProductID,
    ProductName,
    Category,
    SubCategory,
    StandardCostUSD,
    ListPriceUSD,
    StandardMarginPercent,
    IsActive
FROM gold_dim_product;
GO

-- 4. Store Region Dimension View
CREATE OR ALTER VIEW v_dim_store_region AS
SELECT 
    StoreRegionKey,
    ChannelID,
    ChannelName,
    RegionCode,
    RegionName,
    Country,
    RegionalVP,
    SalesDirector,
    ChannelType,
    CommissionTier
FROM gold_dim_store_region;
GO

-- 5. Fact Sales View
CREATE OR ALTER VIEW v_fact_sales AS
SELECT 
    SalesLineID,
    SalesOrderNumber,
    OrderLineNumber,
    OrderDateKey,
    ShipDateKey,
    CustomerKey,
    ProductKey,
    StoreRegionKey,
    Quantity,
    GrossSalesUSD,
    DiscountAmountUSD,
    NetSalesUSD,
    TotalCostUSD,
    MarginUSD,
    GrossMarginPct,
    DiscountPct,
    FulfillmentDays,
    OrderStatus
FROM gold_fact_sales;
GO

-- 6. Fact Budget View
CREATE OR ALTER VIEW v_fact_budget AS
SELECT 
    BudgetID,
    DateKey,
    YearMonth,
    StoreRegionKey,
    Category,
    BudgetUSD
FROM gold_fact_budget;
GO
