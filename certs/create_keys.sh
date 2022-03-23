#!/bin/bash


if [ -z "$1" ] || [ -z "$2" ]; then
	echo "Supply arguments to set the names"
	echo "For example: ./create_keys.sh alice bob"
	exit 1
fi

if [ ! -f root.key ] && [ ! -f root.crt ]; then
	echo "No root certificate and key found, generating them"
	openssl req -x509 -newkey rsa:2048 -keyout root.key -out root.crt -days 365 -nodes -subj "/C=CZ/O=MPC-KRY root/OU=MPC-KRY-R/CN=mpc-kry.cz"
fi

create_cert() {
	NAME=$1

	echo "Generating private key for ${NAME}"
	openssl genrsa -out $NAME.key 2048 
	echo "Generating certificate signing request for ${NAME}"
	openssl req -new -key $NAME.key -out $NAME.csr -subj "/C=CZ/O=MPC-KRY ${NAME}/OU=${NAME}/CN=${NAME}.cz"
	echo "Generating certificate for ${NAME}"
	openssl x509 -req -days 365 -in $NAME.csr -CA root.crt -CAkey root.key -CAcreateserial -out $NAME.crt

	rm $NAME.csr root.srl
	
	cp $NAME.crt $NAME-cert.pem
	echo "Genaring certificate chaine for ${NAME}"
	cat root.crt >> $NAME-cert.pem
}

create_cert $1
create_cert $2
