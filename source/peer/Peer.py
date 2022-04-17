import os
import subprocess
from time import sleep

from .Client import Client
from .Server import Server


class Peer:
    """
    Connect the server and client together to create the application's peer
    """

    def __init__(self, name: str, port: int):
        # Listen for all connections
        self.server_address = '0.0.0.0'
        self.listen_port = port
        self.name = name
        self.retries = 3
        self.timeout = 2
        self.server: Server
        self.client = Client(self.name)

    def listen(self, progress_handler, gui_init):
        """
        Create a server object and start the listening thread

        Very simple function which only passes some arguments to the server
        object constructor and starts the listening thread from the outside.

        :param str -> Any progress_handler: handle the information about file sending progress
        :param (int, bytes) -> Any gui_init: initialize GUI when message header is received
        """
        self.server = Server(self.listen_port, self.server_address, self.name, progress_handler, gui_init)
        self.server.start()

    def send_file(self, hostname, port, file_path, gui_update):
        """
        Connect to the specified socket and send a file contents + header

        Decide if the file should be sent now or in a background process depending
        on the status of the other peer.

        :param str hostname: IP address of the target
        :param int port: port of the target
        :param str file_path: path to the to-be-sent file
        :param function gui_update: Refresh the GUI to update some elements
        """
        if not self.is_alive(hostname, port):
            self.client.available_func(False)
            print("Creating a subprocess for sending a file")
            command = f'{os.path.abspath("app.py")} -bg {hostname} {str(port)} {file_path} {self.name}'
            subprocess.Popen(command, shell=True)
            # Stop sending file in this process
            return
        else:
            self.client.available_func(True)
        gui_update()
        self.client.connect(hostname, port)
        file_bytes, file_name = self.file_open_name(file_path)
        self.client.send_file(file_bytes, file_name)

    def is_alive(self, hostname, port):
        """
        Try to send a heartbeat message a specified amount of times

        :param str hostname: IP address of the target
        :param int port: port of the target
        :return: Is the other peer available
        :rtype: bool
        """
        for i in range(self.retries):
            if self.client.send_heartbeat(hostname, port, self.timeout):
                return True
            else:
                print(f"Peer not accessible trying again ({i + 1}/{self.retries})")
                continue
        print("Peer not accessible")
        return False

    def background_send(self, hostname, port, file_path, loop_interval):
        """
        Try to send a file every `loop_interval` amount of seconds

        :param str hostname: IP address of the target
        :param int port: port of the target
        :param str file_path: File path of the sending file
        :param int loop_interval: Amount of seconds to wait before checking again
        """
        file_bytes, file_name = self.file_open_name(file_path)
        while not self.client.send_heartbeat(hostname, port, self.timeout):
            sleep(loop_interval)
        self.client.connect(hostname, port)
        self.client.send_file(file_bytes, file_name)
        exit(0)

    @staticmethod
    def file_open_name(file_path):
        """
        Get the file name and read it

        :param str file_path: Path to the file
        :return: file contents and its name
        :rtype: (bytes, str)
        """
        file_name = file_path.split("/")[-1]
        file = open(file_path, 'rb')
        file_bytes = file.read()
        file.close()
        return file_bytes, file_name
