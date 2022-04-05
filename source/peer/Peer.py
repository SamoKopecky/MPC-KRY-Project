from .Client import Client
from .Server import Server
from .Flags import Flags


class Peer:
    """
    Connect the server and client together to create the application's peer
    """

    def __init__(self, name: str, port: int):
        self.flags = Flags(b"HEADER_START", b"HEADER_END", b"DATA_END", b"FIN")
        self.server_address = '0.0.0.0'
        self.listen_port = port
        self.name = name
        self.server: Server
        self.client = Client(self.flags, self.name)

    def listen(self, progress_handler, gui_init):
        """
        Create a server object and start the listening thread

        Very simple function which only passes some arguments to the server
        object constructor and starts the listening thread from the outside.

        :param function progress_handler: handle the information about file sending progress
        :param function gui_init: initialize GUI when message header is received
        """
        self.server = Server(self.listen_port, self.server_address, self.flags, self.name, progress_handler, gui_init)
        self.server.start()

    def send_file(self, hostname, port, file_path):
        """
        Connect to the specified socket and send a file contents + header

        Other then reading a file that is to be sent a very simple function
        which only passes some arguments to the Client object that actually
        does all the work.

        :param str hostname: IP address of the target
        :param int port: port of the target
        :param str file_path: path to the to-be-sent file
        """
        self.client.connect(hostname, port)
        file_name = file_path.split("/")[-1]
        file_data = open(file_path, 'rb')
        self.client.send_file(file_data.read(), file_name)
