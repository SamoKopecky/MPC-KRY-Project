import os
import socket

from tkinter import Label, Entry, Button, IntVar, Tk, Listbox, END
from .utils import valid_port, error
from .Gui import Gui
from ..db.Database import Database


class MainGui(Gui):
    """
    Define the main GUI of the application
    """

    def __init__(self, send_function, name: str, port: int, db: Database):
        # Tkinter stuff
        super().__init__()
        self.title = f"{name}:{port}"
        self.parent.title(self.title)

        # Mutex variables
        self.save_dir_check = IntVar()
        self.save_dir_check = IntVar()

        # Dynamic labels
        self.confirm_label: Label = Label()
        self.available_label: Label = Label()
        self.unavailable_label: Label = Label()

        # Saved variables
        self.send_file_path = ""
        self.socket_address = ""
        self.save_dir = ""

        # Initialize all required elements
        self.file_path_entry = Entry(self.parent)
        self.file_path_button = Button(self.parent, text="Zvolit", command=self.choose_save_dir)
        self.saved_path_entry = Label(self.parent, text="-")
        self.save_dir_entry = Entry(self.parent)
        self.save_dir_button = Button(self.parent, text="Vyhledat", command=self.choose_send_file_path)
        self.name_label = Label(self.parent, text="-")
        self.size_label = Label(self.parent, text="0 B")
        self.manual_address_entry = Entry(self.parent)
        self.send_from_entry_button = Button(
            self.parent, text="Odeslat na socket", command=self.choose_socket_addr)
        self.send_from_db_button = Button(
            self.parent, text="Odeslat z DB", command=self.choose_db_addr)
        self.receive_name = Label(self.parent, text="-")
        self.receive_size = Label(self.parent, text="0 B")
        self.receive_button = Button(self.parent, text="Přijmout soubor", command=lambda: self.save_dir_check.set(1))
        self.percentage = Label(self.parent, text="0 %")
        self.new_file_label = Label(self.parent, text="Ne")
        self.listbox = Listbox(self.parent)
        self.create_layout()

        # Linking with server and client
        self.send_function = send_function
        self.server = None

        self.db = db
        self.refresh_list()

        # Temporary, delete later!
        self.file_path_entry.insert(0, "/home/samo/receive")
        self.save_dir_entry.insert(0, "/home/samo/send/test.txt")
        self.manual_address_entry.insert(0, "127.0.0.1:")

    def create_layout(self):
        """
        Set the grid layout for all the gui elements
        """
        # 0
        Label(self.parent, text="Adresář uložení: ").grid(row=0)
        self.file_path_entry.grid(row=0, column=1)
        self.file_path_button.grid(row=0, column=2, sticky='w')
        Label(self.parent, text="Použité adresy:", font=('Arial', 12)).grid(row=0, column=4)

        # 1
        Label(self.parent, text="Uložený adresář: ").grid(row=1)
        self.saved_path_entry.grid(row=1, column=1)
        self.listbox.grid(row=1, column=4, rowspan=9)

        # 2
        Label(self.parent, text="Cesta k souboru: ").grid(row=2)
        self.save_dir_entry.grid(row=2, column=1)
        self.save_dir_button.grid(row=2, column=2, sticky='w')

        # 3
        Label(self.parent, text="Název: ").grid(row=3)
        self.name_label.grid(row=3, column=1)

        # 4
        Label(self.parent, text="Velkost: ").grid(row=4)
        self.size_label.grid(row=4, column=1)
        self.send_from_db_button.grid(row=4, column=2, sticky='W')

        # 5
        Label(self.parent, text="Socket (IP:port): ").grid(row=5)
        self.manual_address_entry.grid(row=5, column=1)
        self.send_from_entry_button.grid(row=5, column=2, sticky='w')

        # 6
        Label(self.parent, text="Příjmaný soubor:", font=('Arial', 18)).grid(row=6, column=1)

        # 7
        Label(self.parent, text=f"Název: ").grid(row=7)
        self.receive_name.grid(row=7, column=1)

        # 8
        Label(self.parent, text=f"Velkost: ").grid(row=8)
        self.receive_size.grid(row=8, column=1)
        self.receive_button.grid(row=8, column=2, sticky='w')

        # 9
        Label(self.parent, text=f"Přijatých procent: ").grid(row=9)
        self.percentage.grid(row=9, column=1)

        # 10
        Label(self.parent, text=f"Nový soubor: ").grid(row=10)
        self.new_file_label.grid(row=10, column=1)

    def choose_send_file_path(self):
        """
        Extract, check and save the file path of the file to be sent
        """
        new_path = str(self.save_dir_entry.get())
        if not self.valid_path(new_path):
            error("Neplatná cesta!")
            return
        self.send_file_path = new_path
        # Display information about the file
        self.size_label.configure(text=self.convert_data_len(os.path.getsize(self.send_file_path)))
        self.name_label.configure(text=self.send_file_path.split(os.sep)[-1])

    def choose_save_dir(self):
        """
        Extract, check and save the directory path for saving received files
        """
        new_path = str(self.file_path_entry.get())
        if not self.valid_path(new_path):
            error("Neplatná cesta!")
            return
        elif new_path[-1] == os.sep:
            error("Lomitko nesmí být na konci cesty!")
        else:
            # receive_check variable is used when the save dir was not entered before receiving a file
            self.save_dir_check.set(1)
            self.save_dir = new_path
            self.saved_path_entry.configure(text=f"{self.save_dir}")
            self.save_dir_check.set(0)

    def choose_socket_addr(self):
        """
        Extract and save the manual socket address, send file to that address
        """
        # add_check is used
        self.socket_address = str(self.manual_address_entry.get())
        self.send_to_socket(self.socket_address)

    def choose_db_addr(self):
        """
        Send file to an address selected in the listbox
        """
        if len(self.listbox.curselection()) == 0:
            error("Nebyl vybrán žádny řádek!")
            return
        selected = self.listbox.curselection()[0]
        addr = self.listbox.get(selected, selected)[0]
        self.send_to_socket(addr)

    def refresh_list(self):
        """
        Refresh list of users
        """
        self.listbox.delete(0, END)
        index = 0
        for item in self.db.get_table(Database.users):
            self.listbox.insert(index, item[1])
            index += 1

    def send_to_socket(self, socket_addr):
        """
        Check and send file to the socket address

        Is called by the `client` part of the peer when sending a file.
        Validate the socket address and whether a the file path was chosen.

        :param str socket_addr: destination socket for the file
        """
        if not self.valid_addr(socket_addr):
            error("Špatně zadána adresa!")
            return
        addr = socket_addr.split(":")
        ip = addr[0]
        port = int(addr[1])

        if self.send_file_path == "":
            error("Nebyl vybrán žádný soubor!")
            return

        slave = self.create_send_gui(socket_addr)
        slave.update()

        self.send_function(ip, port, self.send_file_path, slave.update, self.refresh_list)

    def create_send_gui(self, socket_addr):
        """
        Create new GUI window used for sending a file

        Create a new GUI window for displaying what file is being sent, whether
        a confirmation from the other peer was received and if the other peer
        is available.

        :param str socket_addr: destination socket for the file
        :return: A created GUI
        :rtype: tkinter.Tk
        """
        slave = Tk()
        slave.title(self.title)
        self.available_label = Label(slave, text="...")
        self.confirm_label = Label(slave, text="...")
        self.unavailable_label = Label(slave, text="")

        # 0
        Label(slave, text="Zasílaný soubor: ").grid(row=0, sticky="w")
        Label(slave, text=self.name_label.cget('text')).grid(row=0, column=1, sticky="w")

        # 1
        Label(slave, text="Adresa socketu: ").grid(row=1, sticky="w")
        Label(slave, text=socket_addr).grid(row=1, column=1, sticky="w")

        # 2
        Label(slave, text=f"Je peer dostupný: ").grid(row=2, sticky="w")
        self.available_label.grid(row=2, column=1, sticky="w")

        # 3
        Label(slave, text=f"Potvrzení od cíle: ").grid(row=3, sticky="w")
        self.confirm_label.grid(row=3, column=1, sticky="w")

        return slave

    def update_confirmation(self):
        """
        GUI update function for the `client` peer when FIN flag was received
        """
        self.confirm_label.configure(text="Ano", fg="#319e12")  # Green

    def update_availability(self, available):
        """
        GUI update function for the peer checking the availability of
        the other peer

        :param bool available: If the peer is available
        """
        if available:
            self.available_label.configure(text="Ano", fg="#319e12")  # Green
        else:
            self.available_label.configure(text="Ne", fg="#ff0000")  # Red
            self.unavailable_label.grid(row=4, columnspan=3, rowspan=2)
            self.unavailable_label.configure(text="Peer je nedostupný, posílaní souboru v pozadí")

    def start_receive(self, data_len, name):
        """
        Validate saving directory path, update main GUI for receiving a file

        :param int data_len: Receiving file length
        :param bytes name: Encoded name of the receiving file
        """
        if self.save_dir == "":
            error("Cílový adresář je prázdný!")
            # Wait until a directory os choosen
            self.wait_variable(self.save_dir_check)
        self.server.file_location = self.save_dir
        self.receive_size.configure(text=self.convert_data_len(data_len))
        self.receive_name.configure(text=f"{name.decode('UTF-8')}")
        self.new_file_label.configure(text="Ano", fg="#ff0000")  # Red
        # Makes sure the peer doesn't receive the file unless he clicks a button.
        self.receive_button.wait_variable(self.save_dir_check)
        self.new_file_label.configure(text="Ne", fg="#000000")  # Black
        self.save_dir_check.set(0)

    def progress_handler(self, received):
        """
        Handle the yielded % from the `server` part of the peer when receiving a file

        :param str received: Percentage received
        """
        self.percentage.configure(text=f"{received} %")

    @staticmethod
    def convert_data_len(data_len):
        """
        Convert bytes to readable format

        :param int data_len: File size in bytes
        :return: Formatted string
        :rtype: str
        """
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while data_len > power:
            data_len /= power
            n += 1
        return f'{int(data_len)} {power_labels[n]}'

    @staticmethod
    def valid_addr(addr):
        """
        Validate socket address

        :param str addr: Socket address to be validated
        :return: Whether the address is valid
        :rtype: bool
        """

        addr = addr.split(":")
        if len(addr) != 2:
            return False

        # Check IP
        ip = addr[0]
        if ip == "":
            return False
        try:
            socket.inet_aton(ip)
        except socket.error:
            return False

        return valid_port(addr[1])

    @staticmethod
    def valid_path(path):
        """
        Validate the path in the function argument

        :param str path: path to be validated
        :return: Whether the path is valid
        :rtype: bool
        """
        return os.path.exists(path)
