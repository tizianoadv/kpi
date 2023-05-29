import socket
import json
from messages import *
from cryptofiles import save_public_key_to_file
from time import sleep


# Ask for name
username = input("Enter your name (lower case -  without special character): ")

# Define authority address and port
AUTHORITY_ADDRESS = '192.168.56.2'
AUTHORITY_PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the authority
client_socket.connect((AUTHORITY_ADDRESS, AUTHORITY_PORT))

# Prepare the client message
message = create_message_public_key(username)

# Send the message to the authoritY in JSON format
message_json = json.dumps(message)
client_socket.send(message_json.encode())

while True:
    sleep(1)
    response = dict()
    # Receive the authority's response
    data = client_socket.recv(1024).decode()

    if not data:
        break

    # Parse the received JSON message
    try:
        message = json.loads(data)
        if 'id' in message :
            authority_message_id = message['id']
            if authority_message_id == 0:
                save_public_key_to_file(message['public_key'],f"keys/{message['name']}_public_key.pem")
                # Inclure une CSR dans message 
                # Chiffrer le message avec clé privé de l'autorité
                response_encrypted = create_message_csr(username)
                print("HERE IT IS")
                print(response_encrypted)
                print(type(response_encrypted))
            else :
                print("[Client] - Certificate received from the authority") 
            response_json = json.dumps(response)
            print(response_json)
            client_socket.send(response_json.encode())
    except json.JSONDecodeError as e:
        print('Invalid JSON format:', str(e))

    # response_json = json.dumps(response)
    # print(response_json)
    # client_socket.send(response_json.encode())
    del response

# Close the client socket
client_socket.close()