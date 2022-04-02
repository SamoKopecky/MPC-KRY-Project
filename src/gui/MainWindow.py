import tkinter
import os

from tkinter import Label, Frame, Entry, Button


class MainWindow(Frame):
    send_file_path = ""
    socket_address = ""
    save_dir = ""

    def __init__(self, parent, send_function, name, port):
        super().__init__(parent)
        self.send_function = send_function
        self.server = None
        self.parent = parent
        self.parent.minsize(100, 100)
        self.parent.maxsize(1000, 10000)
        self.parent.resizable(True, True)
        self.parent.title(f"{name}:{port}")
        self.var = tkinter.IntVar()

        Label(self.parent, text="Adresář uložení: ").grid(row=0)
        self.file_path_entry = Entry(self.parent)
        self.file_path_entry.grid(row=0, column=1)
        self.file_path_button = Button(self.parent, text="Zvolit", command=self.choose_save_dir)
        self.file_path_button.grid(row=0, column=2, sticky='w')

        Label(self.parent, text="Ulozeny adresar: ").grid(row=1)
        self.saved_path_entry = Label(self.parent, text="-")
        self.saved_path_entry.grid(row=1, column=1)

        Label(self.parent, text="Cesta k souboru: ").grid(row=2)
        self.save_dir_entry = Entry(self.parent)
        self.save_dir_entry.grid(row=2, column=1)
        self.save_dir_button = Button(self.parent, text="Vyhledat", command=self.choose_send_file)
        self.save_dir_button.grid(row=2, column=2, sticky='w')

        Label(self.parent, text="Název: ").grid(row=3)
        self.name_label = Label(self.parent, text="-")
        self.name_label.grid(row=3, column=1)
        Label(self.parent, text="Velkost: ").grid(row=4)
        self.size_label = Label(self.parent, text="0 B")
        self.size_label.grid(row=4, column=1)

        Label(self.parent, text="Adresa socketu (IP:port): ").grid(row=5)
        self.manual_address_entry = Entry(self.parent)
        self.manual_address_entry.grid(row=5, column=1)
        self.send_from_entry_button = Button(self.parent, text="Odeslat na socket",
                                             command=self.choose_socket_addr)
        self.send_from_entry_button.grid(row=5, column=2, sticky='w')
        self.send_from_db_button = Button(self.parent, text="Odeslat z DB",
                                          command=self.choose_db_addr)
        self.send_from_db_button.grid(row=6, column=2, sticky='W')

        Label(self.parent, text=f"Název: ").grid(row=7)
        self.receive_name = Label(self.parent, text="-")
        self.receive_name.grid(row=7, column=1)
        Label(self.parent, text=f"Velkost: ").grid(row=8)
        self.receive_size = Label(self.parent, text="0 B")
        self.receive_size.grid(row=8, column=1)
        self.receive_button = Button(self.parent, text="Primat", command=lambda: self.var.set(1))
        self.receive_button.grid(row=8, column=2, sticky='w')

        Label(self.parent, text=f"Percenta: ").grid(row=9)
        self.percentage = Label(self.parent, text="0 %")
        self.percentage.grid(row=9, column=1)

        self.file_path_entry.insert(0, "/home/samo")
        self.save_dir_entry.insert(0, "/test.txt")

    def choose_send_file(self):
        self.send_file_path = str(self.save_dir_entry.get())
        self.size_label.configure(text=f"{os.path.getsize(self.send_file_path)} B")
        self.name_label.configure(text=self.send_file_path.split(os.sep)[-1])

    def choose_save_dir(self):
        if str(self.file_path_entry.get())[-1] == os.sep:
            print("Remove separator at the end")
        else:
            self.save_dir = self.file_path_entry.get()
            self.saved_path_entry.configure(text=f"{self.save_dir}")

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

        addr = socket_addr.split(":")
        self.send_function(addr[0], int(addr[1]), self.send_file_path)

    def init_receive(self, data_len, name):
        self.server.file_location = self.save_dir
        self.receive_size.configure(text=f"{data_len} B")
        self.receive_name.configure(text=f"{name.decode('UTF-8')}")
        self.receive_button.wait_variable(self.var)
        self.var.set(0)
        print("test")

    def start_receive(self, received):
        self.percentage.configure(text=f"{received} %")
