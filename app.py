import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from blockchain import add_block, load_chain, is_chain_valid

app = Flask(__name__)


os.makedirs('encrypted_files', exist_ok=True)
os.makedirs('decrypted_files', exist_ok=True)


KEY_FILE = 'secret.key'
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
else:
    with open(KEY_FILE, 'rb') as f:
        key = f.read()

cipher = Fernet(key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    print(f"Received file: {file.filename}")
    filename = secure_filename(file.filename)
    file_path = os.path.join('encrypted_files', filename)

    data = file.read()
    encrypted = cipher.encrypt(data)
    with open(file_path, 'wb') as f:
        f.write(encrypted)

    add_block('upload', filename)
    return render_template('success.html', message='File encrypted successfully.')

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    filename = request.form['filename']
    enc_path = os.path.join('encrypted_files', filename)
    dec_path = os.path.join('decrypted_files', filename)

    if not os.path.exists(enc_path):
        return "File not found!"

    with open(enc_path, 'rb') as f:
        encrypted_data = f.read()

    try:
        decrypted = cipher.decrypt(encrypted_data)
    except Exception as e:
        return f"Decryption failed: {e}"

    with open(dec_path, 'wb') as f:
        f.write(decrypted)

    add_block('decrypt', filename)
    return send_file(dec_path, as_attachment=True)

@app.route('/logs')
def view_logs():
    chain = load_chain()
    valid = is_chain_valid(chain)
    return {
        'valid_chain': valid,
        'log_chain': chain
    }

if __name__ == '__main__':
    app.run(debug=True)