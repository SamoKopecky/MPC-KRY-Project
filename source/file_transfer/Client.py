import socket
import ssl
import sys
import os

from .Flags import Flags


class Client:
    def __init__(self, flags: Flags, name):
        """
        test test
        :param flags:
        :param name:
        """
        self.flags = flags
        self.name = name
        self.certs = os.path.dirname(os.path.abspath(__file__)) + '/../certs'
        self.secure_sock: ssl.SSLSocket
        self.context = None
        self.init_sock()
        self.confirm_func = print

    def init_sock(self):
        """
        this is init socket function
        :return:
        """
        self.context = ssl.create_default_context()
        self.context.load_cert_chain(f"{self.certs}/{self.name}-cert.pem", f"{self.certs}/{self.name}.key")
        self.context.load_verify_locations(f"{self.certs}/root.crt")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_REQUIRED

    def connect(self, hostname, port):
        sock = socket.create_connection((hostname, port))
        self.secure_sock = self.context.wrap_socket(sock, server_hostname=hostname)
        print(f"Connected to: {self.secure_sock.getpeername()}")

    def close_conn(self):
        print("Terminating current connetion")
        self.secure_sock.shutdown(socket.SHUT_WR)
        self.secure_sock.close()

    def send_file(self, file_bytes, file_name):
        print("Sending header and file data")
        data_to_send = self.build_header(file_bytes, file_name)
        self.secure_sock.sendall(data_to_send)
        data = self.secure_sock.recv(2048)
        if data == self.flags.FIN:
            self.confirm_func()
            self.close_conn()
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
