from cryptofiles import *


def create_message_public_key(username):
    message = {
            'id': 0,
            'name': username, 
            'public_key': get_public_key(username)
        }
    return message

def create_message_csr(username):
    message_with_csr = {
        'id': 1,
        'name': username,
        'csr': get_csr(username)
    }

    ecrypted_message = encrypt_with_authority_public_key(message_with_csr)
    return ecrypted_message

    