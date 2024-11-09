import subprocess
import threading
import time
import os

def start_spider(spider_name):
    """Starts the Scrapy spider by name and logs the output in real-time."""
    log_file_path = f"{spider_name}.log"

    # Start the spider process
    spider_process = subprocess.Popen(
        ["scrapy", "crawl", spider_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    print(f"Spider '{spider_name}' started. Logs will be monitored.")

    # Write logs to a file and monitor in real-time
    with open(log_file_path, "w") as log_file:
        for line in iter(spider_process.stdout.readline, ""):
            log_file.write(line)
            log_file.flush()
            print(line, end="")

    # Wait for the spider process to complete
    spider_process.wait()
    print(f"Spider '{spider_name}' has completed.")


def monitor_logs(spider_name):
    """Monitors the logs produced by the active spider."""
    log_file_path = f"{spider_name}.log"

    if not os.path.exists(log_file_path):
        print(f"Log file for '{spider_name}' not found.")
        return

    print(f"Monitoring logs for spider '{spider_name}'...")
    with open(log_file_path, "r") as log_file:
        # Continuously read new lines from the log file
        while True:
            where = log_file.tell()
            line = log_file.readline()
            if not line:
                time.sleep(1)  # Wait for new lines
                log_file.seek(where)
            else:
                # Print or handle the log line
                print(f"[LOG] {line.strip()}")
                # Add logic to detect specific conditions (e.g., 429 or 403 errors)
                if "429" in line or "403" in line:
                    print("Warning: Detected 429 or 403 error in logs.")
                    # Additional logic can be implemented here, such as pausing or stopping the spider

if __name__ == "__main__":
    spider_name = input("Enter the name of the spider to start: ")

    # Start the spider in a separate thread
    spider_thread = threading.Thread(target=start_spider, args=(spider_name,))
    spider_thread.start()

    # Monitor logs in the main thread
    monitor_logs(spider_name)

    # Wait for the spider thread to finish
    spider_thread.join()
