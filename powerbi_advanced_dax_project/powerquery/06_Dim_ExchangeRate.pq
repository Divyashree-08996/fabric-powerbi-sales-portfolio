// =========================================================================
// POWER QUERY (M) - 06_Dim_ExchangeRate.pq
// Daily FX rates for multi-currency dynamic consolidation
// =========================================================================

let
    Source = Csv.Document(File.Contents(#"DataFolderPath" & "Dim_ExchangeRate.csv"), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"Date", type date},
        {"CurrencyCode", type text},
        {"LocalPerUSD", type number},
        {"USDPerLocal", type number}
    })
in
    ChangeTypes
