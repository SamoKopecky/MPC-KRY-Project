#!/usr/bin/env python3

import ssl
import socket
from FileUtils import save_file


# TODO:
# Files bigger then 2048 bytes
# Proper logging
# Docs


class Server:
    def __init__(self):
        self.context = ssl.SSLContext
        self.secure_socket = ssl.SSLSocket
        self.hostname = '127.0.0.1'
        self.port = 8443
        self.init_sock()

    def init_sock(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.context.load_cert_chain("certs/root.crt", "certs/root.key")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind((self.hostname, self.port))
        sock.listen(5)
        self.secure_socket = self.context.wrap_socket(sock, server_side=True)

    def listen(self):
        conn, addr = self.secure_socket.accept()
        print(f"connected: {addr}")
        data = conn.recv(2048)
        save_file('test_files/sent_test.txt', data)
