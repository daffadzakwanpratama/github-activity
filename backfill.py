import os
import subprocess
import random
import datetime
from datetime import timedelta
import json

CONFIG_FILE = "config.json"
LOG_FILE = "activity.txt"

DEFAULT_CONFIG = {
    "scheduled_off_days": [4, 5],
    "random_skip_chance": 0.15,
    "peak_day_chance": 0.20,
    "min_commits": 1,
    "max_commits": 3,
    "working_hours": {"start": 9, "end": 22},
    "commit_messages": [
        "chore: update daily activity log",
        "docs: sync routine progress",
        "feat: record metric logs",
        "refactor: optimize data points",
        "chore: routine healthcheck and log update",
        "docs: update maintenance timestamp",
        "feat: add daily workspace telemetry",
        "perf: sync local cache index"
    ]
}

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                return config
        except Exception as e:
            print(f"[!] Gagal membaca {CONFIG_FILE}, memakai default. Error: {e}")
    return DEFAULT_CONFIG

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

def run_backfill(
    start_date: datetime.date, 
    end_date: datetime.date, 
    min_commits: int = None, 
    max_commits: int = None, 
    skip_chance: float = None,
    scheduled_off_days: list[int] = None,
    log_callback = None
):
    """
    Generate commits for each day between start_date and end_date.
    """
    config = load_config()
    
    if min_commits is None:
        min_commits = config.get("min_commits", 1)
    if max_commits is None:
        max_commits = config.get("max_commits", 3)
    if skip_chance is None:
        skip_chance = config.get("random_skip_chance", 0.15)
    if scheduled_off_days is None:
        scheduled_off_days = config.get("scheduled_off_days", [4, 5])
        
    peak_chance = config.get("peak_day_chance", 0.20)
    messages = config.get("commit_messages", DEFAULT_CONFIG["commit_messages"])
    work_hours = config.get("working_hours", {"start": 9, "end": 22})
    h_start = work_hours.get("start", 9)
    h_end = work_hours.get("end", 22)

    total_days = (end_date - start_date).days + 1
    total_commits = 0
    total_off_days = 0
    
    def log(msg):
        print(msg)
        if log_callback:
            log_callback(msg)

    log(f"[*] Starting backfill from {start_date} to {end_date} ({total_days} hari)...")
    log(f"[*] Libur terjadwal: {scheduled_off_days}, Peluang libur acak: {int(skip_chance*100)}%")
    
    current_date = start_date
    while current_date <= end_date:
        # 1. Cek Libur Terjadwal
        if current_date.weekday() in scheduled_off_days:
            total_off_days += 1
            current_date += timedelta(days=1)
            continue
            
        # 2. Cek Libur Acak (Random Skip)
        if random.random() < skip_chance:
            total_off_days += 1
            current_date += timedelta(days=1)
            continue
        
        is_peak = random.random() < peak_chance
        num_commits = random.randint(5, 8) if is_peak else random.randint(min_commits, max_commits)
        
        for _ in range(num_commits):
            hour = random.randint(min(h_start, h_end), max(h_start, h_end))
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = datetime.datetime.combine(current_date, datetime.time(hour, minute, second))
            
            msg = random.choice(messages)
            make_commit(commit_time, msg)
            total_commits += 1
            
        current_date += timedelta(days=1)
    
    log(f"[+] Backfill selesai!")
    log(f"    - Total commit dibuat: {total_commits}")
    log(f"    - Total hari libur: {total_off_days} hari")
    log("[*] Jangan lupa push ke GitHub: git push -u origin main")
    return {"total_commits": total_commits, "total_off_days": total_off_days}

if __name__ == "__main__":
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

    run_backfill(start_date, end_date)
