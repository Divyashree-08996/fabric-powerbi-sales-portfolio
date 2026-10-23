-- Microsoft Fabric SQL Analytics Endpoint: 02_kpi_analytical_queries.sql
-- Validation and Ad-Hoc Analytics Queries for Sales Performance

-- 1. Executive Revenue, Margin & Order Summary by Fiscal Year
SELECT 
    d.[FiscalYear],
    COUNT(DISTINCT s.SalesOrderNumber) AS TotalOrders,
    SUM(s.Quantity) AS TotalUnitsSold,
    ROUND(SUM(s.NetSalesUSD), 2) AS TotalNetSalesUSD,
    ROUND(SUM(s.TotalCostUSD), 2) AS TotalCostUSD,
    ROUND(SUM(s.MarginUSD), 2) AS TotalGrossProfitUSD,
    ROUND(SUM(s.MarginUSD) / NULLIF(SUM(s.NetSalesUSD), 0) * 100, 2) AS GrossMarginPct,
    ROUND(SUM(s.NetSalesUSD) / NULLIF(COUNT(DISTINCT s.SalesOrderNumber), 0), 2) AS AverageOrderValueUSD
FROM v_fact_sales s
JOIN v_dim_date d ON s.OrderDateKey = d.DateKey
GROUP BY d.[FiscalYear]
ORDER BY d.[FiscalYear] DESC;

-- 2. Monthly Sales vs Budget Variance
SELECT 
    d.YearMonth,
    d.MonthName,
    ROUND(SUM(s.NetSalesUSD), 2) AS ActualSalesUSD,
    ROUND(b.BudgetUSD, 2) AS BudgetUSD,
    ROUND(SUM(s.NetSalesUSD) - b.BudgetUSD, 2) AS VarianceUSD,
    ROUND((SUM(s.NetSalesUSD) - b.BudgetUSD) / NULLIF(b.BudgetUSD, 0) * 100, 2) AS VariancePct
FROM v_fact_sales s
JOIN v_dim_date d ON s.OrderDateKey = d.DateKey
LEFT JOIN (
    SELECT YearMonth, SUM(BudgetUSD) AS BudgetUSD
    FROM v_fact_budget
    GROUP BY YearMonth
) b ON d.YearMonth = b.YearMonth
GROUP BY d.YearMonth, d.MonthName, b.BudgetUSD
ORDER BY d.YearMonth;

-- 3. Top 10 Enterprise Customers by Revenue
SELECT TOP 10
    c.CustomerID,
    c.CustomerName,
    c.Country,
    c.CustomerSegment,
    ROUND(SUM(s.NetSalesUSD), 2) AS TotalRevenueUSD,
    ROUND(SUM(s.MarginUSD) / NULLIF(SUM(s.NetSalesUSD), 0) * 100, 2) AS MarginPct
FROM v_fact_sales s
JOIN v_dim_customer c ON s.CustomerKey = c.CustomerKey
GROUP BY c.CustomerID, c.CustomerName, c.Country, c.CustomerSegment
ORDER BY TotalRevenueUSD DESC;
