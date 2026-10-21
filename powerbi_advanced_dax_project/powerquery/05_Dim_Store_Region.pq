// =========================================================================
// POWER QUERY (M) - 05_Dim_Store_Region.pq
// Sales Channels & Organizational Hierarchy Dimension
// =========================================================================

let
    Source = Csv.Document(File.Contents(#"DataFolderPath" & "Dim_Store_Region.csv"), [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"ChannelID", type text},
        {"ChannelName", type text},
        {"RegionCode", type text},
        {"RegionName", type text},
        {"Country", type text},
        {"RegionalVP", type text},
        {"SalesDirector", type text},
        {"HierarchyPath", type text},
        {"ChannelType", type text},
        {"CommissionTier", type text}
    })
in
    ChangeTypes
