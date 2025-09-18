import mysql.connector
from mysql.connector import Error
import requests
import time
from datetime import datetime

//Request API TAELEGRAM
def kirim_telegram(pesan):
    token = "-"            // isi token
    chat_id = "-"         // ID chat telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": pesan
    }
    
//Notifikasi pengiriman 
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(" Pesan Telegram terkirim.")
        else:
            print(" Gagal mengirim pesan Telegram:", response.text)
    except Exception as e:
        print(" Error kirim Telegram:", e)

//pengecekan status 
def cek_simrs():
    try:
        response = requests.get("http://192.168.1.8/", timeout=5) //IP Server
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response.status_code == 200:
            print(f"{now} - SIMRS OK")
        else:
            pesan = f"{now} - SIMRS ERROR - Status: {response.status_code}"
            print(pesan)
            kirim_telegram(pesan)
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pesan = f"{now} - Tidak bisa akses SIMRS: {e}"
        print(pesan)
        kirim_telegram(pesan)
def cek_mysql():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        connection = mysql.connector.connect(
            host='-',             //IP Server DB 
            port=3306,            //Port      DB
            user='-',             //Username  DB
            password=''           //Password  DB
        )
        if connection.is_connected():
            print(f"{now} - MySQL OK")
            connection.close()
    except Error as e:
        pesan = f"{now} - MySQL DOWN: {e}"
        print(pesan)
        kirim_telegram(pesan)

while True:
    cek_simrs()
    cek_mysql()
    time.sleep(60) //pengecekan dengan detik


