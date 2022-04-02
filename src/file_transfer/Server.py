import ssl
import socket
import os
import threading

from typing import Callable
from .utils import save_file
from .Flags import Flags


class Server(threading.Thread):
    def __init__(self, port, ip, flags: Flags, name: str, handler, interface_gui_init):
        super().__init__()
        self.context = ssl.SSLContext
        self.ip = ip
        self.port = port
        self.name = name
        self.flags = flags
        self.file_location = "./"
        self.secure_socket = None
        self.certs = os.path.dirname(os.path.abspath(__file__)) + '/../../certs'
        self.handler = handler
        self.interface_gui_init = interface_gui_init
        self.current_conn = socket.socket()

    def run(self) -> None:
        self.init_sock()
        while True:
            # Receive header
            # call gui init function, wait for button clicked -- do this in tinker
            # for loop for yielding results
            self.start_listening()
            data_len, name, data = self.receive_header(self.current_conn)
            self.interface_gui_init(data_len, name)
            self.receive_body(self.file_location, self.current_conn, data_len, name, data)
            for done_percent in self.receive_body(self.file_location, self.current_conn, data_len, name, data):
                self.handler(done_percent)

    def init_sock(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(f"{self.certs}/{self.name}-cert.pem", f"{self.certs}/{self.name}.key")
        self.context.load_verify_locations(f"{self.certs}/root.crt")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_REQUIRED

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind((self.ip, self.port))
        sock.listen(5)
        print(f"bound to {(self.ip, self.port)}")
        self.secure_socket = self.context.wrap_socket(sock, server_side=True)

    def start_listening(self):
        print(f"receiving on {self.ip, self.port}")
        conn, addr = self.secure_socket.accept()
        print(f"connected to {addr}")
        self.current_conn = conn

    def is_fin(self, raw_data):
        if raw_data[-len(self.flags.DATA_END):] == self.flags.DATA_END:
            return True
        return False

    def receive_header(self, conn):
        raw_data = conn.recv(2048)
        return self.parse_header(raw_data)

    def receive_body(self, file_path, conn, file_len, file_name, file_data):
        raw_data = conn.recv(2048)
        original_len = file_len
        yielded_value = 0
        while not self.is_fin(raw_data):
            try:
                raw_data = conn.recv(2048)
            except (ConnectionResetError, TimeoutError):
                print("Connection error")
                break
            if self.is_fin(raw_data):
                file_data += raw_data[:-len(self.flags.DATA_END)]
                break
            file_data += raw_data
            file_len -= len(raw_data)
            # Do this without making calculations every round
            received = 100 - round(file_len / original_len * 100)
            if yielded_value != received and received != 100:
                yielded_value = received
                yield received
        print("received file asking client to end connection")
        yield 100
        conn.send(self.flags.FIN)
        save_file(file_path + file_name.decode() + ".copy", file_data)

    def parse_header(self, data: bytes) -> (int, str, bytes):
        # Header Format:
        # +───────────────+──────────────────────+────────────+─────────────+───────+───────────+──────+
        # | HEADER_START  | FILE_LENGTH [64bit]  | FILE_NAME  | HEADER_END  | DATA  | DATA_END  | FIN  |
        # +───────────────+──────────────────────+────────────+─────────────+───────+───────────+──────+
        if self.flags.HEADER_START not in data:
            exit(1)
        header_end_index = data.index(self.flags.HEADER_END)
        header = data[len(self.flags.HEADER_START):header_end_index]
        file_data = data[header_end_index + len(self.flags.HEADER_END):]
        file_len = int(header[:64], 2)
        file_name = header[64:]
        return file_len, file_name, file_data
