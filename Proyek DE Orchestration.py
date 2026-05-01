import requests
import matplotlib.pyplot as plt
import sqlite3
import smtplib
import mimetypes
import os
from email.message import EmailMessage
from datetime import datetime

folder_tujuan = r"C:\File Python 3.11(Global)"

# Gabungkan dengan nama file
db_path = os.path.join(folder_tujuan, 'crypto_data1.db')
log_path = os.path.join(folder_tujuan, 'log1.txt')
img_path = os.path.join(folder_tujuan, 'final_report.png') # Simpan gambar di folder yg sama

def get_crypto_price():
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=idr").json()
    return response['bitcoin']['idr'], response['ethereum']['idr']

def process_data(btc_price, eth_price):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Pastikan tabel ada
    cursor.execute('CREATE TABLE IF NOT EXISTS harga (waktu DATETIME DEFAULT CURRENT_TIMESTAMP, btc_price REAL, eth_price REAL)')
    
    #Ambil harga terakhir yang tersimpan
    cursor.execute('SELECT btc_price, eth_price FROM harga ORDER BY waktu DESC LIMIT 1')
    last_data = cursor.fetchone()

    #Logika anti duplikat
    if last_data is None or btc_price != last_data[0] or eth_price != last_data[1]:
        cursor.execute('INSERT INTO harga (btc_price, eth_price) VALUES (?, ?)', (btc_price, eth_price))
        conn.commit()
        status = 'BARU: Data BTC & ETH berhasil dimasukkan.'
    else:
        status = 'SKIP: Harga keduanya masih sama, tidak perlu disimpan.'

    #Ambil 10 data terakhir untuk grafik
    cursor.execute('SELECT btc_price, eth_price FROM harga ORDER BY waktu DESC LIMIT 10')
    rows = cursor.fetchall()[::-1]
    
    conn.close()
    return rows, status

#def send_report(file_gambar):
    msg = EmailMessage()
    msg['Subject'] = '📊 Daily Crypto Report'
    msg['From'] = 'bot@datamine.id'
    msg['To'] = 'user@pribadi.com'
    msg.set_content('Halo! Berikut adalah update tren harga Bitcoin 10 sesi terakhir.')

    with open(file_gambar, 'rb') as f:
        file_data = f.read()
        ctype, _ = mimetypes.guess_type(file_gambar)
        maintype, subtype = ctype.split('/', 1)
        msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_gambar)

    with smtplib.SMTP('sandbox.smtp.mailtrap.io', 2525) as server:
        server.login('Your_Email_User', 'Your_Email_Password')
        server.send_message(msg)

try:
    btc_now, eth_now = get_crypto_price()
    history, status_insert = process_data(btc_now, eth_now) # Eksekusi di sini saja

    # Bikin Grafik
    plt.figure(figsize=(10, 5))
    btc_hist = [row[0] for row in history]
    plt.plot(btc_hist, marker='o', color='orange', label='Bitcoin')
    
    eth_hist = [row[1] for row in history]
    plt.plot(eth_hist, marker='s', color='blue', label='Ethereum')
    
    plt.title(f'Tren Crypto (BTC: Rp {btc_now:,.0f} | ETH: Rp {eth_now:,.0f})')
    plt.legend()
    plt.savefig(img_path) # Gunakan img_path
    plt.close()

    # Kirim Email
    #send_report(img_path) 
    
    # Catat Log
    with open(log_path, "a") as f:
        waktu_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{waktu_log}] {status_insert} (Harga: (BTC: Rp {btc_now:,.0f} | ETH: Rp {eth_now:,.0f}))\n")
    
    print(f'✅ {status_insert}')

except Exception as e:
    # Backup log jika folder tujuan bermasalah
    with open(r'C:\Users\HUMAM\error_emergency.txt', "a") as f:
        f.write(f"[{datetime.now()}] Error: {str(e)}\n")
    print(f"❌ Terjadi kesalahan: {e}")
