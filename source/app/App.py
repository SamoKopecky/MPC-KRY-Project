from ..gui.MainGui import MainGui
from ..gui.EntryGui import EntryGui
from ..peer.Peer import Peer


class App:
    """
    Make use of all the other modules to create and actually run
    the application.
    """

    def __init__(self, name: str = "", timer_timeout: int = 0):
        self.name = name
        self.port = 0
        self.passwd = ""
        self.timer_timeout = timer_timeout
        self.db = None

    def start_app(self):
        """
        Create the app from modules and run it using the GUI

        Handle the termination of the server thread if the main thread ends.
        The main thread ends if the GUI part of the applications exists.
        """
        # Start entry dialog
        entry = EntryGui()
        entry.mainloop()
        if not entry.data_sent:
            exit(0)

        # Setup variables
        self.name = entry.name
        self.passwd = entry.passwd
        self.port = entry.port
        self.timer_timeout = entry.timeout

        # Start main APP/GUI
        peer = Peer(self.name, self.port, self.passwd, self.timer_timeout)
        gui = MainGui(peer.send_file, self.name, self.port, peer.client.db)
        peer.client.confirm_func = gui.update_confirmation
        peer.client.available_func = gui.update_availability
        peer.listen(gui.progress_handler, gui.start_receive)
        gui.server = peer.server
        gui.mainloop()

        # Used when the mainloop ends by closing the main GUI
        print("Closing sock by connecting from localhost")
        peer.server.stop_loop.set()
        # This is needed to break the server from the while loop
        peer.client.connect('127.0.0.1', peer.server.port)
        peer.client.close_conn()

    def send_file_background(self, hostname, port, file_path, passwd):
        """
        Send a file without creating a GUI

        :param str hostname: IP of the target
        :param int port: ort of the target
        :param str file_path: path to the file
        :param str passwd: Db password
        """

        peer = Peer(self.name, self.port, passwd, self.timer_timeout)
        peer.background_send(hostname, port, file_path, 3)
