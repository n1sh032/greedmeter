from datetime import datetime

LOG_FILE = "activity.log"

def log(message):
    timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")