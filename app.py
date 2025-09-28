import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static',
            template_folder='templates')

# --- KONFIGURASI TELEGRAM ---
# Ganti dengan token dan ID yang Anda dapatkan dari Langkah 1
# PENTING: Untuk production, gunakan environment variables, jangan hardcode seperti ini.
TELEGRAM_BOT_TOKEN = '8226893120:AAFJ-SNKc1F92-FGb9XLaqoulEpJumf5lpw'
TELEGRAM_CHAT_ID = '594729656'

# --- ROUTES UNTUK MENAMPILKAN HALAMAN HTML ---
@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/it-services')
def it_services():
    return render_template('it-services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/konstruksi')
def konstruksi():
    return render_template('konstruksi.html')

# --- API ENDPOINT UNTUK MENANGANI FORM ---
@app.route('/send-message', methods=['POST'])
def send_message():
    # Ambil data dari form yang dikirim oleh JavaScript
    data = request.form
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    company = data.get('company')
    message = data.get('message')
    # Ambil semua layanan yang dicentang
    services = request.form.getlist('service')

    if not name or not email or not message:
        return jsonify({'success': False, 'message': 'Nama, email, dan pesan wajib diisi.'}), 400

    # Format pesan yang akan dikirim ke Telegram
    service_text = ', '.join(services) if services else 'Tidak ada'
    text_to_telegram = (
        f"🔔 *Pesan Baru dari Website Inner Circle Asia*\n\n"
        f"*Nama:* {name}\n"
        f"*Perusahaan:* {company or '-'}\n"
        f"*Email:* {email}\n"
        f"*Telepon:* {phone or '-'}\n"
        f"*Layanan:* {service_text}\n\n"
        f"*Pesan:*\n{message}"
    )

    # Kirim pesan menggunakan Telegram Bot API
    url = f'https://api.telegram.org/bot8226893120:AAFJ-SNKc1F92-FGb9XLaqoulEpJumf5lpw/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text_to_telegram,
        'parse_mode': 'Markdown'
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return jsonify({'success': True, 'message': 'Pesan Anda berhasil terkirim!'})
        else:
            print("========================================")
            print("ERROR DARI TELEGRAM:", response.json())
            print("========================================")
            return jsonify({'success': False, 'message': 'Gagal mengirim notifikasi Telegram. Cek terminal untuk detail.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {e}'}), 500


if __name__ == '__main__':
    app.run(debug=True)