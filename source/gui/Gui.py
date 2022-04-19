import os

from tkinter import Label, Tk, PhotoImage


class Gui(Label):
    """
    Define the template class for GUIs
    """

    def __init__(self):
        parent = Tk()
        super().__init__(parent)
        self.parent = parent
        self.parent.iconphoto(True, PhotoImage(
            file=os.path.dirname(os.path.abspath(__file__)) + '/../../vut.png')
                              )
