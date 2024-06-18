import logging
from gurux_dlms import GXDLMSClient, GXDLMSConverter
from gurux_dlms.enums import InterfaceType, Authentication, DataType
import time
import random
import socket

# Define the simulated register class
class SimulatedDLMSRegister:
    def __init__(self, logical_name):
        self.logical_name = logical_name
        self.value = None

    def update_value(self, new_value):
        self.value = new_value

# Other setup and configurations
logging.basicConfig(level=logging.DEBUG)
client = GXDLMSClient(True)
client.client_address = 1
client.server_address = 1
client.use_logical_name_referencing = True
client.interface_type = InterfaceType.HDLC
client.authentication = Authentication.NONE

def create_and_send_message():
    try:
        energy_register = SimulatedDLMSRegister("1.0.1.8.0.255")
        energy_value = random.randint(10000, 20000)
        energy_register.update_value(energy_value)
        logging.debug(f"Simulated energy value set to: {energy_value}")
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) 
        
        logging.debug(f"Time at: {current_time}")
        
        # This would be your simulated message
        simulated_message = f"Register: {energy_register.logical_name}, Value: {energy_register.value}, Timestamp: {current_time}"
        return simulated_message.encode()  # Encode to bytes for sending
    except Exception as e:
        logging.error(f"Error during create_and_send_message: {e}")
        return None

# Network sending functions and main block remain the same


def send_message_over_network(message):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 12345))
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
