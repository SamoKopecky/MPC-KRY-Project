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
        peer.listen(gui.progress_handler, gui.start_receive)
        gui.server = peer.server
        gui.mainloop()
        print("Closing sock by connecting from localhost")
        peer.server.stop_loop.set()
        peer.client.connect('127.0.0.1', peer.server.port)
        peer.client.close_conn()
