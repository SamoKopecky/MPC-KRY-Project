import socket
import ssl
import sys
import os

from .Flags import Flags


class Client:
    """
    Handle the client side of the peer. It is not a standalone
    client application.
    """

    def __init__(self, flags: Flags, name: str):
        self.flags = flags
        self.name = name
        self.certs = os.path.dirname(os.path.abspath(__file__)) + '/../certs'
        self.secure_sock: ssl.SSLSocket
        self.context = None
        self.init_sock()
        self.confirm_func = print

    def init_sock(self):
        """
        Initialize the `context` that will be used for the ssl socket

        Load certificates, set flags such as if certificates are required
        during the connection creation.
        """
        self.context = ssl.create_default_context()
        self.context.load_cert_chain(f"{self.certs}/{self.name}-cert.pem", f"{self.certs}/{self.name}.key")
        self.context.load_verify_locations(f"{self.certs}/root.crt")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_REQUIRED

    def connect(self, hostname, port):
        """
        Make a new connection to the socket created from function parameters.

        :param str hostname: IP address of the target
        :param int port: port of the target
        """
        sock = socket.create_connection((hostname, port))
        self.secure_sock = self.context.wrap_socket(sock, server_hostname=hostname)
        print(f"Connected to: {self.secure_sock.getpeername()}")

    def close_conn(self):
        """
        Close the connection created by the `connect` function
        """
        print("Terminating current connetion")
        self.secure_sock.shutdown(socket.SHUT_WR)
        self.secure_sock.close()

    def send_file(self, file_bytes, file_name):
        """
        Send a named file with contents specified in function parameters

        Send the file contents together with the created header in
        **build_message** function

        :param bytes file_bytes: encoded bytes of the file contents
        :param str file_name: name of the file
        """
        print("Sending header and file data")
        data_to_send = self.build_message(file_bytes, file_name)
        self.secure_sock.sendall(data_to_send)
        data = self.secure_sock.recv(2048)
        if data == self.flags.FIN:
            self.confirm_func()
            self.close_conn()
        else:
            print("something went wrong")
            sys.exit(0)

    def build_message(self, file_bytes, file_name):
        """
        Build the message defined in :doc:`header`

        :param bytes file_bytes: encoded bytes of the file contents
        :param str file_name: name of the file
        """

        binary_length = bin(len(file_bytes)).split("b")[1]
        binary_length_padded = '0' * (64 - len(binary_length)) + binary_length
        return self.flags.HEADER_START + bytes(binary_length_padded, 'UTF-8') + \
               bytes(file_name, 'UTF-8') + self.flags.HEADER_END + file_bytes + self.flags.DATA_END
