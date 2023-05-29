from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def get_public_key(username):
    # Path to the public key file
    public_key_path = f"pki/{username}_public_key.pem"

    # Load the public key from file
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    # Retrieve the public key in PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_pem.decode()


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

