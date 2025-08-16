import subprocess
import time
import threading
import schedule
import os
import sys

# Get the path to the virtual environment's Python interpreter
venv_python = sys.executable
def run_extract_process():
    # Run extract_to_postgres.py in a separate thread for continuous event generation/insertion
    def extract_thread():
        while True:
            subprocess.run([venv_python, "extract_to_postgres.py"])
            time.sleep(1)  # Respect the 1-second delay from original script

    extract_thread = threading.Thread(target=extract_thread, daemon=True)
    extract_thread.start()

def run_transform_process():
    # Run transformer.py periodically to aggregate and update processed_events
    def transform_job():
        subprocess.run([venv_python, "transformer.py"])
        print(f"Transformed data at {time.strftime('%H:%M:%S', time.localtime())}")

    # Schedule transformation every 30 seconds
    schedule.every(30).seconds.do(transform_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
    print(f"Starting ETL pipeline simulation at {time.strftime('%H:%M:%S', time.localtime())}")
    # Start extract process in background
    run_extract_process()
    # Start transform process in main thread with scheduling
    run_transform_process()
    
    # Keep the main thread alive
    while True:
        time.sleep(1)
