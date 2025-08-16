
# ETL Streaming Pipeline with PostgreSQL and Power BI

## Project Overview
This project implements a simple ETL (Extract, Transform, Load) streaming pipeline using Python, PostgreSQL, and Power BI.  
It simulates event data, stores raw events in PostgreSQL, processes them into an aggregated form, and makes them available for visualization.

---

## Folder Structure
```
etl_project/
│
├── data_generator.py        # Simulates random events and writes to CSV
├── extract_to_postgres.py   # Extracts CSV into PostgreSQL (raw_events)
├── transformer.py           # Cleans & aggregates raw_events → processed_events
├── analytics.py             # Runs queries on processed_events
├── main.py                  # Orchestrates generator + extractor + transformer
└── README.md                # Documentation
```

---

## PostgreSQL Setup

1. **Login to PostgreSQL**
```sql
psql -U postgres
```

2. **Create Database**
```sql
CREATE DATABASE etl_streaming;
\c etl_streaming;
```

3. **Create Tables**

```sql
-- Raw events table
CREATE TABLE IF NOT EXISTS raw_events (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Processed events table
CREATE TABLE IF NOT EXISTS processed_events (
    event_type VARCHAR(50) PRIMARY KEY,
    event_count INT NOT NULL
);

-- Ensure uniqueness for upserts
CREATE UNIQUE INDEX IF NOT EXISTS idx_processed_event_type
ON processed_events(event_type);
```

---

## Pipeline Flow
1. **`data_generator.py`**  
   Generates random user events → writes to `events.csv`.

2. **`extract_to_postgres.py`**  
   Reads `events.csv` → inserts rows into PostgreSQL `raw_events`.

3. **`transformer.py`**  
   Aggregates data (`COUNT(*) GROUP BY event_type`) → stores results in `processed_events`.

4. **`analytics.py`**  
   Runs queries (e.g., top events) on `processed_events`.

5. **`main.py`**  
   Orchestrates all steps continuously with scheduling/threading.

6. **Power BI**  
   Connects to PostgreSQL → pulls from `processed_events` for live dashboards.

---

## How to Run

1. Activate your Python environment
```sh
.env\Scriptsctivate    # Windows
source venv/bin/activate   # Linux/Mac
```

2. Run pipeline
```sh
python main.py
```

3. Verify tables in PostgreSQL
```sql
SELECT * FROM raw_events LIMIT 5;
SELECT * FROM processed_events;
```

---

## Common Pitfalls & Fixes
- **psycopg2 not found** → install with `pip install psycopg2-binary`
- **raw_event vs raw_events mismatch** → ensure all scripts use `raw_events`
- **processed_events counts always = 1** → fix GROUP BY aggregation
- **threading issues** → test scripts standalone before orchestration
- **Power BI connection** → use **PostgreSQL connector**, not CSV

---

## Next Steps / Extensions
- Add Kafka for real streaming
- Store data in a Data Lake (Parquet/Delta)
- Automate refresh in Power BI
- Containerize with Docker

---




# Connecting PostgreSQL Database with Power BI and Visualization

## Step 1: Install Required Components

1.  Install **Power BI Desktop**.
2.  Ensure PostgreSQL is installed and running.
3.  Install the **Npgsql PostgreSQL ODBC driver** (Power BI uses this to
    connect).

------------------------------------------------------------------------

## Step 2: Prepare PostgreSQL Database

1.  Start PostgreSQL and create a database if not already available.

    ``` sql
    CREATE DATABASE etl_streaming;
    ```

2.  Create tables and insert data as part of ETL pipeline
    (`extract_to_postgres.py` and `transformer.py` handle this).

------------------------------------------------------------------------

## Step 3: Connect Power BI to PostgreSQL

1.  Open **Power BI Desktop**.
2.  Go to **Home → Get Data → Database → PostgreSQL Database**.
3.  Enter the following details:
    -   **Server**: `localhost` (or remote server IP)
    -   **Database**: `etl_streaming`
    -   **Username**: your PostgreSQL username
    -   **Password**: your PostgreSQL password
4.  Select **DirectQuery** for live streaming or **Import** for batch
    data.
5.  Load the data.

------------------------------------------------------------------------

## Step 4: Data Transformation in Power BI

1.  Use **Power Query Editor** to clean and shape data.
2.  Merge multiple tables (if required).
3.  Create calculated columns or measures using **DAX**.

------------------------------------------------------------------------

## Step 5: Create Visualizations

1.  Open **Report View** in Power BI.
2.  Drag fields from PostgreSQL tables to the canvas.
3.  Example visualizations:
    -   **Line Chart**: Events over time.
    -   **Bar Chart**: Event counts by category.
    -   **Pie Chart**: Proportional distribution of event types.
    -   **Table**: Detailed event logs.
4.  Add **Filters** and **Slicers** for interactive dashboards.

------------------------------------------------------------------------

## Step 6: Schedule Refresh (Optional)

1.  Publish the report to **Power BI Service**.
2.  Go to **Dataset Settings** → Enable **Scheduled Refresh**.
3.  Power BI will fetch new data from PostgreSQL at defined intervals.

------------------------------------------------------------------------

## Step 7: Share Dashboard

1.  Publish the dashboard to Power BI Service.
2.  Share with team members or embed in applications.

------------------------------------------------------------------------

## Summary

-   **ETL Scripts** insert and transform data in PostgreSQL.\
-   **Power BI** connects directly to PostgreSQL using Npgsql.\
-   Data is visualized in charts, tables, and dashboards.\
-   Dashboards can be refreshed automatically and shared across teams.
