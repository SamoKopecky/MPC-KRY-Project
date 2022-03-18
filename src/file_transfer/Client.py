import socket
import ssl
import sys

from .Flags import Flags


class Client:
    def __init__(self, port: int, hostname: str, flags: Flags):
        self.hostname = hostname
        self.port = port
        self.flags = flags

        self.secure_sock = None
        self.context = None

        self.init_sock()

    def init_sock(self):
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def connect(self):
        sock = socket.create_connection((self.hostname, self.port))
        self.secure_sock = self.context.wrap_socket(sock, server_hostname=self.hostname)
        print(f"connected to {self.secure_sock.getpeername()}")

    def send_file(self, file_bytes, file_name):
        print("sending header + file")
        file_len = f"{len(file_bytes)}"
        data_to_send = \
            self.flags.begin_len + bytes(file_len, 'UTF-8') + self.flags.end_len + \
            bytes(file_name, 'UTF-8') + self.flags.name_end + \
            file_bytes + \
            self.flags.file_end
        self.secure_sock.send(data_to_send)
        data = self.secure_sock.recv(2048)
        if data == self.flags.fin:
            print("ending connection")
            self.secure_sock.shutdown(socket.SHUT_WR)
            self.secure_sock.close()
        else:
            print("something went wrong")
            sys.exit(0)
