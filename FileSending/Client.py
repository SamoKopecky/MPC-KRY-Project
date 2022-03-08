#!/usr/bin/env python3

import socket
import ssl


# TODO:
# Proper logging
# Docs


class Client:
    def __init__(self):
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.hostname = "127.0.0.1"
        self.port = 8443
        self.secure_socket = ssl.SSLSocket

    def connect(self):
        sock = socket.create_connection((self.hostname, self.port))
        self.secure_sock = self.context.wrap_socket(sock, server_hostname=self.hostname)
        print(f"connected: {self.secure_sock.getpeername()}")

    def send_file(self, file_bytes):
        print("sending file")
        self.secure_sock.send(file_bytes)
