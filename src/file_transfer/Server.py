import ssl
import socket
import sys
import os

from .FileUtils import save_file
from .Flags import Flags


# TODO:
# File extension/make a header for file info
# Proper logging
# Docs


class Server:

    def __init__(self, port: int, hostname: str, flags: Flags):
        self.context = ssl.SSLContext
        self.secure_socket = None
        self.hostname = hostname
        self.port = port
        self.certs = os.path.dirname(os.path.abspath(__file__)) + '/../../certs'
        self.flags = flags

    def init_sock(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.context.load_cert_chain(f"{self.certs}/root.crt", f"{self.certs}/root.key")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind((self.hostname, self.port))
        sock.listen(5)
        print(f"bound to {(self.hostname, self.port)}")
        self.secure_socket = self.context.wrap_socket(sock, server_side=True)

    def start_listening(self) -> socket.socket:
        print(f"receiving on {self.hostname, self.port}")
        conn, addr = self.secure_socket.accept()
        print(f"connected to {addr}")
        return conn

    def receive(self, file_path: str, conn: socket.socket):
        # Header received
        raw_data = conn.recv(2048)
        len_end_flag_idx = raw_data.index(self.flags.end_len)
        if raw_data[:len(self.flags.begin_len)] == self.flags.begin_len:
            data_len = int(raw_data[len(self.flags.begin_len):len_end_flag_idx])
        else:
            print('no file length received exiting')
            sys.exit(1)

        print("received header, waiting for file")
        # Remove header from useful data
        file_data = raw_data[len_end_flag_idx + len(self.flags.end_len):]
        original_len = data_len
        data_len -= len(file_data)

        # Receive rest of useful data
        yielded_value = 0
        while True:
            # print(data_len)
            try:
                raw_data = conn.recv(2048)
            except (ConnectionResetError, TimeoutError):
                print("Connection error")
                break
            if raw_data[-len(self.flags.file_end):] == self.flags.file_end:
                file_data += raw_data[:-len(self.flags.file_end)]
                break
            file_data += raw_data
            data_len -= len(raw_data)
            # Do this without making calculations every round
            received = 100 - round(data_len / original_len * 100)
            if received % 5 == 0 and yielded_value != received:
                yielded_value = received
                yield received
        print("received file asking client to end connection")
        conn.send(self.flags.fin)
        save_file(f'{self.certs}/{file_path}', file_data)
