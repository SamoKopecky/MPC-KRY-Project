import tkinter
import os
import time

from tkinter import HORIZONTAL, Label, Frame, Entry, Button, ttk, messagebox, IntVar
from src.file_transfer.User import User
from src.file_transfer.utils import test_files_dir


class MainWindow(Frame):
    send_file_path = ""
    socket_address = ""
    save_dir = ""
    # vybrany uživatel z databaze
    vybranyUzivatel = ""

    def __init__(self, parent, send_function):
        super().__init__(parent)
        self.send_function = send_function
        self.parent = parent
        self.parent.minsize(100, 100)
        self.parent.maxsize(1000, 10000)
        self.parent.resizable(True, True)
        self.parent.title("Application")

        Label(self.parent, text="Adresář uložení: ").grid(row=0)
        self.file_path_entry = Entry(self.parent)
        self.file_path_entry.grid(row=0, column=1)
        self.file_path_button = Button(self.parent, text="Zvolit", command=self.choose_save_dir)
        self.file_path_button.grid(row=0, column=2, sticky='w')

        Label(self.parent, text="Cesta k souboru: ").grid(row=1)
        self.save_dir_entry = Entry(self.parent)
        self.save_dir_entry.grid(row=1, column=1)
        self.save_dir_button = Button(self.parent, text="Vyhledat", command=self.choose_send_file)
        self.save_dir_button.grid(row=1, column=2, sticky='w')

        Label(self.parent, text="Název: ").grid(row=2)
        self.name_label = Label(self.parent, text="-")
        self.name_label.grid(row=2, column=1)
        Label(self.parent, text="Velkost: ").grid(row=3)
        self.size_label = Label(self.parent, text="0 B")
        self.size_label.grid(row=3, column=1)

        Label(self.parent, text="Adresa socketu (IP:port): ").grid(row=4)
        self.manual_address_entry = Entry(self.parent)
        self.manual_address_entry.grid(row=4, column=1)
        self.send_from_entry_button = Button(self.parent, text="Odeslat na socket",
                                             command=self.choose_socket_addr)
        self.send_from_entry_button.grid(row=4, column=2, sticky='w')
        self.send_from_db_button = Button(self.parent, text="Odeslat z DB",
                                          command=self.choose_db_addr)
        self.send_from_db_button.grid(row=5, column=2, sticky='W')

        self.file_path_entry.insert(0, "/home")
        self.save_dir_entry.insert(0, "/test.txt")

    def choose_send_file(self):
        self.send_file_path = str(self.save_dir_entry.get())
        self.size_label.configure(text=f"{os.path.getsize(self.send_file_path)} B")
        self.name_label.configure(text=self.send_file_path.split(os.sep)[-1])

    def choose_save_dir(self):
        self.save_dir = str(self.file_path_entry.get())

    def choose_socket_addr(self):
        self.socket_address = str(self.manual_address_entry.get())
        self.send_to_socket(self.socket_address)

    def choose_db_addr(self):
        db_addr = "1.1.1.1:3"
        self.send_to_socket(db_addr)

    def send_to_socket(self, socket_addr):
        slave = tkinter.Tk()
        slave.minsize(100, 100)
        slave.maxsize(1000, 10000)
        slave.title("Send file")

        Label(slave, text=f"Posielanie suboru: {self.name_label.cget('text')}").grid(row=0, sticky="w")
        Label(slave, text=f"Adresa socketu: {socket_addr}").grid(row=1, sticky="w")
        progress_bar = ttk.Progressbar(slave, orient=HORIZONTAL, length=100, mode='indeterminate')
        progress_bar.grid(row=2)

        slave.tkraise()

        addr = socket_addr.split(":")
        self.send_function(addr[0], int(addr[1]), self.send_file_path)

    def init_receive(self, data_len, name):
        watcher = IntVar()
        slave = tkinter.Tk()
        slave.minsize(100, 100)
        slave.maxsize(1000, 10000)
        slave.title("Receive file")

        Label(slave, text="Adresář uložení: ").grid(row=0)
        file_path_entry = Entry(slave)
        file_path_entry.grid(row=0, column=1)
        file_path_button = Button(slave, text="Jiný adresář", command=self.choose_save_dir)
        file_path_button.grid(row=0, column=2, sticky='w')
        if self.save_dir != "":
            file_path_entry.insert(0, self.save_dir)

        Label(slave, text=f"Název: ").grid(row=2)
        name_label = Label(slave, text=name.decode('UTF-8'))
        name_label.grid(row=2, column=1)
        Label(slave, text=f"Velkost: ").grid(row=3)
        size_label = Label(slave, text=f"{data_len} B")
        size_label.grid(row=3, column=1)

        accept_button = Button(slave, text="Příjmout soubor", command=lambda: watcher.set(1))
        accept_button.grid(row=4, column=0, sticky='w')


    def start_receive(self, received):
        print(received)

