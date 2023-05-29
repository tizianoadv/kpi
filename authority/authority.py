import socket
import json
from messages import *

# Set up Authority username
authority_name = "authority"

# Define server address and port
SERVER_ADDRESS = '192.168.56.2'
SERVER_PORT = 12345
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the server address and port
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
# Listen for incoming connections
server_socket.listen(1)
print('Server listening on {}:{}'.format(SERVER_ADDRESS, SERVER_PORT))

# Accept a client connection
client_socket, client_address = server_socket.accept()
print('Connected to client:', client_address)

while True:
    response = dict()
    # Receive data from the client
    data = client_socket.recv(1024).decode()
    # print(f'Received from client:', data)

    if not data:
        break

    if data.lower() == 'exit':
        break

    # Parse the received JSON message
    try:
        message = json.loads(data)
        
        if 'id' in message :
            print(message)
            client_message_id = message['id']
            if client_message_id == 0:
                print(f"Received public key from {message['name']}")
                save_public_key_to_file(message['public_key'],f"clients_public_key/{message['name']}_public_key.pem")
                response = create_message_public_key(authority_name)
                print(f"Sent authority public key to {message['name']}")
            else :
                print(f"Received encrypted CSR from {message['name']}")
                response = create_message_certificate(authority_name, message_received)
                # Déchiffrer avec ma privé le message
                # Crée un certificat à partir de son CSR
                # Inclure le certificat du client dans le message
                # Inclure le certificat de l'autorité autosigné dans le message
                # Chiffrer l'ensemble du message avec la clé publique du client
                print(f"Sent Certificate to {message['name']}")
    except json.JSONDecodeError as e:
        print('Invalid JSON format:', str(e))

    # Send the response back to the client in JSON format
    response_json = json.dumps(response)
    client_socket.send(response_json.encode())
    del response


# Close the client socket and the server socket
client_socket.close()
server_socket.close()

