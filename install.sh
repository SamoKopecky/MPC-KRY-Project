#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
sudo apt install libc6-dev build-essential tcl libssl-dev

git clone https://github.com/sqlcipher/sqlcipher
cd sqlcipher

sudo ./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC -ansi" LDFLAGS="-lcrypto"
#sudo ./configure --enable-tempstore=yes LDFLAGS="-lcrypto -lm"
sudo make
sudo make install
