import subprocess
import os

# Init
home_dir = os.path.expanduser("~")
pki_dir = os.path.join(home_dir, "pki")
subprocess.run(["mkdir", "-p", pki_dir])
print("[Authority] - PKI folder generated")

# Generate private key
auth_private_key_path = os.path.join(pki_dir, "authority_private_key.pem")
subprocess.run(["openssl", "genrsa", "-out", auth_private_key_path, "4096"])
print("[Authority] - Private key generated")

# Generate public key from private key
auth_public_key_path = os.path.join(pki_dir, "authority_public_key.pem")
subprocess.run(["openssl", "rsa", "-in", auth_private_key_path, "-pubout", "-out", auth_public_key_path])
print("[Authority] - Public key generated")

# Create CSR configuration file
csr_config = '''[req]
default_bits = 4096
prompt = no
default_md = sha256
distinguished_name = dn

[dn]
CN = AUTHORITY_MASTERDAS
O = UNIV_REIMS
OU = DAS_TEAM
L = REIMS
ST = MARNE
C = FR'''

auth_csr_conf_path = os.path.join(pki_dir, "authority_csr.conf")
with open(auth_csr_conf_path, "w") as conf_file:
    conf_file.write(csr_config)
print("[Authority] - Certificate Signing Request configuration file created")

# Generate CSR using private key and configuration file
auth_csr_path = os.path.join(pki_dir, "authority_csr.csr")
subprocess.run(["openssl", "req", "-new", "-key", auth_private_key_path, "-out", auth_csr_path, "-config", auth_csr_conf_path])
print("[Authority] - Certificate Signing Request generated")

# Generate authority certificate
auth_certificate_path = os.path.join(pki_dir, "authority_certificate.crt")
subprocess.run(["mkdir", "-p", "~\/pki"])
subprocess.run(["openssl", "x509", "-req", "365", "-in", auth_csr_path, "-signkey", auth_private_key_path, "-out", auth_certificate_path])
print("[Authority] - Self-signed X509 certificate generated")

# Create clients public keys folder
client_public_key_folder_path = os.path.join(home_dir, "clients_public_key")
subprocess.run(["mkdir", "-p", client_public_key_folder_path])
# Create clients Certificate Signing Request folder
client_csr_folder_path = os.path.join(home_dir, "clients_csr")
subprocess.run(["mkdir", "-p", client_csr_folder_path])
# Create clients Certificate folder
client_certificate_folder_path = os.path.join(home_dir, "clients_certificate")
subprocess.run(["mkdir", "-p", client_certificate_folder_path])
# Create clients Certificate encrypted folder
client_certificate_encrypted_folder_path = os.path.join(home_dir, "clients_certificate_encrypted")
subprocess.run(["mkdir", "-p", client_certificate_encrypted_folder_path])
print("[Authority] - Ready to receive Certificate Signing Requests from clients")

# Clean unseful folder
subprocess.run(["rm", "-r", "~\\/"])