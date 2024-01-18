import socket
import threading

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 1234

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(5)
print('Server listening on', SERVER_ADDRESS, 'port', SERVER_PORT)

# Dictionary to store client username and password
client_credentials = {}

# Function to handle client connections
def handle_client(client_socket, client_address):
    print('New client connected:', client_address)

    # Receive the username and password from the client
    username = client_socket.recv(1024).decode('utf-8')
    password = client_socket.recv(1024).decode('utf-8')

    # Check if the username is already taken
    if username in client_credentials:
        # Send login failure message to the client
        client_socket.send('Username already taken. Please choose a different username.'.encode('utf-8'))
        client_socket.close()
        print('Client disconnected:', client_address)
        return

    # Store the username and password for the client
    client_credentials[username] = password

    # Send login success message to the client
    client_socket.send('Login successful. You are now connected to the server.'.encode('utf-8'))

    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')

        if data == 'get_clients':
            # Send the list of connected clients to the client
            client_list = ', '.join(client_credentials.keys())
            client_socket.send(client_list.encode('utf-8'))
        else:
            # Echo back the received data to the client
            client_socket.send(data.encode('utf-8'))
            print('Received from client:', data)

    # Close the client socket
    client_socket.close()
    print('Client disconnected:', client_address)

# Function to accept incoming connections
def accept_connections():
    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()

        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start accepting incoming connections
accept_connections()