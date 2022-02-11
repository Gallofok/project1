from tkinter import *
from tkinter import ttk
import sqlite3

from gui_tab1 import *
from gui_tab2 import *
from gui_tab3 import *
############# prepare Database #############
conn = sqlite3.connect('speck_datenbank.db')
c_ = conn.cursor()

c_.execute("""CREATE TABLE if not exists customers (
    Firma text,
    Ansprechpartner text,
    Strasse text,
    Ort text,
    PLZ text,
    Land text)
    """)

conn.commit()
conn.close()


class KalibeR:
    def __init__(self):
        self.root = Tk()
        self.root.title('KalibeR')
        self.root.geometry("1000x1000")
        self.root.minsize(1000, 1000)
        self.root.maxsize(1000, 1000)

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25,
                             fieldbackground="#D3D3D3")
        self.style.map('Treeview', background=[('selected', "#347083")])

        self.my_notebook = ttk.Notebook()
        self.my_notebook.pack(pady=10)

        self.my_frame1 = Frame(self.my_notebook)
        self.my_frame2 = Frame(self.my_notebook)
        self.my_frame3 = Frame(self.my_notebook)
        self.my_frame4 = Frame(self.my_notebook)
        self.basicframe = LabelFrame(self.root, text="Feedbackbox", bg="green",
                    fg="white", padx=15, pady=15)



        inputb = Entry(self.basicframe, width=50, font=('Helvetica', 24))
        positionlabel = Label(self.basicframe,text='this is for feedback')



        inputb.pack()
        positionlabel.pack()
        self.basicframe.pack()
        self.my_frame1.pack(fill="both", expand=1)
        self.my_frame2.pack(fill="both", expand=1)
        self.my_frame3.pack(fill="both", expand=1)
        self.my_frame4.pack(fill="both", expand=1)


        self.my_notebook.add(self.my_frame1, text=" Übersicht ")
        self.my_notebook.add(self.my_frame2, text=" Messungprogramm")
        self.my_notebook.add(self.my_frame3, text=" Manuelle Steuerung ")
        self.my_notebook.add(self.my_frame4, text=" Einstellungen ")

        self.mytab1 = tab3(self.root, self.my_frame1)




    def start(self):
        self.mytab1.query_database()
        self.root.mainloop()


tool = KalibeR()

tool.start()
