#!/usr/bin/env python3

import ssl
import socket

# TODO:
# Proper logging
from time import sleep


class Server:
    def __init__(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.context.load_cert_chain("certs/root.crt", "certs/root.key")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.hostname = '127.0.0.1'
        self.port = 8443

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind((self.hostname, self.port))
            sock.listen(5)
            with self.context.wrap_socket(sock, server_side=True) as secure_socket:
                conn, addr = secure_socket.accept()
                print(f"connected: {addr}")
                print(conn.recv(2048))
