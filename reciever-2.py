import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

key = b'1234123412341234'  # Same key as used in sender.py

def decrypt_message(iv, tag, encrypted_message, key):
    try:
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()

        return decryptor.update(encrypted_message) + decryptor.finalize()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 12345))
    s.listen()
    print("Server waiting for a connection...")

    try:
        while True:  # Continuously accept new connections
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            try:
                while True:  # Handle multiple messages if necessary
                    data = conn.recv(1024)
                    if not data:
                        break

                    iv = data[:12]
                    tag = data[12:28]
                    encrypted_message = data[28:]
                    message = decrypt_message(iv, tag, encrypted_message, key)
                    if message:
                        print("Decrypted message:", message.decode('utf-8'))
                    else:
                        print("Failed to decrypt message.")
            finally:
                conn.close()  # Close the current connection and go back to listening
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        s.close()

if __name__ == "__main__":
    main()
