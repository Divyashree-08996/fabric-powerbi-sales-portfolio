// =========================================================================
// POWER QUERY (M) - 02_Dim_Date.pq
// Dynamic Enterprise Date Table Generator with Fiscal Year & Relative Offsets
// Generates a continuous calendar without external file dependencies.
// =========================================================================

let
    // 1. Define calendar boundaries
    StartDate = #date(2023, 1, 1),
    EndDate = #date(2026, 12, 31),
    DayCount = Duration.Days(Duration.From(EndDate - StartDate)) + 1,
    
    // 2. Generate date list
    DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    TableFromList = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    ChangedTypeDate = Table.TransformColumnTypes(TableFromList, {{"Date", type date}}),
    
    // 3. Add Calendar attributes
    AddDateKey = Table.AddColumn(ChangedTypeDate, "DateKey", each Date.Year([Date]) * 10000 + Date.Month([Date]) * 100 + Date.Day([Date]), Int64.Type),
    AddYear = Table.AddColumn(AddDateKey, "Year", each Date.Year([Date]), Int64.Type),
    AddYearMonth = Table.AddColumn(AddYear, "YearMonth", each Date.Year([Date]) * 100 + Date.Month([Date]), Int64.Type),
    AddMonthName = Table.AddColumn(AddYearMonth, "MonthName", each Date.MonthName([Date]), type text),
    AddMonthShort = Table.AddColumn(AddMonthName, "MonthShort", each Date.ToText([Date], "MMM"), type text),
    AddMonthNumber = Table.AddColumn(AddMonthShort, "MonthNumber", each Date.Month([Date]), Int64.Type),
    AddQuarter = Table.AddColumn(AddMonthNumber, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    AddYearQuarter = Table.AddColumn(AddQuarter, "YearQuarter", each Text.From(Date.Year([Date])) & "-Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    AddQuarterNumber = Table.AddColumn(AddYearQuarter, "QuarterNumber", each Date.QuarterOfYear([Date]), Int64.Type),
    AddDayOfMonth = Table.AddColumn(AddQuarterNumber, "DayOfMonth", each Date.Day([Date]), Int64.Type),
    AddDayOfWeekNumber = Table.AddColumn(AddDayOfMonth, "DayOfWeekNumber", each Date.DayOfWeek([Date], Day.Monday) + 1, Int64.Type),
    AddDayOfWeekName = Table.AddColumn(AddDayOfWeekNumber, "DayOfWeekName", each Date.DayOfWeekName([Date]), type text),
    AddDayOfWeekShort = Table.AddColumn(AddDayOfWeekName, "DayOfWeekShort", each Date.ToText([Date], "ddd"), type text),
    AddIsWeekend = Table.AddColumn(AddDayOfWeekShort, "IsWeekend", each if Date.DayOfWeek([Date], Day.Monday) >= 5 then 1 else 0, Int64.Type),
    AddIsWorkday = Table.AddColumn(AddIsWeekend, "IsWorkday", each if [IsWeekend] = 1 then 0 else 1, Int64.Type),
    
    // 4. Fiscal Calendar (Fiscal Year begins July 1st)
    AddFiscalYear = Table.AddColumn(AddIsWorkday, "FiscalYear", each if Date.Month([Date]) >= 7 then "FY" & Text.From(Date.Year([Date]) + 1) else "FY" & Text.From(Date.Year([Date])), type text),
    AddFiscalQuarter = Table.AddColumn(AddFiscalYear, "FiscalQuarter", each if Date.Month([Date]) >= 7 then "FQ" & Text.From(Number.IntegerDivide(Date.Month([Date]) - 7, 3) + 1) else "FQ" & Text.From(Number.IntegerDivide(Date.Month([Date]) + 5, 3) + 1), type text),
    AddFiscalYearQuarter = Table.AddColumn(AddFiscalQuarter, "FiscalYearQuarter", each [FiscalYear] & "-" & [FiscalQuarter], type text),
    AddFiscalPeriod = Table.AddColumn(AddFiscalYearQuarter, "FiscalPeriod", each if Date.Month([Date]) >= 7 then Date.Month([Date]) - 6 else Date.Month([Date]) + 6, Int64.Type),
    
    // 5. Relative Offsets (calculated from today's reference point)
    CurrentDate = DateTime.Date(DateTime.LocalNow()),
    CurrentYear = Date.Year(CurrentDate),
    CurrentMonth = Date.Month(CurrentDate),
    AddMonthOffset = Table.AddColumn(AddFiscalPeriod, "MonthOffset", each (Date.Year([Date]) - CurrentYear) * 12 + (Date.Month([Date]) - CurrentMonth), Int64.Type),
    AddDayOffset = Table.AddColumn(AddMonthOffset, "DayOffset", each Duration.Days(Duration.From([Date] - CurrentDate)), Int64.Type)
in
    AddDayOffset
