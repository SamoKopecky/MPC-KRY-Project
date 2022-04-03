from .Client import Client
from .Server import Server
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
        file_name = file_path.split("/")[-1]
        file_data = open(file_path, 'rb')
        self.client.send_file(file_data.read(), file_name)
