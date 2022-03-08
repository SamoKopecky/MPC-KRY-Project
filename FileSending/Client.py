#!/usr/bin/env python3

import socket
import ssl


# TODO:
# Proper logging
# Docs
import sys
from time import sleep

# TODO:
# use sendfile function


class Client:
    len_begin_flag = b"LEN_B"
    len_end_flag = b"LEN_E"
    file_eof = b"FILE_EOF"
    fin_flag = b"FIN"

    def __init__(self, port):
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.hostname = "127.0.0.1"
        self.port = port
        self.secure_socket = ssl.SSLSocket

    def connect(self):
        sock = socket.create_connection((self.hostname, self.port))
        self.secure_sock = self.context.wrap_socket(sock, server_hostname=self.hostname)
        print(f"connected: {self.secure_sock.getpeername()}")

    def send_file(self, file_bytes):
        print("sending file")
        file_len = f"{len(file_bytes)}"
        data_to_send = self.len_begin_flag + bytes(file_len, 'UTF-8') + self.len_end_flag + file_bytes + self.file_eof
        self.secure_sock.send(data_to_send)
        data = self.secure_sock.recv(2048)
        if data == self.fin_flag:
            self.secure_sock.shutdown(socket.SHUT_WR)
            self.secure_sock.close()
        else:
            print("something went wrong")
            sys.exit(0)


