import ssl
import socket
import os
import threading

from .utils import save_file
from .Flags import Flags


class Server(threading.Thread):
    def __init__(self, port: int, ip: str, flags: Flags, file_location: str, name: str):
        super().__init__()
        self.context = ssl.SSLContext
        self.ip = ip
        self.port = port
        self.name = name
        self.flags = flags
        self.file_location = file_location
        self.secure_socket = None
        self.certs = os.path.dirname(os.path.abspath(__file__)) + '/../../certs'

    def run(self) -> None:
        self.init_sock()
        while True:
            for done_percent in self.receive(self.file_location, self.start_listening()):
                print(f"Received {done_percent}%")

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

    def start_listening(self) -> socket.socket:
        print(f"receiving on {self.ip, self.port}")
        conn, addr = self.secure_socket.accept()
        print(f"connected to {addr}")
        return conn

    def receive(self, file_path: str, conn: socket.socket):
        # Header received
        raw_data = conn.recv(2048)
        file_len, file_name, file_data = self.parse_header(raw_data)
        original_len = file_len
        yielded_value = 0
        while True:
            try:
                raw_data = conn.recv(2048)
            except (ConnectionResetError, TimeoutError):
                print("Connection error")
                break
            if raw_data[-len(self.flags.DATA_END):] == self.flags.DATA_END:
                file_data += raw_data[:-len(self.flags.DATA_END)]
                break
            file_data += raw_data
            file_len -= len(raw_data)
            # Do this without making calculations every round
            received = 100 - round(file_len / original_len * 100)
            if received % 5 == 0 and yielded_value != received:
                yielded_value = received
                yield received
        print("received file asking client to end connection")
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



