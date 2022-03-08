#!/usr/bin/env python3

import sys

from Client import Client
from Server import Server
from FileUtils import read_file


# TODO:
# Create class
# Implement multithreading with server/client working at the same time or check out setblocking function
# Define flags at one place

def print_help():
    print("""usage: User.py [-s] [-c]
    -c  Connect to a server
    -s  Start a server""")
    sys.exit(0)


port = 8443
args = sys.argv[1:]
if len(args) < 1:
    print_help()
if args[0] == "-c":
    client = Client(port)
    client.connect()
    client.send_file(read_file('test_files/test.pdf'))
elif args[0] == "-s":
    server = Server(port)
    server.listen()
else:
    print_help()
