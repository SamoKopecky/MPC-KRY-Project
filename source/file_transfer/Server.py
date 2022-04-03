import ssl
import socket
import os
import threading

from .Flags import Flags


class Server(threading.Thread):
    def __init__(self, port, ip, flags: Flags, name: str, progress_handler, interface_gui_init):
        super().__init__()
        self.stop_loop = threading.Event()
        self.ip = ip
        self.port = port
        self.context = ssl.SSLContext
        self.name = name
        self.flags = flags
        self.file_location = "."
        self.certs = os.path.dirname(os.path.abspath(__file__)) + '/../certs'
        self.progress_handler = progress_handler
        self.interface_gui_init = interface_gui_init
        self.secure_socket: ssl.SSLSocket
        self.current_conn: socket

    def run(self) -> None:
        self.init_sock()
        while not self.stop_loop.is_set():
            # Receive header
            # call gui init function, wait for button clicked -- do this in tinker
            # for loop for yielding results
            self.start_listening()
            if self.stop_loop.is_set():
                break
            data_len, name, data = self.receive_header(self.current_conn)
            self.interface_gui_init(data_len, name)
            for done_percent in self.receive_body(self.file_location, self.current_conn, data_len, name, data):
                self.progress_handler(done_percent)

    def init_sock(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(f"{self.certs}/{self.name}-cert.pem", f"{self.certs}/{self.name}.key")
        self.context.load_verify_locations(f"{self.certs}/root.crt")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_REQUIRED

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind((self.ip, self.port))
        sock.listen(5)
        self.secure_socket = self.context.wrap_socket(sock, server_side=True)

    def start_listening(self):
        print(f"Listening on: {self.ip, self.port}")
        self.current_conn, addr = self.secure_socket.accept()
        print(f"New connection at: {addr}")

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
        file = open(f"{file_path}{os.sep}{file_name.decode()}", 'wb')
        file.write(file_data)
        while not self.is_fin(raw_data):
            try:
                raw_data = conn.recv(4096)
            except (ConnectionResetError, TimeoutError):
                print("Connection error")
                break
            if self.is_fin(raw_data):
                file.write(raw_data[:-len(self.flags.DATA_END)])
                break
            file.write(raw_data)
            file_len -= len(raw_data)
            received = 100 - round(file_len / original_len * 100)
            if yielded_value != received and received != 100:
                yielded_value = received
                yield received
        print("Done receiving file, sending FIN")
        yield 100
        conn.send(self.flags.FIN)

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
