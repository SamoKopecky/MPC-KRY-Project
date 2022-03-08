#!/usr/bin/env python3

import socket
import ssl

# TODO:
# Proper logging
from time import sleep


class Client:
    def __init__(self):
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.hostname = "127.0.0.1"
        self.port = 8443

    def connect(self):
        with socket.create_connection((self.hostname, self.port)) as sock:
            with self.context.wrap_socket(sock, server_hostname=self.hostname) as secure_sock:
                secure_sock.send(b"test")
