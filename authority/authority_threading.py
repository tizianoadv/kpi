import socket
import json
import threading
from messages import *
from cryptofiles import *

# Set up Authority username
authority_name = "authority"

# Initialisation
SERVER_ADDRESS = '192.168.56.2'
SERVER_PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen(1)
print('Server listening on {}:{}'.format(SERVER_ADDRESS, SERVER_PORT))

def handle_connection(client_socket, client_address):
    connection_still_up = 1
    while connection_still_up:
        response = dict()
        data = client_socket.recv(1024).decode()

        try:
            message = json.loads(data)
            if 'id' in message:
                if message['id'] == 0:
                    print(f"[Authority] - Public key from *** {message['name']} *** Received")
                    save_public_key_to_file(message['public_key'], f"clients_public_key/{message['name']}_public_key.pem")
                    print(f"[Authority] - Public key from *** {message['name']} *** Saved")
                    response = create_message_public_key(authority_name)
                    print(f"[Authority] - Authority's public key sent to *** {message['name']} ***")
                else:
                    print(f"[Authority] - Encrypted CSR received from *** {message['name']} ***")
                    decrypt_csr_message(data['name'], data['csr'])
                    print(f"[Authority] - CSR of *** {message['name']} *** decrypted")
                    create_certificate(data['name'])
                    print(f"[Authority] - Certificate of *** {message['name']} *** created")
                    response = create_message_certificate(authority_name, message_received)
                    response['certificate'] = encrypt_certificate_with_pub_key_client(data['name'], response['certificate'])
                    print(f"[Authority] - Certificate of *** {message['name']} *** encrypted with his public key")
                    print(f"[Authority] - Encrypted certificate sent to *** {message['name']} ***")
                    connection_still_up = 0
                response_json = json.dumps(response)
                client_socket.send(response_json.encode())
        except json.JSONDecodeError as e:
            print('Invalid JSON format:', str(e))

        del response
    client_socket.close()



while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Connected to client:', client_address)

    # Start a new thread to handle the connection
    connection_thread = threading.Thread(target=handle_connection, args=(client_socket, client_address))
    connection_thread.start()
