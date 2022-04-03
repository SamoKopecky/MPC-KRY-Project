from time import sleep
from .Client import Client
from .Server import Server
from .utils import read_file, test_files_dir
from .Flags import Flags


class User:
    def __init__(self, name, port):
        self.flags = Flags(b"HEADER_START", b"HEADER_END", b"DATA_END", b"FIN")
        self.server_address = '0.0.0.0'
        self.listen_port = port
        self.name = name
        self.server: Server
        self.client = Client(self.flags, self.name)

    def listen(self, handler, init_func):
        self.server = Server(self.listen_port, self.server_address, self.flags, self.name, handler, init_func)
        self.server.start()

    def send_file(self, hostname, port, file_path):
        self.client.connect(hostname, port)
        self.client.send_file(read_file(file_path), file_path.split("/")[-1])
