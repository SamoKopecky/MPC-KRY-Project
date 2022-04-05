from ..gui.MainGui import MainGui
from ..peer.Peer import Peer


class App:
    """
    Make use of all the other modules to create and actually run
    the application.
    """
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port

    def start_app(self):
        """
        Create the app from modules and run it

        Handle the termination of the server thread if the main thread ends.
        The main thread ends if the GUI part of the applications exists.
        """
        peer = Peer(self.name, self.port)
        gui = MainGui(peer.send_file, self.name, self.port)
        peer.client.confirm_func = gui.update_confirmation
        peer.client.available_func = gui.update_availability
        peer.listen(gui.progress_handler, gui.start_receive)
        gui.server = peer.server
        gui.mainloop()
        print("Closing sock by connecting from localhost")
        peer.server.stop_loop.set()
        peer.client.connect('127.0.0.1', peer.server.port)
        peer.client.close_conn()

    def send_file_background(self, hostname, port, file_path):
        """
        Send a file without creating a GUI

        :param str hostname: IP of the target
        :param int port: ort of the target
        :param str file_path: path to the file
        """
        peer = Peer(self.name, self.port)
        peer.background_send(hostname, port, file_path, 10)
