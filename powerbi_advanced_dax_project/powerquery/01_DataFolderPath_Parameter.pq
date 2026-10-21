// =========================================================================
// POWER QUERY (M) - 01_DataFolderPath_Parameter.pq
// Global parameter defining the base folder containing the project CSV files.
// Modify this path when deploying to different environments.
// =========================================================================

let
    // Default relative or absolute path to the data folder
    SourceFolder = "C:\Users\hp\Documents\antigravity\dazzling-hypatia\powerbi_advanced_dax_project\data\" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
in
    SourceFolder
