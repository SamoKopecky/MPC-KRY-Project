#!/usr/bin/env python3


import socket
import ssl

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
hostname = "127.0.0.1"

sock = socket.create_connection((hostname, 8443))
ssock = context.wrap_socket(sock, server_hostname=hostname)
ssock.send(b"test")
print(ssock.version())


