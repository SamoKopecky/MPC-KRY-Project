#!/usr/bin/env python3

import sys
from time import sleep

from Client import Client
from Server import Server
from FileUtils import read_file
from Flags import Flags


# TODO:
# Implement multithreading with server/client working at the same time or check out setblocking function

class User:
    def __init__(self, port):
        self.flags = Flags(b"LEN_B", b"LEN_E", b"FILE_EOF", b"FIN")
        self.server_address = '0.0.0.0'
        self.port = port

    def listen(self, location):
        server = Server(self.port, self.server_address, self.flags)
        server.init_sock()
        while True:
            server.receive(location, server.start_listening())

    def send_file(self, hostname, file_path):
        client = Client(self.port, hostname, self.flags)
        client.connect()
        client.send_file(read_file(file_path))


user = User(8443)


def print_help():
    # temporary
    print("""usage: User.py [-s] [-c]
    -c  Connect to a server
    -s  Start a server""")
    sys.exit(0)


args = sys.argv[1:]
if len(args) < 1:
    print_help()
if args[0] == "-c":
    user.send_file('127.0.0.1', 'test_files/test.pdf')
elif args[0] == "-s":
    user.listen('test_files/test_2.pdf')
else:
    print_help()
