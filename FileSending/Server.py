#!/usr/bin/env python3

import ssl
import socket
import sys

from FileUtils import save_file


# TODO:
# Files bigger then 2048 bytes, finish EOF flag after every file and then remove it so it doens't save with the file
# File extension/make a header for file info
# Proper logging
# Docs


class Server:
    len_begin_flag = b"LEN_B"
    len_end_flag = b"LEN_E"
    file_eof = b"FILE_EOF"
    fin_flag = b"FIN"

    def __init__(self, port):
        self.context = ssl.SSLContext
        self.secure_socket = None
        self.hostname = '127.0.0.1'
        self.port = port
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
        raw_data = conn.recv(2048)

        len_end_flag_idx = raw_data.index(self.len_end_flag)
        if raw_data[:len(self.len_begin_flag)] == self.len_begin_flag:
            data_len = int(raw_data[len(self.len_begin_flag):len_end_flag_idx])
            # print(data_len)
        else:
            print('no file length received exiting')
            sys.exit(1)

        file_data = raw_data[len_end_flag_idx + len(self.len_end_flag):]
        data_len -= len(file_data)

        while True:
            # print(data_len)
            try:
                raw_data = conn.recv(8192)
            except (ConnectionResetError, TimeoutError):
                break
            if raw_data[-len(self.file_eof):] == self.file_eof:
                file_data += raw_data[:-len(self.file_eof)]
                break
            file_data += raw_data
            data_len -= len(raw_data)
        conn.send(self.fin_flag)
        save_file('test_files/test_2.pdf', file_data)
