# 🌿 GitHub Contribution Auto-Bot & Web Dashboard

Sistem otomatisasi dan generator kontribusi GitHub modern dengan **Web Dashboard visual** untuk mengatur jadwal libur (seperti Jumat & Sabtu), peluang libur acak, frekuensi commit harian, serta backfill riwayat masa lalu.

---

## 🎛️ Cara Membuka Web Dashboard Pengaturan

Kamu bisa mengatur seluruh jadwal dan melakukan commit secara visual lewat browser:

1. Klik ganda (double-click) file **[`buka_dashboard.bat`](buka_dashboard.bat)**  
   *atau buka terminal dan jalankan `python app.py`*.
2. Browser akan terbuka otomatis di **`http://localhost:5000`**.
3. Di Dashboard kamu bisa:
   - **Memilih Hari Libur Terjadwal**: Klik tombol hari (misal Jumat & Sabtu libur).
   - **Mengatur Peluang Libur Acak**: Slider 0%–100% agar kontribusi terlihat sangat alami layaknya manusia.
   - **Peluang Peak Day**: Mengatur frekuensi hari super produktif (5–8 commits).
   - **Simulasi Grafik Hijau (Live Heatmap)**: Melihat simulasi visual kontribusi GitHub secara realtime.
   - **Test Commit & Backfill**: Menjalankan commit hari ini atau backfill tanggal masa lalu langsung dari browser.
   - **Simpan Pengaturan**: Langsung tersimpan ke `config.json` dan otomatis dipakai oleh GitHub Actions.

---

## 📁 Struktur File

- **`buka_dashboard.bat`**: Shortcut Windows sekali klik untuk membuka Web Dashboard.
- **`app.py`**: Server backend dashboard lokal (zero-dependency, tanpa perlu `pip install`).
- **`web/`**: Tampilan visual antarmuka dashboard (HTML, CSS, JS modern & responsif).
- **`config.json`**: File pengaturan terpusat (hari libur, probabilitas, rentang commit).
- **`daily.py`**: Script yang membuat commit harian berdasarkan `config.json`.
- **`backfill.py`**: Script generator riwayat commit masa lalu.
- **`.github/workflows/auto-commit.yml`**: GitHub Action otomatis yang berjalan setiap hari di cloud.
- **`activity.txt`**: File log rekaman kontribusi.

---

## 🚀 Panduan Setup Langkah Demi Langkah

### Langkah 1: Buat Repository Baru di GitHub
1. Buka [github.com/new](https://github.com/new).
2. Beri nama repository (misal: `github-activity-tracker` atau `webgithub`).
3. Set sebagai **Public** *(atau Private, tapi pastikan opsi "Include private contributions" di profil GitHub kamu sudah dicentang)*.
4. **Jangan centang** "Add a README file".
5. Klik **Create repository**.

---

### Langkah 2: Hubungkan Project Lokal ke Repository GitHub
Buka terminal / PowerShell di folder ini (`c:\Users\daffa\Desktop\webgithub`), lalu jalankan:

```bash
git init
git add .
git commit -m "feat: initial commit with web dashboard"
git branch -M main
git remote add origin https://github.com/USERNAME_KAMU/NAMA_REPO_KAMU.git
git push -u origin main
```
*(Ganti `USERNAME_KAMU` dan `NAMA_REPO_KAMU` dengan akun GitHub kamu).*

---

### Langkah 3: Mengisi Hari Masa Lalu (Backfill History - Opsional)
Buka Dashboard (`buka_dashboard.bat`), pilih rentang tanggal pada panel **Backfill Masa Lalu**, lalu klik **Jalankan Backfill**. Setelah selesai, klik tombol **Git Push** di dashboard.

---

### Langkah 4: Aktifkan Izin Otomatisasi Cloud (GitHub Actions)
Agar GitHub Action bisa melakukan push otomatis setiap hari tanpa error permission:

1. Buka repository kamu di GitHub.
2. Masuk ke tab **Settings** -> **Actions** -> **General**.
3. Scroll ke bawah sampai bagian **Workflow permissions**.
4. Pilih **Read and write permissions**.
5. Centang **Allow GitHub Actions to create and approve pull requests**.
6. Klik **Save**.
