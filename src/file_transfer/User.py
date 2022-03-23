from time import sleep
from .Client import Client
from .Server import Server
from .utils import read_file, test_files_dir
from .Flags import Flags


class User:
    def __init__(self, port, name):
        self.flags = Flags(b"LEN_B", b"LEN_E", b"FILE_EOF", b"NAME_E", b"FIN")
        self.server_address = '0.0.0.0'
        self.listen_port = port
        self.name = name

    def listen(self, location):
        server = Server(self.listen_port, self.server_address, self.flags, location, self.name)
        server.start()

    def send_file(self, hostname, file_path, port):
        client = Client(port, hostname, self.flags, self.name)
        client.connect()
        client.send_file(read_file(file_path), file_path.split("/")[-1])



