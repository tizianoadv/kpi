import subprocess
import os

# Ask for name
username = input("Enter your name (lower case -  without special character): ")

# Init
home_dir = os.path.expanduser("~")
keys_dir = os.path.join(home_dir, "keys")
subprocess.run(["mkdir", "-p", keys_dir])
print(f"[{username}] - Keys folder generated")

# Generate private key
client_private_key_path = os.path.join(keys_dir, f"{username}_private_key.pem")
subprocess.run(["openssl", "genrsa", "-out", client_private_key_path, "4096"])
print(f"[{username}] - Private key generated")

# Generate public key from private key
client_public_key_path = os.path.join(keys_dir, f"{username}_public_key.pem")
subprocess.run(["openssl", "rsa", "-in", client_private_key_path, "-pubout", "-out", client_public_key_path])
print(f"[{username}] - Public key generated")

# Greate CSR configuration file
uppercase_username = username.upper()
csr_config = f'''[req]
default_bits = 4096
prompt = no
default_md = sha256
distinguished_name = dn

[dn]
CN = {uppercase_username}
O = UNIV_REIMS
OU = DAS_TEAM
L = REIMS
ST = MARNE
C = FR
emailAddress = {username}@email.com'''

client_csr_conf_path = os.path.join(keys_dir, f"{username}_csr.conf")
with open(client_csr_conf_path, "w") as conf_file:
    conf_file.write(csr_config)
print(f"[{username}] - Certificate Signing Request configuration file created")


# Generate CSR using private key and configuration file
client_csr_path = os.path.join(keys_dir, f"{username}_csr.csr")
subprocess.run(["openssl", "req", "-new", "-key", client_private_key_path, "-out", client_csr_path, "-config", client_csr_conf_path])
print(f"[{username}] - Certificate Signing Request generated")
