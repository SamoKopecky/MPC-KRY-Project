import tkinter
from tkinter import HORIZONTAL
import os
from pathlib import Path
from tkinter import ttk, messagebox
import time


class MainWindow(tkinter.Frame):
    # cela cesta k souboru k odeslání
    celaCesta = ""
    # vybrany uživatel z databaze
    vybranyUzivatel = ""
    # zadana IP adresa
    ipAdresa = ""
    # vybrany adresar pro ulozeni pri prijmu souboru
    vybranyAdresar = ""

    def __init__(self, parent):

        super().__init__(parent)
        self.parent = parent
        self.parent.minsize(100, 100)
        self.parent.maxsize(1000, 10000)
        self.parent.resizable(True, True)
        self.parent.title("Application")

        def functionForFindFile():
            self.parent.minsize(200, 100)

            self.celaCesta = str(e1.get())

            with open(str(self.celaCesta), encoding='utf-8') as soubor:
                obsahSouboru = soubor.read()
                sizeSouboru = os.path.getsize(str(self.celaCesta))
                cesta = Path(self.celaCesta)
                cesta = cesta.parts
                pozice = len(cesta) - 1
                nazev = cesta[pozice]

                vypis = 'NÁZEV: ' + nazev + ' VELIKOST: ' + str(sizeSouboru) + 'B'

                tkinter.Label(self.parent, text=vypis).grid(row=1, column=1)

        def functionForFindDirectory():
            # CESTA DO ADRESARE
            self.vybranyAdresar = str(e3.get())

        def functionForSendWithIPAdress():
            self.parent.minsize(200, 100)
            # ZDE SE VYPISE ZADANA IP ADRESA
            self.ipAdresa = str(e2.get())
            sendWithIP()

        def sendWithIP():
            def step():
                for i in range(5):
                    slave.update_idletasks()
                    zobrazeniProcentBeh['value'] += 20

                    time.sleep(1)
                    if (i == 4):
                        vypisInformaci = "Soubor byl odeslán"

                        ttk.Label(slave, text=vypisInformaci).pack()

            slave = tkinter.Tk()
            slave.geometry('400x150+500+200')
            slave.title("Send file")

            cesta = Path(self.celaCesta)
            cesta = cesta.parts
            pozice = len(cesta) - 1
            nazev = cesta[pozice]

            sizeSouboru = os.path.getsize(str(self.celaCesta))
            vypln = ""
            vypisNazvu = 'Odesílání souboru s názvem: ' + nazev + ' o velikosti:' + str(sizeSouboru) + 'B'
            vypisInformaci = 'Soubor bude odeslán na zvolenou IP adresu: ' + self.ipAdresa

            ttk.Label(slave, text=vypln).pack()
            ttk.Label(slave, text=vypisNazvu).pack()
            ttk.Label(slave, text=vypisInformaci).pack()

            zobrazeniProcentBeh = ttk.Progressbar(slave, orient=HORIZONTAL, length=100, mode='indeterminate')
            zobrazeniProcentBeh.pack(expand=True)

            zobrazeniProcent = ttk.Button(slave, text='Odeslat', command=step)
            zobrazeniProcent.pack()

        def functionForListbox():
            def on_listbox_select(event):
                pozice = listbox.curselection()[0]
                # ZDE SE VYPISE VYBRANY UZIVATEL V DATABAZI PO STISKU NA NEJ
                self.vybranyUzivatel = str(obsahSouboru[pozice])
                print(obsahSouboru[pozice])
                # KONTROLA ZDA BYL VYBRAN SOUBOR PRO ODESLANI
                if (self.celaCesta == ""):
                    messagebox.showerror("ERROR", "Nebyl vybrán žádný soubor k odeslání")
                else:
                    send()

            root = tkinter.Tk()
            root.minsize(100, 100)
            root.maxsize(1000, 10000)
            root.resizable(True, True)
            root.title("Choose Users")

            listbox = tkinter.Listbox(root)
            # TŘEBA ZMĚNIT CESTU!!!!!
            with open('soubor.txt', encoding='utf-8') as soubor:
                obsahSouboru = soubor.read()

            obsahSouboru = obsahSouboru.split("\n")
            for lang in obsahSouboru:
                listbox.insert(tkinter.END, lang)

            listbox.bind("<<ListboxSelect>>", on_listbox_select)
            quitButton = ttk.Button(root, text="Exit", command=exit)

            listbox.pack()
            quitButton.pack()

        def send():
            def step():
                for i in range(5):
                    slave.update_idletasks()
                    # POCITANI PROCENT!!!
                    zobrazeniProcentBeh['value'] += 20
                    # USPANI ABY TO NEBYLO TAK RYCHLE
                    time.sleep(1)
                    if (i == 4):
                        # POKUD SE ZMENI RANGE, MUSI SE ZMENIT I TATO PODMINKA, JINAK NEVYPISE
                        # ZDA BYL PROCES DOKONCEN
                        vypisInformaci = "Soubor byl odeslán"

                        ttk.Label(slave, text=vypisInformaci).pack()

            slave = tkinter.Tk()
            slave.geometry('400x150+500+200')
            slave.title("Send file")

            cesta = Path(self.celaCesta)
            cesta = cesta.parts
            pozice = len(cesta) - 1
            nazev = cesta[pozice]

            sizeSouboru = os.path.getsize(str(self.celaCesta))
            vypln = ""
            vypisNazvu = 'Odesílání souboru s názvem: ' + nazev + ' o velikosti:' + str(sizeSouboru) + 'B'
            vypisInformaci = 'Soubor bude odeslán: ' + self.vybranyUzivatel

            ttk.Label(slave, text=vypln).pack()
            ttk.Label(slave, text=vypisNazvu).pack()
            ttk.Label(slave, text=vypisInformaci).pack()

            zobrazeniProcentBeh = ttk.Progressbar(slave, orient=HORIZONTAL, length=100, mode='indeterminate')
            zobrazeniProcentBeh.pack(expand=True)

            zobrazeniProcent = ttk.Button(slave, text='Odeslat', command=step)
            zobrazeniProcent.pack()

        def functionForReceive():
            def step():
                for i in range(5):
                    slave.update_idletasks()
                    # OPET POCITANI PROCENT
                    zobrazeniProcentBeh['value'] += 20
                    # OPET USPANI, ABY TO SLO POMALEJI
                    time.sleep(1)
                    # A OPET TREBA ZMENIT, POKUD SE ZMENI RANGE!!!!
                    # JINAK NEVYPISE INFO O KONCI PROCESU
                    if (i == 4):
                        vypisInformaci = "Soubor byl přijat"
                        ttk.Label(slave, text=vypisInformaci).pack()

            slave = tkinter.Tk()
            slave.geometry('400x150+500+200')
            slave.title("Send file")

            vypln = ""

            ttk.Label(slave, text=vypln).pack()

            if (self.vybranyAdresar == ""):
                vypisBezAdresare = "Zadejte adresář pro uložení souboru:"
                ttk.Label(slave, text=vypisBezAdresare).pack()

                adresar = tkinter.Entry(slave).pack()
                self.vybranyAdresar = str(adresar)

            else:
                vypisInformaci = 'Soubor bude uložen do: ' + str(self.vybranyAdresar)
                vypisBezAdresare = "Chcete-li změnit umístění uložení, zadejte cestu k novému adresáři:"
                ttk.Label(slave, text=vypisInformaci).pack()
                ttk.Label(slave, text=vypisBezAdresare).pack()
                adresar = tkinter.Entry(slave).pack()

                self.vybranyAdresar = str(adresar)

            zobrazeniProcentBeh = ttk.Progressbar(slave, orient=HORIZONTAL, length=100, mode='indeterminate')
            zobrazeniProcentBeh.pack(expand=True)

            zobrazeniProcent = ttk.Button(slave, text='Přijmout', command=step)
            zobrazeniProcent.pack()

        # HLAVNI OKNO PROGRAMU
        tkinter.Label(self.parent, text="Cesta k souboru").grid(row=0)
        e1 = tkinter.Entry(self.parent)
        e1.grid(row=0, column=1)

        self.buttonOne = tkinter.Button(self.parent, text="Vyhledat", command=functionForFindFile)
        self.buttonOne.grid(row=0, column=2, sticky='w')

        tkinter.Label(self.parent, text="Cesta do adresáře").grid(row=2)
        e3 = tkinter.Entry(self.parent)
        e3.grid(row=2, column=1)

        self.buttonOne = tkinter.Button(self.parent, text="Zvolit", command=functionForFindDirectory)
        self.buttonOne.grid(row=2, column=2, sticky='w')

        vypis = "Odeslat soubor:"

        tkinter.Label(self.parent, text=vypis).grid(row=3, column=1)

        tkinter.Label(self.parent, text="IP adresa, port").grid(row=4)
        e2 = tkinter.Entry(self.parent)
        e2.grid(row=4, column=1)

        self.buttonOne = tkinter.Button(self.parent, text="Odeslat na zadanou IP adresu",
                                        command=functionForSendWithIPAdress)
        self.buttonOne.grid(row=4, column=2, sticky='w')

        self.buttonTwo = tkinter.Button(self.parent, text="Odeslat uživateli v databázi", command=functionForListbox)
        self.buttonTwo.grid(row=5, column=2, sticky='W')

        vypis = "Přijmout soubor:"

        tkinter.Label(self.parent, text=vypis).grid(row=6, column=1)

        self.buttonThree = tkinter.Button(self.parent, text="Přijmout soubor", command=functionForReceive)
        self.buttonThree.grid(row=7, column=1, sticky='s')


def main():
    root = tkinter.Tk()
    app = MainWindow(root)
    app.mainloop()


main()
