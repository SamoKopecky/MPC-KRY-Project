#!/usr/bin/env python3
import sys

from source.app.App import App

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("supply a name and port")
        sys.exit(1)

    app = App(sys.argv[1], int(sys.argv[2]))
    app.start_app()
