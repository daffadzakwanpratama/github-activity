// State
const DAYS_NAME = [
  { id: 0, name: "Senin", short: "Sen" },
  { id: 1, name: "Selasa", short: "Sel" },
  { id: 2, name: "Rabu", short: "Rab" },
  { id: 3, name: "Kamis", short: "Kam" },
  { id: 4, name: "Jumat", short: "Jum" },
  { id: 5, name: "Sabtu", short: "Sab" },
  { id: 6, name: "Minggu", short: "Min" }
];

let currentConfig = {
  scheduled_off_days: [4, 5],
  random_skip_chance: 0.15,
  peak_day_chance: 0.20,
  min_commits: 1,
  max_commits: 3,
  working_hours: { start: 9, end: 22 },
  commit_messages: []
};

// Elements
const daysSelector = document.getElementById("days-selector");
const inputRandomSkip = document.getElementById("input-random-skip");
const valRandomSkip = document.getElementById("val-random-skip");
const inputPeakDay = document.getElementById("input-peak-day");
const valPeakDay = document.getElementById("val-peak-day");
const inputMinCommit = document.getElementById("input-min-commit");
const inputMaxCommit = document.getElementById("input-max-commit");
const inputHourStart = document.getElementById("input-hour-start");
const inputHourEnd = document.getElementById("input-hour-end");
const commitMessagesList = document.getElementById("commit-messages-list");
const inputNewMsg = document.getElementById("input-new-msg");
const btnAddMsg = document.getElementById("btn-add-msg");
const heatmapGrid = document.getElementById("heatmap-grid");
const btnRefreshSim = document.getElementById("btn-refresh-sim");
const btnSaveTop = document.getElementById("btn-save-top");
const statTodayDay = document.getElementById("stat-today-day");
const statTodayStatus = document.getElementById("stat-today-status");
const btnRunToday = document.getElementById("btn-run-today");
const btnForceToday = document.getElementById("btn-force-today");
const backfillStart = document.getElementById("backfill-start");
const backfillEnd = document.getElementById("backfill-end");
const btnRunBackfill = document.getElementById("btn-run-backfill");
const btnGitPush = document.getElementById("btn-git-push");
const consoleBox = document.getElementById("console-box");

// Logger helper
function appendLog(msg, type = "normal") {
  const line = document.createElement("div");
  line.textContent = msg;
  if (type === "error") line.className = "log-err";
  if (type === "info") line.className = "log-info";
  consoleBox.appendChild(line);
  consoleBox.scrollTop = consoleBox.scrollHeight;
}

// Toast helper
function showToast(msg, isSuccess = true) {
  const toast = document.getElementById("toast");
  const toastMsg = document.getElementById("toast-msg");
  const toastIcon = document.getElementById("toast-icon");
  toastMsg.textContent = msg;
  toastIcon.textContent = isSuccess ? "✅" : "⚠️";
  toast.className = "show";
  setTimeout(() => {
    toast.className = "";
  }, 3500);
}

// Render Days Selector
function renderDaysSelector() {
  daysSelector.innerHTML = "";
  DAYS_NAME.forEach(day => {
    const isOff = currentConfig.scheduled_off_days.includes(day.id);
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `day-btn ${isOff ? "active-off" : "active-work"}`;
    btn.innerHTML = `
      <span>${day.name}</span>
      <span class="day-status">${isOff ? "Libur" : "Aktif"}</span>
    `;
    btn.addEventListener("click", () => {
      toggleDayOff(day.id);
    });
    daysSelector.appendChild(btn);
  });
  updateTodayStats();
  renderHeatmap();
}

function toggleDayOff(dayId) {
  const idx = currentConfig.scheduled_off_days.indexOf(dayId);
  if (idx > -1) {
    currentConfig.scheduled_off_days.splice(idx, 1);
  } else {
    currentConfig.scheduled_off_days.push(dayId);
  }
  renderDaysSelector();
}

// Render Commit Message Tags
function renderCommitMessages() {
  commitMessagesList.innerHTML = "";
  (currentConfig.commit_messages || []).forEach((msg, idx) => {
    const tag = document.createElement("div");
    tag.className = "tag-item";
    tag.innerHTML = `
      <span>${msg}</span>
      <span class="del-tag" title="Hapus pesan">&times;</span>
    `;
    tag.querySelector(".del-tag").addEventListener("click", () => {
      currentConfig.commit_messages.splice(idx, 1);
      renderCommitMessages();
    });
    commitMessagesList.appendChild(tag);
  });
}

// Update Today Status
function updateTodayStats() {
  const now = new Date();
  // JS getDay(): 0=Sunday, 1=Monday, ..., 6=Saturday
  // Convert to Python weekday: 0=Monday, ..., 6=Sunday
  const jsDay = now.getDay();
  const pyWeekday = (jsDay === 0) ? 6 : jsDay - 1;
  
  const dayObj = DAYS_NAME.find(d => d.id === pyWeekday);
  statTodayDay.textContent = dayObj ? dayObj.name : "Hari Ini";
  
  const isScheduledOff = currentConfig.scheduled_off_days.includes(pyWeekday);
  if (isScheduledOff) {
    statTodayStatus.textContent = "Libur";
    statTodayStatus.style.color = "var(--accent-red)";
  } else {
    statTodayStatus.textContent = "Aktif";
    statTodayStatus.style.color = "var(--accent-green)";
  }
}

// Live Heatmap Simulator
function renderHeatmap() {
  heatmapGrid.innerHTML = "";
  const totalWeeks = 30;
  const daysCount = totalWeeks * 7;
  const skipChance = currentConfig.random_skip_chance;
  const peakChance = currentConfig.peak_day_chance;
  const offDays = currentConfig.scheduled_off_days;

  for (let i = 0; i < daysCount; i++) {
    const dayOfWeek = i % 7;
    const isScheduledOff = offDays.includes(dayOfWeek);
    const cell = document.createElement("div");
    cell.className = "heatmap-cell";

    if (isScheduledOff) {
      cell.classList.add("off-day");
      cell.title = `Libur Terjadwal (${DAYS_NAME[dayOfWeek].name})`;
    } else if (Math.random() < skipChance) {
      cell.classList.add("level-0");
      cell.title = `Libur Acak / Istirahat (${DAYS_NAME[dayOfWeek].name})`;
    } else {
      const isPeak = Math.random() < peakChance;
      if (isPeak) {
        cell.classList.add("level-4");
        cell.title = `Peak Day (5-8 Commits)`;
      } else {
        const randLevel = Math.floor(Math.random() * 3) + 1; // level 1, 2, 3
        cell.classList.add(`level-${randLevel}`);
        cell.title = `Hari Aktif (${currentConfig.min_commits} - ${currentConfig.max_commits} commits)`;
      }
    }

    heatmapGrid.appendChild(cell);
  }
}

// Load Config from Server
async function loadConfig() {
  try {
    const res = await fetch("/api/config");
    if (res.ok) {
      const data = await res.json();
      currentConfig = data;
      
      // Update UI Inputs
      inputRandomSkip.value = Math.round((currentConfig.random_skip_chance || 0.15) * 100);
      valRandomSkip.textContent = `${inputRandomSkip.value}%`;
      
      inputPeakDay.value = Math.round((currentConfig.peak_day_chance || 0.20) * 100);
      valPeakDay.textContent = `${inputPeakDay.value}%`;
      
      inputMinCommit.value = currentConfig.min_commits || 1;
      inputMaxCommit.value = currentConfig.max_commits || 3;
      
      inputHourStart.value = currentConfig.working_hours?.start || 9;
      inputHourEnd.value = currentConfig.working_hours?.end || 22;
      
      renderDaysSelector();
      renderCommitMessages();
      appendLog("[✓] Konfigurasi berhasil dimuat dari server.", "info");
    }
  } catch (err) {
    appendLog("[!] Gagal memuat konfigurasi dari server: " + err.message, "error");
  }
}

// Save Config to Server
async function saveConfig() {
  currentConfig.random_skip_chance = parseFloat(inputRandomSkip.value) / 100;
  currentConfig.peak_day_chance = parseFloat(inputPeakDay.value) / 100;
  currentConfig.min_commits = parseInt(inputMinCommit.value) || 1;
  currentConfig.max_commits = parseInt(inputMaxCommit.value) || 3;
  currentConfig.working_hours = {
    start: parseInt(inputHourStart.value) || 9,
    end: parseInt(inputHourEnd.value) || 22
  };

  try {
    const res = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(currentConfig, null, 2)
    });
    
    if (res.ok) {
      showToast("Pengaturan berhasil disimpan ke config.json!");
      appendLog("[✓] Pengaturan berhasil disimpan.", "info");
      renderHeatmap();
    } else {
      throw new Error("Respon server gagal");
    }
  } catch (err) {
    showToast("Gagal menyimpan pengaturan: " + err.message, false);
    appendLog("[!] Gagal menyimpan: " + err.message, "error");
  }
}

// Event Listeners
inputRandomSkip.addEventListener("input", (e) => {
  valRandomSkip.textContent = `${e.target.value}%`;
  currentConfig.random_skip_chance = parseFloat(e.target.value) / 100;
  renderHeatmap();
});

inputPeakDay.addEventListener("input", (e) => {
  valPeakDay.textContent = `${e.target.value}%`;
  currentConfig.peak_day_chance = parseFloat(e.target.value) / 100;
  renderHeatmap();
});

inputMinCommit.addEventListener("change", () => renderHeatmap());
inputMaxCommit.addEventListener("change", () => renderHeatmap());

btnAddMsg.addEventListener("click", () => {
  const text = inputNewMsg.value.trim();
  if (text) {
    if (!currentConfig.commit_messages) currentConfig.commit_messages = [];
    currentConfig.commit_messages.push(text);
    inputNewMsg.value = "";
    renderCommitMessages();
  }
});

inputNewMsg.addEventListener("keydown", (e) => {
  if (e.key === "Enter") btnAddMsg.click();
});

btnRefreshSim.addEventListener("click", () => renderHeatmap());
btnSaveTop.addEventListener("click", () => saveConfig());

// Run Daily Test
btnRunToday.addEventListener("click", async () => {
  appendLog("[*] Menjalankan test daily commit...", "info");
  try {
    const res = await fetch("/api/run-daily", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ force: false })
    });
    const data = await res.json();
    appendLog(data.output || data.message);
  } catch (err) {
    appendLog("[!] Error: " + err.message, "error");
  }
});

// Force Daily Commit
btnForceToday.addEventListener("click", async () => {
  if (!confirm("Apakah Anda yakin ingin memaksakan commit hari ini (mengabaikan aturan libur)?")) return;
  appendLog("[*] Menjalankan forced daily commit (bypass libur)...", "info");
  try {
    const res = await fetch("/api/run-daily", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ force: true })
    });
    const data = await res.json();
    appendLog(data.output || data.message);
  } catch (err) {
    appendLog("[!] Error: " + err.message, "error");
  }
});

// Run Backfill
btnRunBackfill.addEventListener("click", async () => {
  const start = backfillStart.value;
  const end = backfillEnd.value;
  if (!start || !end) {
    alert("Silakan pilih tanggal mulai dan tanggal akhir terlebih dahulu!");
    return;
  }
  
  if (!confirm(`Jalankan backfill kontribusi dari ${start} sampai ${end}?`)) return;
  
  appendLog(`[*] Memulai proses backfill dari ${start} s/d ${end}...`, "info");
  try {
    const res = await fetch("/api/run-backfill", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        start_date: start,
        end_date: end
      })
    });
    const data = await res.json();
    appendLog(data.output || data.message);
  } catch (err) {
    appendLog("[!] Error backfill: " + err.message, "error");
  }
});

// Git Push
btnGitPush.addEventListener("click", async () => {
  appendLog("[*] Melakukan git push ke remote repository...", "info");
  try {
    const res = await fetch("/api/git-push", { method: "POST" });
    const data = await res.json();
    appendLog(data.output || data.message);
  } catch (err) {
    appendLog("[!] Push error: " + err.message, "error");
  }
});

// Default Date Pickers for Backfill
function initDates() {
  const today = new Date();
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(today.getDate() - 30);
  
  backfillEnd.value = today.toISOString().split("T")[0];
  backfillStart.value = thirtyDaysAgo.toISOString().split("T")[0];
}

// Initial Load
initDates();
loadConfig();
