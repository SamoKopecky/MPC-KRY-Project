#!/usr/bin/env python3

import sys

from Client import Client
from Server import Server

args = sys.argv[1:]
if args[0] == "-c":
    client = Client()
    client.connect()
elif args[0] == "-s":
    server = Server()
    server.listen()
