from tkinter import *
from tkinter import ttk
from typing import Counter, ValuesView
import sqlite3


class tab1:
    def __init__(self, root, frame):

        self.root = root
        self.frame = frame

        self.TreeFrame = Frame(self.frame)
        self.TreeFrame.pack(pady=10)

        self.TreeScroll = Scrollbar(self.TreeFrame)
        self.TreeScroll.pack(side=RIGHT, fill=Y)

        self.MyTree = ttk.Treeview(self.TreeFrame, yscrollcommand=self.TreeScroll.set, selectmode="extended")
        self.MyTree.pack()

        self.TreeScroll.config(command=self.MyTree.yview)

        self.MyTree['columns'] = ("iD","Firma", "Ansprechpartner", "Straße","Ort","PLZ", "Land")
        self.MyTree.column("#0", width=0, stretch=NO)
        self.MyTree.column("iD", anchor=W, width=40)
        self.MyTree.column("Firma", anchor=W, width=150)
        self.MyTree.column("Ansprechpartner", anchor=W, width=150)
        self.MyTree.column("Straße", width=0, stretch=NO)
        self.MyTree.column("Ort", width=0, stretch=NO)
        self.MyTree.column("PLZ", width=0, stretch=NO)
        self.MyTree.column("Land", width=0, stretch=NO)

        self.MyTree.heading("#0", text="", anchor=W)
        self.MyTree.heading("iD", text="iD", anchor=W)
        self.MyTree.heading("Firma", text="Firma", anchor=W)
        self.MyTree.heading("Ansprechpartner", text="Ansprechpartner", anchor=W)
        self.MyTree.heading("Straße", text="", anchor=W)
        self.MyTree.heading("Ort", text="", anchor=W)
        self.MyTree.heading("PLZ", text="", anchor=W)
        self.MyTree.heading("Land", text="", anchor=W)

        self.MyTree.tag_configure('oddrow', background='white')
        self.MyTree.tag_configure('evenrow', background='lightgreen')

        self.DataFrame = LabelFrame(self.frame, text="Kunde")
        self.DataFrame.pack(fill="none", expand="yes", padx=20, pady=10)

        self.FirmaLabel = Label(self.DataFrame, text="Firma")
        self.FirmaLabel.grid(row=0, column=0, sticky=W ,padx=10, pady=2)
        self.FirmaEntry = Entry(self.DataFrame)
        self.FirmaEntry.grid(row=0, column=1, padx=10, pady=2)

        self.AnsprechLabel = Label(self.DataFrame, text="Kontakt")
        self.AnsprechLabel.grid(row=1, column=0, sticky=W ,padx=10, pady=2)
        self.AnsprechEntry = Entry(self.DataFrame)
        self.AnsprechEntry.grid(row=1, column=1, padx=10, pady=2)

        self.StrasseLabel = Label(self.DataFrame, text="Straße")
        self.StrasseLabel.grid(row=2, column=0, sticky=W ,padx=10, pady=2)
        self.StrasseEntry = Entry(self.DataFrame)
        self.StrasseEntry.grid(row=2, column=1, padx=30, pady=2)

        self.StadtLabel = Label(self.DataFrame, text="Ort")
        self.StadtLabel.grid(row=3, column=0, sticky=W ,padx=10, pady=2)
        self.StadtEntry = Entry(self.DataFrame)
        self.StadtEntry.grid(row=3, column=1, padx=10, pady=2)

        self.PlzLabel = Label(self.DataFrame, text="PLZ")
        self.PlzLabel.grid(row=4, column=0, sticky=W ,padx=10, pady=2)
        self.PlzEntry = Entry(self.DataFrame)
        self.PlzEntry.grid(row=4, column=1, padx=10, pady=2)

        self.LandLabel = Label(self.DataFrame, text="Land")
        self.LandLabel.grid(row=5, column=0, sticky=W ,padx=10, pady=2)
        self.LandEntry = Entry(self.DataFrame)
        self.LandEntry.grid(row=5, column=1, padx=10, pady=2)

        ############### Buttons ##################

        self.ButtonFrame = LabelFrame(self.frame, text="")
        self.ButtonFrame.pack(fill="x", expand="yes", padx=20)

        self.button_add_cust = Button(self.ButtonFrame, text=" Einfg ", command=self.add_record)
        self.button_add_cust.grid(row=0, column=0, padx=20, pady=10)

        self.button_update_cust = Button(self.ButtonFrame, text=" Update ", command=self.update_record)
        self.button_update_cust.grid(row=0, column=2, padx=20, pady=10)

        self.button_rem_cust = Button(self.ButtonFrame, text=" Entf ", command=self.remove_record)
        self.button_rem_cust.grid(row=0, column=3, padx=20, pady=10)

        self.button4 = Button(self.ButtonFrame, text="  button 4  ")
        self.button4.grid(row=0, column=4, padx=20, pady=10)

        self.button5 = Button(self.ButtonFrame, text="  button 5  ")
        self.button5.grid(row=0, column=5, padx=20, pady=10)

        self.button6 = Button(self.ButtonFrame, text="  button 6  ")
        self.button6.grid(row=0, column=6, padx=20, pady=10)

        self.button7 = Button(self.ButtonFrame, text="  button 7  ")
        self.button7.grid(row=0, column=7, padx=20, pady=10)

        self.button8 = Button(self.ButtonFrame, text="  button 8  ")
        self.button8.grid(row=0, column=8, padx=20, pady=10)


        self.MyTree.bind("<ButtonRelease-1>",  self.select_record)



    ############### functions ##################

    def query_database(self):
        conn = sqlite3.connect('speck_datenbank.db')
        c_ = conn.cursor()

        c_.execute("SELECT rowid, * FROM customers")
        records = c_.fetchall()

        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                self.MyTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow',))
            else:
                self.MyTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',))
            count += 1    
    
        conn.commit()
        conn.close()



    def clear_entry(self):
        # clear entry boxes
        self.FirmaEntry.delete(0,END)
        self.AnsprechEntry.delete(0,END)
        self.StrasseEntry.delete(0,END)
        self.StadtEntry.delete(0,END)
        self.PlzEntry.delete(0,END)
        self.LandEntry.delete(0,END)

    def select_record(self, dummy):

        self.clear_entry()
        # get selected entry
        selected = self.MyTree.focus()
        values = self.MyTree.item(selected, 'values')

        # put selected items into entries
        self.FirmaEntry.insert(0,values[1])
        self.AnsprechEntry.insert(0,values[2])
        self.StrasseEntry.insert(0,values[3])
        self.StadtEntry.insert(0,values[4])
        self.PlzEntry.insert(0,values[5])
        self.LandEntry.insert(0,values[6])
        


    def update_record(self):
        selected = self.MyTree.focus()
        values = self.MyTree.item(selected, 'values')

        conn = sqlite3.connect('speck_datenbank.db')
        c_ = conn.cursor()

        c_.execute("""UPDATE customers SET
            Firma = :Firma,
            Ansprechpartner = :Ansprechpartner,
            Strasse = :Strasse,
            Ort = :Ort,
            PLZ = :PLZ,
            Land = :Land

            WHERE oid = :oid""",
            {
            'Firma': self.FirmaEntry.get(),
            'Ansprechpartner': self.AnsprechEntry.get(),
            'Strasse': self.StrasseEntry.get(),
            'Ort': self.StadtEntry.get(),
            'PLZ': self.PlzEntry.get(),
            'Land': self.LandEntry.get(),
            'oid': values[0]       
            }
        )
        
        conn.commit()
        conn.close()

        self.MyTree.item(selected, text="", values=(values[0], self.FirmaEntry.get(), self.AnsprechEntry.get(), self.StrasseEntry.get(), self.StadtEntry.get(), self.PlzEntry.get(), self.LandEntry.get()))
        
        self.clear_entry()

    def remove_record(self):
        selected = self.MyTree.focus()
        values = self.MyTree.item(selected, 'values')

        x = self.MyTree.selection()[0]
        self.MyTree.delete(x)

        conn = sqlite3.connect('speck_datenbank.db')
        c_ = conn.cursor()

        c_.execute("DELETE from customers WHERE oid=" + values[0])

        conn.commit()
        conn.close()

        self.clear_entry

        # update tree
        self.MyTree.delete(*self.MyTree.get_children())
        self.query_database()



    # Add customer to database
    def add_record(self):
        conn = sqlite3.connect('speck_datenbank.db')
        c_ = conn.cursor()

        c_.execute("INSERT INTO customers VALUES (:Firma, :Ansprechpartner, :Strasse, :Ort, :PLZ, :Land )",
            {
            'Firma': self.FirmaEntry.get(),
            'Ansprechpartner': self.AnsprechEntry.get(),
            'Strasse': self.StrasseEntry.get(),
            'Ort': self.StadtEntry.get(),
            'PLZ': self.PlzEntry.get(),
            'Land': self.LandEntry.get()           
            }
            )

        self.clear_entry

        conn.commit()
        conn.close()
        # update tree
        self.MyTree.delete(*self.MyTree.get_children())
        self.query_database()


if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)

    tab1(root, frame)

    root.mainloop()











