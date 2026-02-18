# fastapi-backend-app



PART 1 — SQL CODING QUESTION (Real-world & tricky)
🎯 Scenario: Latest Status Per Customer

You have an order status history table.

Input Table: order_status
order_id	customer_id	status	status_time
1	101	Placed	2024-01-01 10:00
1	101	Shipped	2024-01-02 12:00
1	101	Delivered	2024-01-03 09:00
2	102	Placed	2024-01-05 14:00
2	102	Cancelled	2024-01-06 16:00
3	101	Placed	2024-01-07 11:00
❓ Question

👉 Write a SQL query to return the latest status per order.

✅ Expected Output
order_id	customer_id	latest_status	status_time
1	101	Delivered	2024-01-03 09:00
2	102	Cancelled	2024-01-06 16:00
3	101	Placed	2024-01-07 11:00
✅ Answer
SELECT order_id,
       customer_id,
       status AS latest_status,
       status_time
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY status_time DESC) AS rn
    FROM order_status
) t
WHERE rn = 1;


PART 2 — PYSPARK CODING QUESTION (Log processing)
🎯 Scenario: Web Server Logs
Input: log file
2024-01-01 10:00:01 INFO user=101 action=login
2024-01-01 10:05:10 INFO user=102 action=login
2024-01-01 10:06:22 ERROR user=101 action=payment_failed
2024-01-01 10:10:11 INFO user=101 action=logout
2024-01-01 10:15:45 ERROR user=103 action=timeout

❓ Question

👉 Using PySpark, produce a DataFrame showing:

user_id

total_actions

total_errors

✅ Expected Output
user_id	total_actions	total_errors
101	3	1
102	1	0
103	1	1
✅ Answer (PySpark)
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, when, count

spark = SparkSession.builder.getOrCreate()

# Load file
df = spark.read.text("logs.txt")

# Extract fields
parsed_df = df.select(
    regexp_extract("value", r"user=(\d+)", 1).alias("user_id"),
    regexp_extract("value", r"(INFO|ERROR)", 1).alias("log_level")
)

# Aggregate
result = parsed_df.groupBy("user_id").agg(
    count("*").alias("total_actions"),
    count(when(col("log_level") == "ERROR", True)).alias("total_errors")
)

result.show()


AWS TOOL-SPECIFIC VERIFICATION QUESTIONS
🟠 AWS GLUE (Most important)
❓ Q1: What are the 3 types of Glue jobs?
✅ Expected Answer

Spark (ETL) jobs

Python Shell jobs

Streaming jobs

👉 If they mention Ray jobs → bonus (new feature).

❓ Q2: What is the difference between DynamicFrame and DataFrame in Glue?
✅ Expected Answer
DynamicFrame	DataFrame
Glue abstraction	Spark native
Handles schema inconsistencies	Strict schema
Has built-in transformations like ResolveChoice	Requires manual handling

👉 If they can name ResolveChoice → strong signal.

❓ Q3: Where does Glue store table metadata?
✅ Expected Answer

AWS Glue Data Catalog.

❓ Q4: What happens when you run a Glue Crawler?
✅ Expected Answer

Scans data source (e.g., S3)

Infers schema

Creates/updates tables in Data Catalog

Detects partitions

❓ Q5: How does Glue read data from S3 internally?
✅ Expected Answer

Uses Spark readers via Hadoop S3 connector

Data read via s3:// or s3a://

🟠 AWS S3 (Data Engineering Critical)
❓ Q6: Difference between s3://, s3a://, and s3n://
✅ Expected Answer
Protocol	Status	Notes
s3://	legacy	not recommended
s3n://	deprecated	5GB limit
s3a://	current	high performance
❓ Q7: What is S3 consistency model?
✅ Expected Answer

Strong read-after-write for PUT

Strong consistency for overwrite & delete (modern S3)

Previously eventual → but now strong

👉 If they say "eventual consistency" → outdated knowledge.

❓ Q8: What is the max size of a single S3 object?
✅ Expected Answer

5 TB.

❓ Q9: Minimum size for multipart upload?
✅ Expected Answer

5 MB per part.

🟠 AWS ATHENA
❓ Q10: What engine does Athena use?
✅ Expected Answer

Presto / Trino.

❓ Q11: Where does Athena store query results?
✅ Expected Answer

S3 output location.

❓ Q12: Why does Athena require partition repair?
✅ Expected Answer

If partitions added manually to S3, must run:

MSCK REPAIR TABLE table_name;


to update metadata.

🟠 AWS DATA CATALOG
❓ Q13: Can Athena query data without Glue Data Catalog?
✅ Expected Answer

Yes — using inline schema (but rare).
Typically requires Data Catalog.

🟠 AWS REDSHIFT
❓ Q14: Difference between Redshift and Athena?
✅ Expected Answer
Redshift	Athena
Data warehouse	Query engine
Stores data	Queries S3
Columnar storage	Serverless
Requires cluster	No cluster
❓ Q15: What command loads data from S3 to Redshift?
✅ Expected Answer
COPY table_name
FROM 's3://bucket/path'
IAM_ROLE 'arn:aws:iam::account:role/role'
FORMAT AS PARQUET;

🟠 SNOWFLAKE ON AWS (From CV)
❓ Q16: What is Snowflake stage?
✅ Expected Answer

A staging location for loading/unloading data.

Types:

Internal stage

External stage (S3)

❓ Q17: What is Snowpipe?
✅ Expected Answer

Continuous data ingestion using event notifications.

🟠 AIRFLOW (from CV)
❓ Q18: What are the core components of an Airflow DAG?
✅ Expected Answer

DAG

Tasks

Operators

Scheduler

Executor

❓ Q19: What triggers a DAG?
✅ Expected Answer

Schedule interval

Manual trigger

External trigger/API

🟠 IAM (Hidden but critical)
❓ Q20: How does Glue access S3?
✅ Expected Answer

Using IAM Role attached to Glue job.
