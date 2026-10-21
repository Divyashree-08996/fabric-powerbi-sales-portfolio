// =========================================================================
// POWER QUERY (M) - 08_Fact_Budget.pq
// Budget and Financial Targets at Category & Regional Grain
// =========================================================================

let
    Source = Csv.Document(File.Contents(#"DataFolderPath" & "Fact_Budget.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"BudgetID", Int64.Type},
        {"BudgetMonthDate", type date},
        {"YearMonth", Int64.Type},
        {"Category", type text},
        {"RegionCode", type text},
        {"TargetRevenueUSD", Currency.Type},
        {"TargetMarginUSD", Currency.Type}
    })
in
    ChangeTypes
