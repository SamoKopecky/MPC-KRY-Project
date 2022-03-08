#!/usr/bin/env python3

import sys

from Client import Client
from Server import Server
from FileUtils import read_file


def print_help():
    print("""usage: User.py [-s] [-c]
    -c  Connect to a server
    -s  Start a server""")
    sys.exit(0)


args = sys.argv[1:]
if len(args) < 1:
    print_help()
if args[0] == "-c":
    client = Client()
    client.connect()
    client.send_file(read_file('test_files/test.txt'))
elif args[0] == "-s":
    server = Server()
    server.listen()
else:
    print_help()
