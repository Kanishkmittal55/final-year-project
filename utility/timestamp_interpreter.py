from datetime import datetime

# Given timestamp in milliseconds
timestamp_ms = 1729329880680

# Convert milliseconds to seconds
timestamp_seconds = timestamp_ms / 1000

# Convert to human-readable format
expiration_time = datetime.utcfromtimestamp(timestamp_seconds)

print("Session expires on:", expiration_time)