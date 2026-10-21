// =========================================================================
// POWER QUERY (M) - 09_Disconnected_Parameters.pq
// Disconnected tables for What-If Analysis, Currency Selector, and Top N Slicers
// =========================================================================

// Table 1: Param_ReportingCurrency
let
    SourceCurrency = Csv.Document(File.Contents(#"DataFolderPath" & "Param_ReportingCurrency.csv"), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeadersCurr = Table.PromoteHeaders(SourceCurrency, [PromoteAllScalars=true]),
    ChangeTypesCurr = Table.TransformColumnTypes(PromoteHeadersCurr, {
        {"CurrencyCode", type text},
        {"CurrencyName", type text},
        {"CurrencySymbol", type text},
        {"IsDefault", Int64.Type}
    })
in
    ChangeTypesCurr;

// Table 2: Param_WhatIf_Price
let
    SourcePrice = Csv.Document(File.Contents(#"DataFolderPath" & "Param_WhatIf_Price.csv"), [Delimiter=",", Columns=2, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeadersPrice = Table.PromoteHeaders(SourcePrice, [PromoteAllScalars=true]),
    ChangeTypesPrice = Table.TransformColumnTypes(PromoteHeadersPrice, {
        {"PriceAdjustmentPercent", Percentage.Type},
        {"PriceAdjustmentLabel", type text}
    })
in
    ChangeTypesPrice;

// Table 3: Param_WhatIf_Cost
let
    SourceCost = Csv.Document(File.Contents(#"DataFolderPath" & "Param_WhatIf_Cost.csv"), [Delimiter=",", Columns=2, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeadersCost = Table.PromoteHeaders(SourceCost, [PromoteAllScalars=true]),
    ChangeTypesCost = Table.TransformColumnTypes(PromoteHeadersCost, {
        {"CostAdjustmentPercent", Percentage.Type},
        {"CostAdjustmentLabel", type text}
    })
in
    ChangeTypesCost;

// Table 4: Param_TopN
let
    SourceTopN = Csv.Document(File.Contents(#"DataFolderPath" & "Param_TopN.csv"), [Delimiter=",", Columns=2, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeadersTopN = Table.PromoteHeaders(SourceTopN, [PromoteAllScalars=true]),
    ChangeTypesTopN = Table.TransformColumnTypes(PromoteHeadersTopN, {
        {"TopNValue", Int64.Type},
        {"TopNLabel", type text}
    })
in
    ChangeTypesTopN;

// Table 5: Param_MetricSelector
let
    SourceMetric = Csv.Document(File.Contents(#"DataFolderPath" & "Param_MetricSelector.csv"), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeadersMetric = Table.PromoteHeaders(SourceMetric, [PromoteAllScalars=true]),
    ChangeTypesMetric = Table.TransformColumnTypes(PromoteHeadersMetric, {
        {"MetricID", Int64.Type},
        {"MetricName", type text},
        {"DisplayOrder", Int64.Type},
        {"FormatType", type text}
    })
in
    ChangeTypesMetric;
