// =========================================================================
// POWER QUERY (M) - 07_Fact_Sales.pq
// Sales Transaction Line Items Fact Table
// =========================================================================

let
    Source = Csv.Document(File.Contents(#"DataFolderPath" & "Fact_Sales.csv"), [Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"SalesLineID", Int64.Type},
        {"SalesOrderNumber", type text},
        {"OrderLineNumber", Int64.Type},
        {"OrderDate", type date},
        {"ShipDate", type date},
        {"CustomerID", type text},
        {"ProductID", type text},
        {"ChannelID", type text},
        {"TransactionCurrency", type text},
        {"Quantity", Int64.Type},
        {"LocalGrossSales", Currency.Type},
        {"LocalDiscount", Currency.Type},
        {"LocalNetSales", Currency.Type},
        {"GrossSalesUSD", Currency.Type},
        {"DiscountAmountUSD", Currency.Type},
        {"NetSalesUSD", Currency.Type},
        {"TotalCostUSD", Currency.Type},
        {"MarginUSD", Currency.Type},
        {"OrderStatus", type text}
    })
in
    ChangeTypes
