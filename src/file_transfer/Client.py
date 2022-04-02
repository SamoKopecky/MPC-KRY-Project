import socket
import ssl
import sys
import os

from .Flags import Flags


class Client:
    def __init__(self, port: int, ip: str, flags: Flags, name):
        self.ip = ip
        self.port = port
        self.flags = flags
        self.name = name
        self.certs = os.path.dirname(os.path.abspath(__file__)) + '/../../certs'
        self.secure_sock = None
        self.context = None
        self.init_sock()

    def init_sock(self):
        self.context = ssl.create_default_context()
        self.context.load_cert_chain(f"{self.certs}/{self.name}-cert.pem", f"{self.certs}/{self.name}.key")
        self.context.load_verify_locations(f"{self.certs}/root.crt")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_REQUIRED

    def connect(self):
        sock = socket.create_connection((self.ip, self.port))
        self.secure_sock = self.context.wrap_socket(sock, server_hostname=self.ip)
        print(f"connected to {self.secure_sock.getpeername()}")

    def send_file(self, file_bytes, file_name):
        print("sending header + file")
        data_to_send = self.build_header(file_bytes, file_name)
        self.secure_sock.send(data_to_send)
        data = self.secure_sock.recv(2048)
        if data == self.flags.FIN:
            print("ending connection")
            self.secure_sock.shutdown(socket.SHUT_WR)
            self.secure_sock.close()
        else:
            print("something went wrong")
            sys.exit(0)

    def build_header(self, file_bytes, file_name) -> bytes:
        # Header Format:
        # +───────────────+──────────────────────+────────────+─────────────+───────+───────────+──────+
        # | HEADER_START  | FILE_LENGTH [64bit]  | FILE_NAME  | HEADER_END  | DATA  | DATA_END  | FIN  |
        # +───────────────+──────────────────────+────────────+─────────────+───────+───────────+──────+
        binary_length = bin(len(file_bytes)).split("b")[1]
        binary_length_padded = '0' * (64 - len(binary_length)) + binary_length
        return self.flags.HEADER_START + bytes(binary_length_padded, 'UTF-8') + \
               bytes(file_name, 'UTF-8') + self.flags.HEADER_END + file_bytes + self.flags.DATA_END