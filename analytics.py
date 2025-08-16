import psycopg2
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def run_analytics_queries():
    conn = get_connection()
    cur = conn.cursor()

    # Query 1: Total events per country (aggregated)
    cur.execute("""
        SELECT country, SUM(total_events) AS grand_total
        FROM processed_events
        GROUP BY country
        ORDER BY grand_total DESC;
    """)
    results = cur.fetchall()
    print("Total events by country:")
    for row in results:
        print(row)

    # Query 2: Total events per event_type
    cur.execute("""
        SELECT event_type, SUM(total_events) AS grand_total
        FROM processed_events
        GROUP BY event_type
        ORDER BY grand_total DESC;
    """)
    results = cur.fetchall()
    print("\nTotal events by event_type:")
    for row in results:
        print(row)

    # Add more if needed, e.g., by date or user_id

    cur.close()
    conn.close()

if __name__ == "__main__":
    run_analytics_queries()