# 🔒 Row-Level Security (RLS) & Data Governance in Microsoft Fabric Direct Lake

This guide describes how to implement **Row-Level Security (RLS)** and **Object-Level Security (OLS)** for the Pre-Sales Analytics engine across **Microsoft Fabric OneLake** and the **Power BI Direct Lake Semantic Model**.

---

## 🛡️ 1. Security Architecture & Personas

Enterprise Pre-Sales organizations require strict access governance:
- **Global Pre-Sales Leadership & CRO**: Unrestricted worldwide visibility into all pipeline deals, POC projects, SE capacity, and revenue metrics.
- **Regional SE Directors (e.g., North America, EMEA, APAC, LATAM)**: Visibility restricted to accounts, opportunities, activities, and SE team members assigned to their respective geographic regions.
- **Individual Solution Engineers**: Visibility restricted only to the deals, POCs, and activities they are directly assigned to, plus read-only access to global product catalog benchmarks.

```
+-----------------------------------------------------------------------------------+
|                            Microsoft Entra ID (Azure AD)                         |
|   Security Groups: AAD-Presales-Global-Execs, AAD-Presales-EMEA-Directors, etc.  |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|               Power BI Direct Lake Semantic Model RLS Filter Rules                |
|                                                                                   |
|  [Role: Regional_SE_Lead]                                                         |
|  gold_dim_account[region] == LOOKUPVALUE(...)                                     |
|                                                                                   |
|  [Role: Individual_SE]                                                            |
|  gold_dim_solution_engineer[email] == USERPRINCIPALNAME()                         |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|         Filtered Result Set Streamed to Power BI Dashboards in OneLake            |
+-----------------------------------------------------------------------------------+
```

---

## 🔑 2. Implementing RLS in the Direct Lake Semantic Model

In Microsoft Fabric Direct Lake mode, DAX Row-Level Security is configured directly in the semantic model definitions (via Fabric Web Modeler, Tabular Editor, or PBIP).

### Role 1: `Regional_SE_Lead`
Filters the entire Star Schema by propagating through the `gold_dim_account` and `gold_dim_solution_engineer` tables.

**DAX Filter Expression on `gold_dim_solution_engineer`**:
```dax
[region] = 
LOOKUPVALUE(
    Security_User_Region_Mapping[AssignedRegion],
    Security_User_Region_Mapping[UserPrincipalName],
    USERPRINCIPALNAME()
)
```

**DAX Filter Expression on `gold_dim_account`**:
```dax
[region] = 
LOOKUPVALUE(
    Security_User_Region_Mapping[AssignedRegion],
    Security_User_Region_Mapping[UserPrincipalName],
    USERPRINCIPALNAME()
)
```

Because of standard 1-to-Many single-direction relationships from `gold_dim_account` and `gold_dim_solution_engineer` down to `gold_fact_opportunity_snapshot`, `gold_fact_poc`, and `gold_fact_presales_activity`, the filtering flows naturally to all transactional facts!

---

### Role 2: `Individual_SE_Access`
Enforces individual contributor data privacy, ensuring Solution Engineers only see their personal activities, pipeline contributions, and assigned POCs.

**DAX Filter Expression on `gold_dim_solution_engineer`**:
```dax
[email] = USERPRINCIPALNAME()
```

When this filter is applied:
- The dimension `gold_dim_solution_engineer` shrinks to 1 single row for the logged-in engineer.
- All joined facts (`gold_fact_presales_activity`, `gold_fact_poc`) automatically filter to only show this engineer's engagements.

---

### Role 3: `Executive_Unrestricted`
No DAX filter applied. Entra ID group `AAD-Presales-Global-Execs` is mapped directly to this role in the Power BI Service security settings.

---

## 🏗️ 3. Direct Lake Native Security vs. OneLake Data Access Roles

Microsoft Fabric introduced **OneLake Data Access Roles (Preview)**, allowing security to be enforced directly at the storage level in OneLake:

1. **Storage-Level RLS (Lakehouse / Delta Lake)**:
   - Configured in the Fabric Lakehouse UI under **Manage Data Access**.
   - Ensures that whether users query via SQL Analytics Endpoint, PySpark Notebooks, or Direct Lake, identical security rules are enforced.
2. **Dynamic Data Masking (DDM)**:
   - Mask sensitive client contact numbers, deal margin percentages, or specific pricing formulas using SQL Masking functions in the Fabric SQL Analytics endpoint:
   ```sql
   ALTER TABLE gold_dim_solution_engineer 
   ALTER COLUMN hourly_cost_rate_usd ADD MASKED WITH (FUNCTION = 'default()');
   ```

---

## 🧪 4. Testing & Validation Checklist
1. In Power BI Desktop or Fabric Web Modeler, navigate to **Modeling** $\rightarrow$ **View as Roles**.
2. Select `Individual_SE_Access` and specify a test user email: `marcus.vance@enterprise-cloud.io`.
3. Verify that:
   - `[Total SE Hours]` only displays Marcus's hours.
   - `[Pre-Sales Influenced Won ACV]` filters exclusively to deals where Marcus was the primary SE.
   - Product list remains complete and accessible.
