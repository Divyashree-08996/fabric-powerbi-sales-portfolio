# 🚀 CI/CD, Git Integration & Deployment Pipelines in Microsoft Fabric

This guide outlines the enterprise software development lifecycle (SDLC) for deploying and maintaining the **Pre-Sales Analytics Project** across Development, Test, and Production environments in **Microsoft Fabric**.

---

## 🏗️ 1. Multi-Stage Workspace Architecture

In enterprise Fabric deployments, isolate environments using dedicated Fabric workspaces backed by an Azure DevOps or GitHub repository:

```
+-----------------------------------------------------------------------------------+
|                        Azure DevOps / GitHub Repository                           |
|   Branches: feature/*  -->  develop  -->  release/*  -->  main                    |
+-----------------------------------------------------------------------------------+
       │                            │                             │
       ▼                            ▼                             ▼
+---------------------+     +---------------------+     +---------------------+
| Fabric Dev Workspace|     |Fabric Test Workspace|     | Fabric Prod Workspace|
| - Lakehouse (Dev)   | --> | - Lakehouse (UAT)   | --> | - Lakehouse (Prod)  |
| - Notebooks 01-03   |     | - Automated Tests   |     | - Direct Lake Model |
| - Data Pipelines    |     | - Power BI QA Report|     | - Exec Dashboards   |
+---------------------+     +---------------------+     +---------------------+
```

---

## 🔗 2. Fabric Native Git Integration Setup

Microsoft Fabric natively syncs workspace items with Git repositories:

### Step-by-Step Configuration:
1. In Microsoft Fabric, go to **Workspace Settings** $\rightarrow$ **Git Integration**.
2. Select your Git provider: **Azure DevOps** or **GitHub**.
3. Choose the organization, repository, and branch:
   - Dev Workspace syncs to `develop` or `feature/<name>`.
   - Test Workspace syncs to `release/v1.0`.
   - Production Workspace syncs to `main`.
4. Fabric automatically tracks all changes to:
   - Lakehouses & Warehouse definitions
   - PySpark Notebooks (`notebook-content.py` and metadata)
   - Fabric Data Pipelines (`pipeline-content.json`)
   - Direct Lake Semantic Models (`definition.pbism` / `model.bim`)
   - Power BI Reports (`definition.pbir`)

---

## 📦 3. Fabric Deployment Pipelines

Use **Fabric Deployment Pipelines** for promoting code between workspaces with automated rule replacements:

### Stage Setup:
1. **Development**:
   - Data source: Small sample data or anonymized CRM extract.
   - Run frequency: On demand.
2. **Test / UAT**:
   - Data source: Full synthetic volume or staging CRM replica.
   - Validation: Run automated notebook data quality checks (`assert df.count() > 0`).
3. **Production**:
   - Data source: Production CRM (Salesforce / HubSpot / Vivun) via OneLake Shortcuts or CDC.
   - Direct Lake model actively serves executive reporting with zero downtime.

### Deployment Parameter Rules:
When promoting from Dev to Prod, configure **Deployment Rules**:
- **Lakehouse Connection**: Swap `lh_presales_dev` $\rightarrow$ `lh_presales_prod`.
- **Pipeline Parameters**: Swap `notification_webhook` to production alerts channel.

---

## ⚡ 4. Fabric Capacity Sizing & Cost Optimization

### Recommended Capacity:
- **Development / Testing**: **F2** to **F16** capacity or Fabric Trial.
- **Production (Enterprise 1,000+ Users)**: **F64** (Includes Power BI Premium reporting without per-user licensing requirements).

### Cost Reduction Best Practices:
1. **Auto-Pause & Scheduled Scaling**:
   - Pause Dev/Test capacities during non-business hours using Azure Automation or Azure Logic Apps.
2. **Starter Spark Pool vs. Custom Pool**:
   - Use the **Starter Pool** in Fabric (sub-5 second cold start!) for fast ingestion and transformation notebooks.
3. **V-Order & Native Compaction**:
   - Keep V-Order enabled (`SET spark.sql.parquet.vorder.enabled = true`). V-Order parquet reduces storage foot-print in OneLake by 30-40% and provides up to 10x query acceleration for Direct Lake!
