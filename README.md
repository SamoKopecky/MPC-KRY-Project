# MPC-KRY-Project

School project for BUTs MPC-KRY subject.

# How to run

- `Python3.8` is the recommended version, but the app can probably run even on lower python versions
- Before installing dependencies it is recommended to create a virtual environment, refer to
  the [guides below](#how-to-create-a-virtual-environment)
- Install `tkinter` dependency based on which OS you are on:
    - Debian/Ubuntu `apt-get install python3-tk`
    - Fedora/RHEL: `dnf install python3-tkinter`
- Install dependencies by running `pip3 install -r requirements.py` in the project root directory
- Run by launching the `app.py` file in the projects root directory with `./app.py`
- The best way to run this on Windows is to
  install [WSL (Windows Subsystem for Linux)](https://docs.microsoft.com/en-us/windows/wsl/install) or create a Linux
  vritual machine

## How to create a virtual environment

- Create a virtual environment with `python3 -m venv path/to/myenv`
- Start using venv with `source path/to/myenv/bin/activate`

# Documentation

- You can browse the documentation either in code or by visiting [this](http://172.105.249.59:6060) website
- The hosted documentation is created using [shpinx](https://www.sphinx-doc.org/en/master/)
    - Configuration files for creating the documentation are in the `sphinx` folder
    - In order to build the website from code documentation install `sphinx` with `pip3 install sphinx`
    - Move to the `sphinx` folder and run `make html`, output folder is `_build/html`
