import io
import socket
import ssl
import sys
import os
import typing

from .Flags import Flags


class Client:
    """
    Handle the client side of the peer. It is not a standalone
    client application.
    """

    def __init__(self, name: str):
        self.flags = Flags()
        self.name = name
        self.certs = os.path.dirname(os.path.abspath(__file__)) + f'{os.sep}..{os.sep}certs'
        self.secure_sock = socket.socket()
        self.context = None
        self.init_sock()
        # Initialize to do nothing for now
        self.confirm_func = lambda: None
        self.available_func = lambda x: None

    def init_sock(self):
        """
        Initialize the `context` that will be used for the ssl socket

        Load certificates, set flags such as if certificates are required
        during the connection creation.
        """
        self.context = ssl.create_default_context()
        self.context.load_cert_chain(f"{self.certs}{os.sep}{self.name}-cert.pem",
                                     f"{self.certs}{os.sep}{self.name}.key")
        self.context.load_verify_locations(f"{self.certs}{os.sep}root.crt")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_REQUIRED

    def connect(self, hostname, port, timeout=120):
        """
        Make a new connection to the socket created from function parameters.

        :param str hostname: IP address of the target
        :param int port: port of the target
        :param int timeout: After how many seconds will the socket timeout
        """
        sock = socket.create_connection((hostname, port))
        sock.settimeout(timeout)
        self.secure_sock = self.context.wrap_socket(sock, server_hostname=hostname)
        print(f"Connected to: {self.secure_sock.getpeername()}")

    def close_conn(self):
        """
        Close the connection created by the `connect` function
        """
        print("Terminating current connection")
        self.secure_sock.shutdown(socket.SHUT_WR)
        self.secure_sock.close()

    def send_heartbeat(self, hostname, port, timeout):
        """
        Send a heartbeat message to the other peer and check if he received it

        :param str hostname: IP address of the target
        :param int port: port of the target
        :param int timeout: After how many seconds is the heartbeat considered dead
        :return: Was the heartbeat successful
        :rtype: bool
        """
        try:
            self.connect(hostname, port, timeout)
        except ConnectionRefusedError:
            print("Connection refused")
            return False
        self.secure_sock.send(self.flags.HEARTBEAT)
        print("Sending heartbeat message")
        try:
            received = self.secure_sock.recv(2048)
        except socket.timeout:
            print("Connection timeout")
            return False
        if received == self.flags.HEARTBEAT:
            print("Received heartbeat back")
            self.available_func(True)
            self.close_conn()
            return True

    def send_file(self, file, file_name):
        """
        Send a named file with contents specified in function parameters

        Send the file contents together with the created header in
        **build_message** function

        :param bytes file: Opened file to send
        :param str file_name: name of the file
        """
        print("Sending header and file data")
        data_to_send = self.build_message(file, file_name)
        self.secure_sock.sendall(data_to_send)
        data = self.secure_sock.recv(2048)
        if data == self.flags.FIN:
            self.confirm_func()
            self.close_conn()
        else:
            print("Something went wrong")
            sys.exit(0)

    def build_message(self, file_bytes, file_name):
        """
        Build the message defined in :doc:`header`

        :param bytes file_bytes: encoded bytes of the file contents
        :param str file_name: name of the file
        """

        binary_length = bin(len(file_bytes)).split("b")[1]
        # Padded to 64 bit length
        binary_length_padded = '0' * (64 - len(binary_length)) + binary_length
        return self.flags.HEADER_START + bytes(binary_length_padded, 'UTF-8') + \
               bytes(file_name, 'UTF-8') + self.flags.HEADER_END + file_bytes + self.flags.DATA_END
