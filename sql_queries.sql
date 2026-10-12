-- Customer Churn Analysis SQL examples
SELECT COUNT(DISTINCT customerid) AS total_customers FROM db_customer;

SELECT COUNT(*) AS total_subscriptions,
       SUM(CASE WHEN cancellation_date IS NOT NULL THEN 1 ELSE 0 END) AS churned_customers,
       ROUND(100.0 * SUM(CASE WHEN cancellation_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM db_subscription;

SELECT contract_type, COUNT(*) AS customers,
       ROUND(100.0 * SUM(CASE WHEN cancellation_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM db_subscription GROUP BY contract_type ORDER BY churn_rate_pct DESC;

SELECT plan_type, COUNT(*) AS customers,
       ROUND(100.0 * SUM(CASE WHEN cancellation_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM db_subscription GROUP BY plan_type ORDER BY churn_rate_pct DESC;

SELECT cancellation_reason, COUNT(*) AS churned_customers
FROM db_subscription WHERE cancellation_date IS NOT NULL
GROUP BY cancellation_reason ORDER BY churned_customers DESC;
