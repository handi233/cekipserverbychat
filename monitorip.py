import os
import mysql.connector
from mysql.connector import Error
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# ====== LOAD ENVIRONMENT VARIABLE ======
# Buat file .env di direktori yang sama:
# TELEGRAM_TOKEN=xxxx
# TELEGRAM_CHAT_ID=xxxx
# DB_HOST=192.168.xxx.xxx
# DB_PORT=3306
# DB_USER=username
# DB_PASS=password

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# ====== FUNGSI KIRIM TELEGRAM ======
def kirim_telegram(pesan: str):
    """Mengirim pesan ke Telegram bot"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": pesan
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            print("✅ Pesan Telegram terkirim.")
        else:
            print(f"⚠️ Gagal mengirim pesan Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Error kirim Telegram: {e}")

# ====== CEK SIMRS (SERVER APLIKASI) ======
def cek_simrs():
    """Cek apakah SIMRS (aplikasi rumah sakit) dapat diakses"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.get("http://192.168.1.8/", timeout=5)  # Ganti dengan IP server SIMRS
        if response.status_code == 200:
            print(f"{now} - SIMRS ✅ OK")
        else:
            pesan = f"{now} - ⚠️ SIMRS ERROR - Status: {response.status_code}"
            print(pesan)
            kirim_telegram(pesan)
    except Exception as e:
        pesan = f"{now} - ❌ Tidak bisa akses SIMRS: {e}"
        print(pesan)
        kirim_telegram(pesan)

# ====== CEK MYSQL (SERVER DATABASE) ======
def cek_mysql():
    """Cek koneksi server MySQL tanpa akses ke data pasien"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            connection_timeout=5
        )
        if connection.is_connected():
            print(f"{now} - MySQL ✅ OK")
            connection.close()
    except Error as e:
        pesan = f"{now} - ❌ MySQL DOWN: {e}"
        print(pesan)
        kirim_telegram(pesan)

# ====== LOOP CEK TIAP 60 DETIK ======
if __name__ == "__main__":
    while True:
        cek_simrs()
        cek_mysql()
        time.sleep(60)  # pengecekan setiap 60 detik
