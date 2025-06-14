import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file, abort
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from functools import wraps
from models import db, add_user, get_user, check_user_password
from blockchain import add_block, load_chain, is_chain_valid

app = Flask(__name__)
app.secret_key = 'sheeba'

# Config for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create folders
os.makedirs('encrypted_files', exist_ok=True)
os.makedirs('decrypted_files', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

# Encryption key
if os.path.exists('secret.key'):
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

cipher = Fernet(key)

# Login protection
def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# Home route
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['role'] == 'uploader':
        return redirect(url_for('uploader_dashboard'))
    elif session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        user = get_user(uname)
        if user and check_user_password(user, pwd):
            session['username'] = uname
            session['role'] = user.role
            if user.role == 'uploader':
                return redirect(url_for('uploader_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
        return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        role = request.form['role']
        add_user(uname, pwd, role)
        return "User registered successfully!"
    return render_template('register.html')

@app.route('/uploader')
@login_required(role='uploader')
def uploader_dashboard():
    return render_template('index.html', username=session['username'])

@app.route('/admin')
@login_required(role='admin')
def admin_dashboard():
    files = os.listdir('uploads')
    return render_template('files.html', files=files)

@app.route('/encrypt', methods=['POST'])
@login_required(role='uploader')
def encrypt_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return "No file selected"
    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join('uploads', filename)
    uploaded_file.save(filepath)

    with open(filepath, 'rb') as f:
        data = f.read()
    encrypted = cipher.encrypt(data)

    encrypted_path = os.path.join('encrypted_files', filename + '.enc')
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted)

    add_block(f"{session['username']} encrypted and uploaded {filename}")
    return render_template('success.html', message="File encrypted successfully.")

@app.route('/decrypt/<filename>')
@login_required(role='admin')
def decrypt_file(filename):
    encrypted_path = os.path.join('encrypted_files', filename + '.enc')
    if not os.path.exists(encrypted_path):
        return "Encrypted file not found"
    with open(encrypted_path, 'rb') as f:
        encrypted = f.read()
    try:
        decrypted = cipher.decrypt(encrypted)
    except:
        return "Decryption failed"
    decrypted_path = os.path.join('decrypted_files', 'decrypted_' + filename)
    with open(decrypted_path, 'wb') as f:
        f.write(decrypted)

    add_block(f"{session['username']} decrypted {filename}")
    return send_file(decrypted_path, as_attachment=True)

@app.route('/view_logs')
@login_required(role='admin')
def view_logs():
    chain = load_chain()
    valid = is_chain_valid(chain)
    return render_template('logs.html', chain=chain, valid=valid)

if __name__ == '__main__':
<<<<<<< HEAD
    with app.app_context():
        db.create_all()  # Only first time
    app.run(debug=True)

















=======
    app.run(debug=True)
>>>>>>> 10c11696daaedde5298c06acd93b98843da94dff
