import os
import subprocess
import random
import datetime

LOG_FILE = "activity.txt"

COMMIT_MESSAGES = [
    "chore: update daily activity log",
    "docs: sync routine progress",
    "feat: record metric logs",
    "refactor: optimize data points",
    "chore: routine healthcheck and log update",
    "docs: update maintenance timestamp",
    "feat: add daily workspace telemetry",
    "perf: sync local cache index"
]

def make_daily_commits(min_commits: int = 1, max_commits: int = 3):
    now = datetime.datetime.now()
    
    # 20% kemungkinan menjadi "Peak Day" (hari produktif tinggi dengan hijau lebih terang 5-8 commit)
    is_peak_day = random.random() < 0.20
    if is_peak_day:
        num_commits = random.randint(5, 8)
        print(f"[*] [PEAK DAY] Hari ini diset sebagai hari aktivitas tinggi ({num_commits} commits)")
    else:
        num_commits = random.randint(min_commits, max_commits)
    
    print(f"[*] Menjalankan {num_commits} commit untuk hari ini: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    for i in range(num_commits):
        current_time = datetime.datetime.now()
        iso_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
        msg = f"{random.choice(COMMIT_MESSAGES)} #{i+1}"
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{iso_date}] {msg}\n")
            
        subprocess.run(["git", "add", LOG_FILE], check=True)
        subprocess.run(["git", "commit", "-m", msg], check=True)
        print(f"  [+] Commit {i+1}/{num_commits}: {msg}")

if __name__ == "__main__":
    make_daily_commits(1, 3)
