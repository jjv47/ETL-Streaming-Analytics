import random
from datetime import datetime
import time


# Step 1: Define possible values for each field
USER_IDS = list(range(1, 10))  # 1000 users
EVENT_TYPES = ["app_open", "play", "pause", "like", "dislike", "logout"]
COUNTRIES = ["India", "USA", "UK", "Germany", "Australia"]
DEVICE_TYPES = ["Android", "iOS", "Web"]
APP_VERSIONS = ["1.0", "1.1", "1.2", "2.0"]

# Step 2: Function to create a single event record
def generate_event():
    return {
        "user_id": random.choice(USER_IDS),
        "event_type": random.choice(EVENT_TYPES),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "country": random.choice(COUNTRIES),
        "device_type": random.choice(DEVICE_TYPES),
        "app_version": random.choice(APP_VERSIONS)
    }

# Step 3: If run directly, keep generating events
if __name__ == "__main__":
    while True:
        event = generate_event()
        print(event)
        time.sleep(1)  # 1 second between events
