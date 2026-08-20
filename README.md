# 🌿 GitHub Contribution Auto-Bot & Backfill System

Sistem otomatisasi dan generator kontribusi GitHub untuk memperbanyak kotak hijau di profil GitHub kamu (1–3 kontribusi per hari atau backfill riwayat masa lalu).

---

## 📁 Struktur File

- **`backfill.py`**: Script untuk mengisi kotak hijau pada tanggal-tanggal masa lalu (bisa 1 tahun terakhir, 6 bulan, atau custom tanggal).
- **`daily.py`**: Script yang membuat 1–3 commit acak untuk hari ini.
- **`.github/workflows/auto-commit.yml`**: GitHub Action otomatis yang berjalan di cloud setiap hari (tidak perlu laptop menyala).
- **`activity.txt`**: File catatan yang akan diupdate secara otomatis setiap commit.

---

## 🚀 Panduan Setup Langkah Demi Langkah

### Langkah 1: Buat Repository Baru di GitHub
1. Buka [github.com/new](https://github.com/new).
2. Beri nama repository (misal: `github-activity-tracker` atau `webgithub`).
3. Set sebagai **Public** *(atau Private, tapi pastikan opsi "Include private contributions" di profil GitHub kamu sudah dicentang)*.
4. **Jangan centang** "Add a README file" (karena kita sudah punya filenya).
5. Klik **Create repository**.

---

### Langkah 2: Hubungkan Project Lokal ke Repository GitHub
Buka terminal / PowerShell di folder ini (`c:\Users\daffa\Desktop\webgithub`), lalu jalankan:

```bash
git init
git add .
git commit -m "feat: initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME_KAMU/NAMA_REPO_KAMU.git
git push -u origin main
```
*(Ganti `USERNAME_KAMU` dan `NAMA_REPO_KAMU` dengan akun GitHub kamu).*

---

### Langkah 3: Mengisi Hari Masa Lalu (Backfill History - Opsional)
Jika kamu ingin langsung menghijaukan hari-hari yang kosong di masa lalu:

1. Jalankan script backfill di terminal:
   ```bash
   python backfill.py
   ```
2. Pilih opsi rentang waktu (misal pilih `1` untuk 365 hari terakhir).
3. Setelah proses selesai, push commit-commit tersebut ke GitHub:
   ```bash
   git push origin main
   ```
*Tunggu 1-2 menit, lalu refresh profil GitHub kamu. Kotak hijau masa lalu akan langsung terisi!*

---

### Langkah 4: Aktifkan Izin Otomatisasi Cloud (GitHub Actions)
Agar GitHub Action bisa melakukan push otomatis setiap hari tanpa error permission:

1. Buka repository kamu di GitHub.
2. Masuk ke tab **Settings** -> **Actions** -> **General**.
3. Scroll ke bawah sampai bagian **Workflow permissions**.
4. Pilih **Read and write permissions**.
5. Centang **Allow GitHub Actions to create and approve pull requests**.
6. Klik **Save**.

---

### Langkah 5: Tes Jalankan GitHub Action
1. Masuk ke tab **Actions** di repo GitHub kamu.
2. Klik workflow **Daily Auto Contribution** di sebelah kiri.
3. Klik tombol **Run workflow** -> **Run workflow**.
4. Setelah workflow berhasil berstatus hijau (centang), cek profil kamu!

---

## ⚙️ Pengaturan Tambahan (Opsional)

- **Mengubah Jam Jadwal**: Buka [`.github/workflows/auto-commit.yml`](.github/workflows/auto-commit.yml) dan sesuaikan baris `cron: '0 3 * * *'` (Waktu menggunakan format UTC, WIB = UTC + 7).
- **Mengubah Jumlah Commit**: Buka [`daily.py`](daily.py) dan ubah parameter `make_daily_commits(1, 3)` sesuai keinginan.
