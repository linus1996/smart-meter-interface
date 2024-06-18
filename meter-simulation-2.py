import os
import socket
import time
import random
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

logging.basicConfig(level=logging.DEBUG)

# Encryption setup
key = b'1234123412341234'  # Ensure it's securely shared between both scripts

def encrypt_message(message):
    iv = os.urandom(12)  # Generate a random IV for AES-GCM each time
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    # Encrypt the message
    encrypted_data = encryptor.update(message.encode()) + encryptor.finalize()
    return (iv, encryptor.tag, encrypted_data)

def create_and_send_message():
    try:
        energy_value = random.randint(10000, 20000)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        message = f"Energy value: {energy_value}, Timestamp: {current_time}"
        iv, tag, encrypted_message = encrypt_message(message)

        logging.debug(f"Encrypted message: {encrypted_message}")
        return iv + tag + encrypted_message
    except Exception as e:
        logging.error(f"Error during message encryption: {e}")
        return None

def send_message_over_network(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12345))
        s.sendall(message)
        logging.info("Encrypted message sent over network")

if __name__ == "__main__":
    logging.info("Starting encrypted DLMS/COSEM message simulation")
    while True:  # Loop to send messages every 10 seconds
        message = create_and_send_message()
        if message:
            send_message_over_network(message)
        time.sleep(10)  # Wait for 10 seconds before sending the next message
