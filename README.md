# MPC-KRY-Project

School project for BUTs MPC-KRY subject.

# How to run

- Before installing dependencies it is recommended to create a virtual environment, refer
  to [guides below](#how-to-create-a-virtual-environment)
- Install `tkinter` dependency based on which OS you are on:
    - Debian/Ubuntu `apt-get install python3-tk`
    - Fedora/RHEL: `dnf install python3-tkinter`
    - Windows: `tkinter` should be packaged with the standard python library
- Install dependencies by running `pip3 install -r requirements.py` in the project root directory
- Run by launching the `source/app.py` file
    - Linux: `./app.py`
    - Windows: `python3 app.py`

## How to create a virtual environment

### Linux

- Create a virtual environment with `python3 -m venv path/to/myenv`
- Start using venv with `source path/to/myenv/bin/activate`

### Windows

- Create a virtual environment with `python3 -m venv c:\path\to\myenv`
- Start using venv with `TODO`

# Documentation

- You can browse the documentation either in code or by visiting [this](http://172.105.249.59:6060/index.html) website
- The hosted documentation is created using [shpinx](https://www.sphinx-doc.org/en/master/)
    - Configuration files for creating the documentation are in the `sphinx` folder 