# Bot Telegram Menu Dinamis (Branch: inline-button)

Bot Telegram sederhana yang menggunakan **Inline Buttons** untuk navigasi menu yang interaktif dan modern. Bot ini memungkinkan pengguna untuk memilih layanan dan memasukkan data (seperti username) dalam satu alur percakapan yang mulus.

## ✨ Fitur Baru

- **Inline Menu**: Tombol navigasi menempel langsung pada pesan chat (bukan di keyboard bawah).
- **Interactive Flow**: Setelah memilih layanan, pesan akan berubah secara dinamis untuk meminta input berikutnya.
- **🔄 Tombol Coba Lagi**: Fitur untuk mereset menu dan memilih ulang layanan dari awal.
- **Support .env**: Konfigurasi token yang aman menggunakan file environment variables.

## 🛠️ Persyaratan

- Python 3.10 ke atas
- Token Bot dari [@BotFather](https://t.me/botfather)

## 🚀 Cara Menjalankan

1. **Clone project dan masuk ke direktori:**

   ```powershell
   cd BotTele
   ```

2. **Aktifkan Virtual Environment:**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Konfigurasi Token:**
   Buat file `.env` di folder utama dan isi dengan token bot Anda:

   ```text
   BOT_TOKEN=TOKEN_BOT_ANDA
   ```

5. **Jalankan Bot:**
   ```powershell
   python bot.py
   ```

## 📖 Cara Penggunaan

1. Kirim perintah `/start` ke bot.
2. Klik salah satu tombol layanan (Diamond, Cash, Poin, atau Lokasi).
3. Ketikkan username yang diminta.
4. Klik tombol **"Coba Lagi"** jika ingin mengulang atau memilih layanan lain.

---

