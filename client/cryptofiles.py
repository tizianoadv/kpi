from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509
import json

def get_public_key(username):
    # Path to the public key file
    public_key_path = f"keys/{username}_public_key.pem"

    # Load the public key from file
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    # Retrieve the public key in PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_pem.decode()


def get_csr(username):

    # Read the contents of the file
    with open(f"keys/{username}_csr.csr", "rb") as file:
        csr_data = file.read()

    # Load the CSR from the data
    csr = x509.load_pem_x509_csr(csr_data, default_backend())

    return csr.public_bytes(encoding=serialization.Encoding.PEM).decode("utf-8")[:-2]


def save_public_key_to_file(public_key_str, file_path):
     # Convert the string to bytes
    public_key_bytes = public_key_str.encode()

    # Load the public key from bytes
    public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())

    # Serialize the public key to PEM format
    pem_data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write the PEM data to the file
    with open(file_path, "wb") as file:
        file.write(pem_data)


def encrypt_with_authority_public_key(json_object):
    # Serialize the JSON object
    json_data = json.dumps(json_object).encode('utf-8')

    # Load the public key from file
    with open("keys/authority_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    # Retrieve the public key in PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Encrypt the JSON data
    encrypted_data = public_key.encrypt(
        json_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Return the encrypted data
    return encrypted_data