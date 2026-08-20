import os
import subprocess
import random
import datetime
from datetime import timedelta

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

def make_commit(commit_datetime: datetime.datetime, message: str):
    iso_date = commit_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Update activity file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"Contribution timestamp: {iso_date} | {message}\n")
    
    # Stage file
    subprocess.run(["git", "add", LOG_FILE], check=True)
    
    # Set environment variables for backdating commit
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = iso_date
    env["GIT_COMMITTER_DATE"] = iso_date
    
    # Commit
    subprocess.run(
        ["git", "commit", "-m", message],
        env=env,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def run_backfill(start_date: datetime.date, end_date: datetime.date, min_commits: int = 1, max_commits: int = 3, skip_chance: float = 0.05):
    """
    Generate commits for each day between start_date and end_date.
    skip_chance: probability (0.0 - 1.0) of skipping a day to make the graph look natural.
    """
    total_days = (end_date - start_date).days + 1
    total_commits = 0
    
    print(f"[*] Starting backfill from {start_date} to {end_date} ({total_days} days)...")
    
    current_date = start_date
    while current_date <= end_date:
        # Occasionally skip a day for natural appearance
        if random.random() < skip_chance:
            current_date += timedelta(days=1)
            continue
        
        num_commits = random.randint(min_commits, max_commits)
        for _ in range(num_commits):
            # Random hour, minute, second during working/active hours (09:00 - 22:00)
            hour = random.randint(9, 22)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = datetime.datetime.combine(current_date, datetime.time(hour, minute, second))
            
            msg = random.choice(COMMIT_MESSAGES)
            make_commit(commit_time, msg)
            total_commits += 1
            
        current_date += timedelta(days=1)
    
    print(f"[+] Backfill complete! Total commits created: {total_commits}")
    print("[*] Don't forget to push to GitHub using: git push -u origin main (or your branch name)")

if __name__ == "__main__":
    # Inisialisasi git jika belum ada
    if not os.path.exists(".git"):
        print("[!] Inisialisasi Git repository...")
        subprocess.run(["git", "init"], check=True)
    
    print("==================================================")
    print("       GITHUB GREEN GRAPH BACKFILL GENERATOR      ")
    print("==================================================")
    print("Pilih opsi rentang waktu yang ingin di-hijaukan:")
    print("1. 1 Tahun Terakhir (365 Hari ke belakang)")
    print("2. 6 Bulan Terakhir")
    print("3. Dari awal tahun ini (1 Januari)")
    print("4. Custom Tanggal (YYYY-MM-DD)")
    
    choice = input("Pilihan (1/2/3/4) [default: 1]: ").strip() or "1"
    today = datetime.date.today()
    
    if choice == "1":
        start_date = today - timedelta(days=365)
        end_date = today
    elif choice == "2":
        start_date = today - timedelta(days=180)
        end_date = today
    elif choice == "3":
        start_date = datetime.date(today.year, 1, 1)
        end_date = today
    elif choice == "4":
        s_input = input("Masukkan tanggal mulai (YYYY-MM-DD): ").strip()
        e_input = input(f"Masukkan tanggal akhir (YYYY-MM-DD) [default: {today}]: ").strip() or str(today)
        start_date = datetime.datetime.strptime(s_input, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(e_input, "%Y-%m-%d").date()
    else:
        start_date = today - timedelta(days=365)
        end_date = today

    min_c = input("Jumlah commit minimal per hari [default: 1]: ").strip()
    min_c = int(min_c) if min_c.isdigit() else 1

    max_c = input("Jumlah commit maksimal per hari [default: 3]: ").strip()
    max_c = int(max_c) if max_c.isdigit() else 3

    run_backfill(start_date, end_date, min_commits=min_c, max_commits=max_c)
