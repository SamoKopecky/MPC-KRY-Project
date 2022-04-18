#!/bin/bash

NAME=$1
PASSWORD=$2
CERTS_DIR=$3

cd $CERTS_DIR

echo $PASSWORD
if [ ! -f root.key ] && [ ! -f root.crt ]; then
	echo "No root certificate and key found, generating them"
	openssl req -x509 -newkey rsa:2048 -keyout root.key -out root.crt -days 365 -nodes -subj "/C=CZ/O=MPC-KRY root/OU=MPC-KRY-R/CN=mpc-kry.cz"
fi

create_cert() {

	echo "Generating private key for ${NAME}"
	openssl genrsa -aes128 -passout pass:$PASSWORD -out $NAME.key 2048
	echo "Generating certificate signing request for ${NAME}"
	openssl req -passin pass:$PASSWORD -new -key $NAME.key -out $NAME.csr -subj "/C=CZ/O=MPC-KRY ${NAME}/OU=${NAME}/CN=${NAME}.cz"
	echo "Generating certificate for ${NAME}"
	openssl x509 -req -days 365 -in $NAME.csr -CA root.crt -CAkey root.key -CAcreateserial -out $NAME.crt

	rm $NAME.csr root.srl
	
	cp $NAME.crt $NAME-cert.pem
	echo "Generating certificate chain for ${NAME}"
	cat root.crt >> $NAME-cert.pem
}

create_cert $1
