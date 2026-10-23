-- Microsoft Fabric SQL Analytics Endpoint: 03_row_level_security.sql
-- Dynamic Row-Level Security (RLS) Implementation for Regional Directors and Sales Reps

CREATE SCHEMA Security;
GO

-- 1. Security Predicate Function
CREATE OR ALTER FUNCTION Security.fn_SalesSecurityPredicate(@RegionCode VARCHAR(20))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS fn_securitypredicate_result
WHERE 
    -- Allow Global Admins and Sales VPs full visibility
    IS_ROLEMEMBER('SalesExecutiveAdmins') = 1
    OR 
    -- Filter according to authenticated Fabric user's assigned region
    @RegionCode = CASE 
        WHEN USER_NAME() = 'david.vance@company.com' THEN 'NA'
        WHEN USER_NAME() = 'klaus.richter@company.com' THEN 'EMEA'
        WHEN USER_NAME() = 'mei.lin@company.com' THEN 'APAC'
        ELSE 'PUBLIC'
    END;
GO

-- 2. Security Policy on Store Region Dimension
CREATE SECURITY POLICY Security.SalesFilterPolicy
ADD FILTER PREDICATE Security.fn_SalesSecurityPredicate(RegionCode)
ON dbo.v_dim_store_region
WITH (STATE = ON);
GO
