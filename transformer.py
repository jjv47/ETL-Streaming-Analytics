import psycopg2
from config import DB_CONFIG

# Step 1: Connect to Postgres
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# Step 2: Create processed_events table
def create_processed_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS processed_events (
            event_id SERIAL PRIMARY KEY,
            user_id INT,
            event_type VARCHAR(50),
            event_date DATE,
            country VARCHAR(50),
            device_type VARCHAR(50),
            app_version VARCHAR(20),
            total_events INT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Step 3: Transform & aggregate data from raw_events
def transform_data():
    conn = get_connection()
    cur = conn.cursor()

    # Remove duplicates & group data
    cur.execute("""
        INSERT INTO processed_events (user_id, event_type, event_date, country, device_type, app_version, total_events)
        SELECT
            user_id,
            event_type,
            DATE(timestamp) AS event_date,
            country,
            device_type,
            app_version,
            COUNT(event_type) AS total_events
        FROM raw_events
        WHERE timestamp IS NOT NULL
        GROUP BY user_id, event_type, event_date, country, device_type, app_version 
        ON CONFLICT DO NOTHING;
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_processed_table()
    transform_data()
    print("Transformation complete. Data moved to processed_events.")
