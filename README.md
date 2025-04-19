# 🔐 Secure Document Transmission System for Defence Units

A secure file transfer web application that enables encrypted document uploads, access-controlled decryption, and blockchain-style action logging — built using Python, Flask, and HTML/CSS.

---

## ✨ Features

- *File Encryption:* Encrypt documents before upload using Fernet symmetric encryption.
- *Secure Upload & Download:* Transfer encrypted documents safely via the web app.
- *Decryption Access Control:* Only authorized users can decrypt files with the right key.
- *Blockchain Logging:* Track file actions using a simulated blockchain log.
- *User-Friendly Interface:* Responsive UI with Bootstrap.

---

## 🛠 Technologies Used

- Python 3
- Flask
- HTML5, CSS3, Bootstrap
- Cryptography (Fernet)
- Simulated Blockchain (Python logic)

---

## 🖼 Screenshots

### Upload Page
![Upload Page](screenshots/upload.png)

### Decryption Page
![Decrypt Page](screenshots/decrypt.png)

> Make sure you add your screenshots in a folder called screenshots/ and push them too!

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/yourusername/itsecuredefenseproject.git
cd itsecuredefenseproject
pip install -r requirements.txt
python app.py
