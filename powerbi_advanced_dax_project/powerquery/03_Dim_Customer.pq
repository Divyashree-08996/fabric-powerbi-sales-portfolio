// =========================================================================
// POWER QUERY (M) - 03_Dim_Customer.pq
// Ingestion, typing, and enrichment for Dim_Customer
// =========================================================================

let
    Source = Csv.Document(File.Contents(#"DataFolderPath" & "Dim_Customer.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"CustomerID", type text},
        {"CustomerName", type text},
        {"CustomerSegment", type text},
        {"Country", type text},
        {"Region", type text},
        {"CreditRating", type text},
        {"AccountManagerEmail", type text},
        {"CustomerJoinDate", type date},
        {"IsStrategicAccount", Int64.Type}
    }),
    CleanWhitespace = Table.TransformColumns(ChangeTypes, {{"CustomerName", Text.Trim, type text}})
in
    CleanWhitespace
