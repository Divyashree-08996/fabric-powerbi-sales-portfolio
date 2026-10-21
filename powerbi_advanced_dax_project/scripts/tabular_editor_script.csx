// ===============================================================================
// TABULAR EDITOR C# AUTOMATION SCRIPT: tabular_editor_script.csx
// Automated deployment of Calculation Groups, Measure Tables, Display Folders,
// and Dynamic Format Strings for Enterprise Tabular Models (Compatibility 1567+)
// Author: Alex Rivera | DP-600 & PL-300 Certified Analytics Engineer
// ===============================================================================

// 1. Create Dedicated Measure Tables if they do not exist
var coreMeasuresTable = Model.Tables.FirstOrDefault(t => t.Name == "_Measures_Core");
if (coreMeasuresTable == null) {
    coreMeasuresTable = Model.AddTable("_Measures_Core");
    coreMeasuresTable.Description = "Container for core volume, financial, and unit economics measures";
}

// 2. Add Time Intelligence Calculation Group
var timeCalcGroup = Model.Tables.FirstOrDefault(t => t.Name == "Time Intelligence");
if (timeCalcGroup != null) {
    Model.Tables.Remove(timeCalcGroup);
}

var calcGroupTable = Model.AddCalculationGroup("Time Intelligence");
calcGroupTable.CalculationGroup.Precedence = 20;

// Add Calculation Items
var itemCurrent = calcGroupTable.CalculationGroup.AddCalculationItem("Current", "SELECTEDMEASURE()");
itemCurrent.FormatStringExpression = "SELECTEDMEASUREFORMATSTRING()";

var itemPY = calcGroupTable.CalculationGroup.AddCalculationItem("Prior Year (PY)", "CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Dim_Date'[Date]))");
itemPY.FormatStringExpression = "SELECTEDMEASUREFORMATSTRING()";

var itemYoY = calcGroupTable.CalculationGroup.AddCalculationItem("YoY Variance", @"
VAR _Current = SELECTEDMEASURE()
VAR _PY = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Dim_Date'[Date]))
RETURN IF(NOT ISBLANK(_Current) && NOT ISBLANK(_PY), _Current - _PY, BLANK())");
itemYoY.FormatStringExpression = "SELECTEDMEASUREFORMATSTRING()";

var itemYoYPct = calcGroupTable.CalculationGroup.AddCalculationItem("YoY %", @"
VAR _Current = SELECTEDMEASURE()
VAR _PY = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Dim_Date'[Date]))
RETURN DIVIDE(_Current - _PY, _PY, BLANK())");
itemYoYPct.FormatStringExpression = "\"+0.0%;-0.0%;0.0%\"";

var itemYTD = calcGroupTable.CalculationGroup.AddCalculationItem("YTD", "TOTALYTD(SELECTEDMEASURE(), 'Dim_Date'[Date])");
itemYTD.FormatStringExpression = "SELECTEDMEASUREFORMATSTRING()";

var itemPYTD = calcGroupTable.CalculationGroup.AddCalculationItem("PYTD", "CALCULATE(TOTALYTD(SELECTEDMEASURE(), 'Dim_Date'[Date]), SAMEPERIODLASTYEAR('Dim_Date'[Date]))");
itemPYTD.FormatStringExpression = "SELECTEDMEASUREFORMATSTRING()";

var itemYTDYoYPct = calcGroupTable.CalculationGroup.AddCalculationItem("YTD YoY %", @"
VAR _CurrentYTD = TOTALYTD(SELECTEDMEASURE(), 'Dim_Date'[Date])
VAR _PYTD = CALCULATE(TOTALYTD(SELECTEDMEASURE(), 'Dim_Date'[Date]), SAMEPERIODLASTYEAR('Dim_Date'[Date]))
RETURN DIVIDE(_CurrentYTD - _PYTD, _PYTD, BLANK())");
itemYTDYoYPct.FormatStringExpression = "\"+0.0%;-0.0%;0.0%\"";

var itemRolling3M = calcGroupTable.CalculationGroup.AddCalculationItem("Rolling 3M Avg", @"
VAR _WindowRows = WINDOW(-2, RELATIVE, 0, RELATIVE, ALLSELECTED('Dim_Date'[YearMonth]), ORDERBY('Dim_Date'[YearMonth], ASC))
RETURN CALCULATE(AVERAGEX(VALUES('Dim_Date'[YearMonth]), SELECTEDMEASURE()), _WindowRows)");
itemRolling3M.FormatStringExpression = "SELECTEDMEASUREFORMATSTRING()";

// 3. Batch Configure Display Folders & Formatting across all Measures
foreach (var m in Model.AllMeasures) {
    if (m.Name.Contains("%") || m.Name.Contains("Rate") || m.Name.Contains("Share") || m.Name.Contains("Pct")) {
        m.FormatString = "0.0%";
    } else if (m.Name.Contains("$") || m.Name.Contains("Revenue") || m.Name.Contains("Cost") || m.Name.Contains("Margin") || m.Name.Contains("Price") || m.Name.Contains("AOV") || m.Name.Contains("ASP") || m.Name.Contains("Discounts")) {
        m.FormatString = "$#,##0";
    } else if (m.Name.Contains("Orders") || m.Name.Contains("Count") || m.Name.Contains("Units") || m.Name.Contains("Days") || m.Name.Contains("Transactions")) {
        m.FormatString = "#,##0";
    }
    
    // Assign display folders
    if (m.Name.Contains("PY") || m.Name.Contains("YoY") || m.Name.Contains("YTD") || m.Name.Contains("MoM") || m.Name.Contains("OFFSET") || m.Name.Contains("WINDOW") || m.Name.Contains("Rolling")) {
        m.DisplayFolder = "Time Intelligence";
    } else if (m.Name.Contains("Pareto") || m.Name.Contains("Top N") || m.Name.Contains("Rank")) {
        m.DisplayFolder = "Pareto & Concentration";
    } else if (m.Name.Contains("RFM") || m.Name.Contains("Churn") || m.Name.Contains("Retention") || m.Name.Contains("Customer")) {
        m.DisplayFolder = "Customer Intelligence";
    } else if (m.Name.Contains("Basket") || m.Name.Contains("Lift") || m.Name.Contains("Confidence") || m.Name.Contains("Support") || m.Name.Contains("Cross-Sell")) {
        m.DisplayFolder = "Basket & Affinity";
    } else if (m.Name.Contains("Currency") || m.Name.Contains("FX") || m.Name.Contains("Converted")) {
        m.DisplayFolder = "Multi-Currency";
    } else if (m.Name.Contains("Simulated") || m.Name.Contains("Scenario") || m.Name.Contains("What-If")) {
        m.DisplayFolder = "What-If Modeling";
    } else if (m.Name.Contains("Budget") || m.Name.Contains("Target") || m.Name.Contains("Attainment")) {
        m.DisplayFolder = "Budget & Targets";
    } else if (m.Name.Contains("SVG")) {
        m.DisplayFolder = "SVG Visuals";
        m.DataCategory = "ImageUrl";
    } else {
        m.DisplayFolder = "Core Metrics";
    }
}

Output("Tabular Model automated setup completed successfully. All Calculation Groups and Display Folders initialized!");
