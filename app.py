#!/usr/bin/env python3
import sys

from source.app.App import App

if __name__ == '__main__':
    # TODO: Update when DB is finished
    if len(sys.argv) > 1 and sys.argv[1] == "-bg":
        # Used for creating a background file sending process
        app = App(sys.argv[5], int(sys.argv[7]))
        app.send_file_background(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[6])
        exit(0)
    # Used for starting the app with GUI
    app = App()
    app.start_app()
