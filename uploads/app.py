from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def encrypt_file(file_path):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    
    with open(file_path, 'rb') as f:
        data = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(data)

    enc_file_path = file_path + '.enc'
    with open(enc_file_path, 'wb') as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

    with open(file_path + '.key', 'wb') as f:
        f.write(key)

    return enc_file_path
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)

    with open(file_path, 'rb') as f:
        data = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(data)

    enc_path = file_path + '.enc'
    with open(enc_path, 'wb') as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

    key_path = file_path + '.key'
    with open(key_path, 'wb') as fkey:
        fkey.write(key)

    return f"File uploaded and encrypted successfully! Encrypted file: {enc_path}"

@app.route('/files')
def list_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.enc'):
            files.append(filename)
    return render_template('files.html', files=files)

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    filename = request.form['filename']
    enc_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    key_path = enc_path.replace('.enc', '.key')

    print("ENC File Path:", enc_path)
    print("KEY File Path:", key_path)

    if not os.path.exists(enc_path):
        return f"Encrypted file not found: {filename}"
    if not os.path.exists(key_path):
        return f"Key file not found: {filename.replace('.enc', '.key')}"

if __name__ == '__main__':
    app.run(debug=True)