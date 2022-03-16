#!/usr/bin/env python3

import sys
import os

from datetime import datetime, timedelta

from .Client import Client
from .Server import Server
from .FileUtils import read_file
from .Flags import Flags




class User:
    def __init__(self, port):
        self.flags = Flags(b"LEN_B", b"LEN_E", b"FILE_EOF", b"FIN")
        self.server_address = '0.0.0.0'
        self.port = port
        self.this_file = os.path.dirname(os.path.abspath(__file__))

    def listen(self, location):
        server = Server(self.port, self.server_address, self.flags)
        server.init_sock()
        while True:
            begin = datetime.now().timestamp()
            for done_percent in server.receive(location, server.start_listening()):
                print(f"Received {done_percent}%")
            now = datetime.now().timestamp()
            duration = timedelta(seconds=(now - begin))
            print(f"Done in {duration}")

    def send_file(self, hostname, file_path):
        client = Client(self.port, hostname, self.flags)
        client.connect()
        client.send_file(read_file(f'{self.this_file}/{file_path}'))


def test_user():
    user = User(8444)

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
        user.send_file('127.0.0.1', 'test_files/movie.mkv')
    elif args[0] == "-s":
        user.listen('test_files/movie_copied.mkv')
    else:
        print_help()
