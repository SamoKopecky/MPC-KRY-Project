#!/usr/bin/env python3
import sys
import threading
import tkinter
from src.file_transfer.User import User
from src.gui.MainWindow import MainWindow


def main():
    if len(sys.argv) <= 2:
        print("supply a name and port")
        sys.exit(1)

    user = User(sys.argv[1], int(sys.argv[2]))
    gui = MainWindow(tkinter.Tk(), user.send_file, sys.argv[1], int(sys.argv[2]))
    user.client.confirm_func = gui.update_confirmation
    user.listen(gui.start_receive, gui.init_receive)
    gui.server = user.server
    gui.mainloop()


if __name__ == '__main__':
    main()
