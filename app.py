#!/usr/bin/env python3
import sys

from source.file_transfer.Peer import Peer
from source.gui.Gui import Gui


def main():
    if len(sys.argv) <= 2:
        print("supply a name and port")
        sys.exit(1)

    peer = Peer(sys.argv[1], int(sys.argv[2]))
    gui = Gui(peer.send_file, sys.argv[1], int(sys.argv[2]))
    peer.client.confirm_func = gui.update_confirmation
    peer.listen(gui.progress_handler, gui.start_receive)
    gui.server = peer.server
    gui.mainloop()
    print("Closing sock by connecting from localhost")
    peer.server.stop_loop.set()
    peer.client.connect('127.0.0.1', peer.server.port)
    peer.client.close_conn()


if __name__ == '__main__':
    main()
