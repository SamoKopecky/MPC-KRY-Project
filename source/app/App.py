from ..gui.Gui import Gui
from ..file_transfer.Peer import Peer


class App:
    def __init__(self, name, port):
        """
        THis is init method
        :param name:
        :param port:
        """
        self.name = name
        self.port = port

    def start_app(self):
        """
        this is a commend

        :return:
        """
        peer = Peer(self.name, self.port)
        gui = Gui(peer.send_file, self.name, self.port)
        peer.client.confirm_func = gui.update_confirmation
        peer.listen(gui.progress_handler, gui.start_receive)
        gui.server = peer.server
        gui.mainloop()
        print("Closing sock by connecting from localhost")
        peer.server.stop_loop.set()
        peer.client.connect('127.0.0.1', peer.server.port)
        peer.client.close_conn()
