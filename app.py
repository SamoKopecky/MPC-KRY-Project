#!/usr/bin/env python3
import sys

from source.app.App import App

if __name__ == '__main__':
    # TODO: Clean up
    if len(sys.argv) <= 2:
        print("supply a name and port")
        sys.exit(1)
    elif sys.argv[1] == "-bg":
        app = App(sys.argv[5], 0)
        app.send_file_background(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        app = App(sys.argv[1], int(sys.argv[2]))
        app.start_app()
