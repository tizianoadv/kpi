from cryptofiles import *

def create_message_public_key(username):
    message = {
            'id': 0,
            'name': username, 
            'content': 'Hello, I want to create an asymetric exchange, here is my public key',
            'public_key': get_public_key(username)
        }
    return message

def create_message_certificate():
    return ""