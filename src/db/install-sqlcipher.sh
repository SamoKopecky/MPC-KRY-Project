#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


git clone https://github.com/sqlcipher/sqlcipher
cd sqlcipher

./configure --enable-tempstore=yes LDFLAGS="-lcrypto -lm"
make
sudo make install
