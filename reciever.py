import socket

def main():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to localhost on port 12345
    s.bind(('localhost', 12345))

    # Start listening for incoming connections
    s.listen()
    print("Server is waiting for a connection...")

    try:
        while True:
            print("Ready to accept a new connection...")
            conn, addr = s.accept()  # Accept a new connection
            print('Connected by', addr)

            try:
                while True:
                    data = conn.recv(1024)  # Receive data from the client
                    if not data:
                        break  # If no data is received, break the loop
                    print("Received:", data)
            finally:
                conn.close()
    except KeyboardInterrupt:
        print("stopped by user")
        s.close()
    # Note: The server will keep running until manually stopped.
if __name__ == "__main__":
    main()