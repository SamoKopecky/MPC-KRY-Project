#!/usr/bin/env python3
import threading
from time import sleep
from src.file_transfer.User import User
from src.file_transfer.utils import test_files_dir
from src.gui.MainWindow import main


def start():
    user = User(int(input("port: ")))
    user.listen(f'{test_files_dir()}/')
    for thread in threading.enumerate():
        print(thread.name)

    sleep(1)
    while True:
        file_name = input("file name: ")

        user.send_file('127.0.0.1', f'{test_files_dir()}/{file_name}', int(input("port to send to: ")))


if __name__ == '__main__':
    # main()  # Uncomment for GUI
    start()
