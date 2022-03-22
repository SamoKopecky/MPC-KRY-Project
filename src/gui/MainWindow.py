import tkinter

from ..file_transfer.User import User


class MainWindow(tkinter.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.minsize(100, 100)
        self.parent.maxsize(1000, 10000)
        self.parent.resizable(True, True)
        self.parent.title("Application")

        def send():
            print("send")

        def functionOne():
            print(textFeildOne.get())

        def listen():
            print("listen")

        tkinter.Label(self.parent, text="Cesta k souboru").grid(row=0)
        textFeildOne = tkinter.Entry(self.parent)
        textFeildOne.grid(row=0, column=1)

        self.buttonOne = tkinter.Button(self.parent, text="Vyhledat", command=functionOne)
        self.buttonOne.grid(row=0, column=2, sticky='w')
        self.buttonTwo = tkinter.Button(self.parent, text="Odeslat uživateli v databázi", command=send)
        self.buttonTwo.grid(row=2, column=1, sticky='s')
        self.buttonThree = tkinter.Button(self.parent, text="Přijmout soubor", command=listen)
        self.buttonThree.grid(row=2, column=2, sticky='s')


def main():
    root = tkinter.Tk()
    app = MainWindow(root)
    app.mainloop()
