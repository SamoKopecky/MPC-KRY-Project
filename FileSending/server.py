#!/usr/bin/env python3

import ssl
import socket


context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_cert_chain("root.crt", "root.key")
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind(('127.0.0.1', 8443))
sock.listen(5)

ssock = context.wrap_socket(sock, server_side=True)
conn, addr = ssock.accept()
print(f"connected: {addr}")
print(conn.recv(2048))

conn.close()

