from tkinter import Label, Entry, Button
from .utils import valid_port, error
from .Gui import Gui


class EntryGui(Gui):
    """
    Define the entry GUI for entering name, port and password
    """

    def __init__(self):
        super().__init__()
        self.parent.title('p2p app')

        # Initialize all required elements
        self.name_entry = Entry(self.parent)
        self.passwd_entry = Entry(self.parent, show='*')
        self.port_entry = Entry(self.parent)
        self.timeout_entry = Entry(self.parent)
        self.send_button = Button(self.parent, text="OK", command=self.send_data)

        self.name = ''
        self.passwd = ''
        self.port = 0
        self.timeout = 0
        self.data_sent = False

        self.parent.bind('<KeyPress>', self.enter_pressed)

        self.create_layout()

        # Temporary, delete later!
        self.name_entry.insert(0, 'alice')
        self.passwd_entry.insert(0, 'test')
        self.port_entry.insert(0, '8888')
        self.timeout_entry.insert(0, '30')

    def create_layout(self):
        """
        Set the grid layout for all the gui elements
        """
        Label(self.parent, text="P2P aplikace", font=('Arial', 14)).grid(row=0, columnspan=2)

        # 1
        Label(self.parent, text="Jméno: ").grid(row=1)
        self.name_entry.grid(row=1, column=1)

        # 2
        Label(self.parent, text="Heslo: ").grid(row=2)
        self.passwd_entry.grid(row=2, column=1)

        # 3
        Label(self.parent, text="Port: ").grid(row=3)
        self.port_entry.grid(row=3, column=1)

        # 4
        Label(self.parent, text="Čas uložení souboru (s): ").grid(row=4)
        self.timeout_entry.grid(row=4, column=1)

        # 5
        self.send_button.grid(row=5, columnspan=2)

    def send_data(self):
        """
        Save name, port and password to object variables
        """
        if self.name_entry.get() == '' or self.passwd_entry.get() == '':
            error("Jmnéno nebo heslo nemúže být prázdne!")
            return
        self.name = self.name_entry.get()
        self.passwd = self.passwd_entry.get()
        try:
            self.timeout = int(self.timeout_entry.get())
        except ValueError:
            error("Neprávny časovač!")

        if valid_port(self.port_entry.get()):
            self.port = int(self.port_entry.get())
        else:
            error("Nesprávny port!")
            return
        self.data_sent = True
        self.parent.destroy()

    def enter_pressed(self, event):
        """
        Check if enter was pressed, if yes send filled in data

        :param event: press key event
        """
        if event.char == '\r':
            self.send_data()
