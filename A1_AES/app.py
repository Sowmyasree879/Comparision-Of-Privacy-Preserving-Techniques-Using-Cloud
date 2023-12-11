from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import os

app = Flask(__name__)

def encrypt_data(data, key):
    if len(key) != 64:
        raise ValueError("Incorrect AES key length")

    cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    cipher_text_base64 = base64.b64encode(cipher_text).decode('utf-8')
    return iv, cipher_text_base64

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json().get('data')
    key = os.environ.get('ENCRYPTION_KEY', '')

    try:
        # Encrypt data
        iv, encrypted_data = encrypt_data(data, key)
        return jsonify({'iv': iv, 'encrypted_data': encrypted_data})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000)
