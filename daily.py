import os
import subprocess
import random
import datetime
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
    """Memuat konfigurasi dari config.json atau memakai default jika file belum ada."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Merge dengan default jika ada key baru
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                return config
        except Exception as e:
            print(f"[!] Gagal membaca {CONFIG_FILE}, memakai konfigurasi default. Error: {e}")
    return DEFAULT_CONFIG

def is_today_off(now: datetime.datetime, config: dict) -> tuple[bool, str]:
    """Mengecek apakah hari ini adalah hari libur (terjadwal atau acak)."""
    day_name = now.strftime("%A")
    day_index = now.weekday()
    
    scheduled_days = config.get("scheduled_off_days", [4, 5])
    random_skip = config.get("random_skip_chance", 0.15)
    
    # 1. Cek Libur Terjadwal (Fixed Schedule)
    if day_index in scheduled_days:
        return True, f"Libur terjadwal ({day_name})"
        
    # 2. Cek Libur Acak (Random Day Off)
    if random.random() < random_skip:
        return True, f"Libur acak / istirahat santai ({day_name})"
        
    return False, ""

def make_daily_commits(force: bool = False):
    """
    Menjalankan proses commit harian berdasarkan konfigurasi.
    force: jika True, bypass cek libur (untuk testing).
    """
    config = load_config()
    now = datetime.datetime.now()
    
    if not force:
        is_off, reason = is_today_off(now, config)
        if is_off:
            print(f"[*] [HARI LIBUR] {reason} pada {now.strftime('%Y-%m-%d')}. Tidak ada commit yang dibuat.")
            return

    peak_chance = config.get("peak_day_chance", 0.20)
    is_peak_day = random.random() < peak_chance
    
    min_c = config.get("min_commits", 1)
    max_c = config.get("max_commits", 3)
    messages = config.get("commit_messages", DEFAULT_CONFIG["commit_messages"])
    
    if is_peak_day:
        num_commits = random.randint(5, 8)
        print(f"[*] [PEAK DAY] Hari ini diset sebagai hari aktivitas tinggi ({num_commits} commits)")
    else:
        num_commits = random.randint(min_c, max_c)
    
    print(f"[*] Menjalankan {num_commits} commit untuk hari ini: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    for i in range(num_commits):
        current_time = datetime.datetime.now()
        iso_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
        msg = f"{random.choice(messages)} #{i+1}"
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{iso_date}] {msg}\n")
            
        subprocess.run(["git", "add", LOG_FILE], check=True)
        subprocess.run(["git", "commit", "-m", msg], check=True)
        print(f"  [+] Commit {i+1}/{num_commits}: {msg}")

if __name__ == "__main__":
    make_daily_commits()
