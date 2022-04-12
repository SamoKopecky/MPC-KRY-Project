from tkinter import messagebox


def valid_port(port_str):
    """
    Validate port

    :param str port_str: Port in str
    """
    try:
        port = int(port_str)
    except ValueError:
        return False
    if port <= 0 or port > 65535:
        return False
    return True


def error(text):
    """
    Display an GUI error message using the function parameter

    :param str text: error message
    """
    messagebox.showerror("Chyba", text)
