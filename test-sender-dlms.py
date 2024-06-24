import logging
from gurux_dlms import GXDLMSClient, GXDLMSConverter, GXByteBuffer, GXDLMSTranslator
from gurux_dlms.enums import InterfaceType, Authentication
from gurux_dlms.secure import GXDLMSSecureClient
from gurux_dlms.objects import GXDLMSObject
import time
import random
import socket

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create a DLMS/COSEM client
client = GXDLMSClient(True)
client.client_address = 16
client.server_address = 1
client.use_logical_name_referencing = True
client.interface_type = InterfaceType.HDLC
client.authentication = Authentication.NONE

# Define the simulated register class
class SimulatedDLMSRegister(GXDLMSObject):
    def __init__(self, logical_name):
        super().__init__()
        self.logical_name = logical_name
        self.value = None

    def update_value(self, new_value):
        self.value = new_value

def create_and_send_message():
    try:
        energy_register = SimulatedDLMSRegister("1.0.1.8.0.255")
        energy_value = random.randint(10000, 20000)
        energy_register.update_value(energy_value)
        logging.debug(f"Simulated energy value set to: {energy_value}")

        # Create a request to read the value of the register
        data = client.read(energy_register)
        bb = GXByteBuffer()
        client.getMessages(data, bb)
        
        return bb.array()  # Return the bytes to be sent over the network
    except Exception as e:
        logging.error(f"Error during create_and_send_message: {e}")
        return None

def send_message_over_network(message):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('192.168.53.5', 12345))
                s.sendall(message)
                logging.info("Message sent over network")
                break  # Exit the loop if message sent successfully
        except ConnectionRefusedError:
            logging.warning("Connection refused, retrying...")
            time.sleep(5)  # Wait for some time before retrying

def send_messages_periodically():
    try:
        while True:
            message = create_and_send_message()
            if message:
                send_message_over_network(message)  # Send the message over the network
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Stopped by user")

if __name__ == "__main__":
    logging.info("Starting DLMS/COSEM message simulation")
    send_messages_periodically()
