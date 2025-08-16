import psycopg2
from psycopg2 import sql
import time
from data_generator import generate_event
from config import DB_CONFIG

# Step 1: Database connection parameters

# Step 2: Function to insert event into Postgres
def insert_event(event):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    

    insert_query = sql.SQL("""
        INSERT INTO raw_events (user_id, event_type, timestamp, country, device_type, app_version)
        VALUES (%s, %s, %s, %s, %s, %s)
    """)

    cur.execute(insert_query, (
        event["user_id"],
        event["event_type"],
        event["timestamp"],
        event["country"],
        event["device_type"],
        event["app_version"]
    ))

    conn.commit()
    cur.close()
    conn.close()

# Step 3: Main loop to generate & insert events
if __name__ == "__main__":
    while True:
        event = generate_event()
        insert_event(event)
        print(f"Inserted event: {event}")
        time.sleep(1)  # 1 second delay
