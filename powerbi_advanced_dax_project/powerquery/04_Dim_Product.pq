// =========================================================================
// POWER QUERY (M) - 04_Dim_Product.pq
// Ingestion, hierarchy structuring, and typing for Dim_Product
// =========================================================================

let
    Source = Csv.Document(File.Contents(#"DataFolderPath" & "Dim_Product.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"ProductID", type text},
        {"ProductName", type text},
        {"Category", type text},
        {"SubCategory", type text},
        {"StandardCost", Currency.Type},
        {"ListPrice", Currency.Type},
        {"StandardMarginPercent", Percentage.Type},
        {"IsActive", Int64.Type}
    })
in
    ChangeTypes
