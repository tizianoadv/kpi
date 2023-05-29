[SERVERCA]
// Init
workdir ~/app
apt update
apt install -y openssl
mkdir -p ~/openssl_cert && cd openssl_cert

// Generate private key for CA
openssl genrsa -des3 -out private.key -passout pass:masterdas 4096
openssl genrsa -out private.key 4096

// Generate a Certificate Signing Request
// Create a config file
touch csr.conf

echo -e "[req]\ndefault_bits = 4096\nprompt = no\ndefault_md = sha256\ndistinguished_name = dn\n\n[dn]\nCN = MASTERDAS_AUTHORITY\nO = UNIV_REIMS\nOU = DAS_TEAM\nL = REIMS\nST = MARNE\nC = FR" > csr.conf 

//Generate CSR file
openssl req -new -key private.key -out csr.csr -passout pass:masterdas -config csr.conf 
openssl req -new -key private.key -out csr.csr -config csr.conf 

// Generate Cert file:
openssl x509 -req -days 365 -in csr.csr -signkey private.key -out certificate.crt


// Watch conclusion: 
openssl x509 -in certificate.crt -subject -issuer -dates -noout


// sign a certificate received:
openssl x509 -req -in client.csr -out client.crt -CA certificate.crt -CAkey private.key

// Check information of the certificate
openssl x509 -in client.crt -subject -issuer -dates -noout




[Client]
//Gen private key
openssl genrsa -out private.key 4096

//Gen information for CSR

echo -e "[req]\ndefault_bits = 4096\nprompt = no\ndefault_md = sha256\ndistinguished_name = dn\n\n[dn]\nCN = MY_NAME\nO = UNIV_REIMS\nOU = DAS_TEAM\nL = REIMS\nST = MARNE\nC = FR\nemailAddress = myemail@email.com" > csr.conf 

sed -i 's/CN = MY_NAME/CN = MY_NAME/' csr.conf
sed -i 's/emailAddress = myemail@email.com/emailAddress = myemail@email.com/' csr.conf

openssl req -new -key private.key -out csr.csr -config csr.conf

//Verify a certificate
openssl verify -CAfile authoritycert.crt mycert.crt
