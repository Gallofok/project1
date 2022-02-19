from tkinter import *
from tkinter import ttk
from typing import Counter, ValuesView
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.testing.jpl_units import rad


class tab2:



    def __init__(self, root, frame):

        self.root = root
        self.frame = frame
        # self.loadimg = PhotoImage(file="control_xy.png")
        # self.button_add_cust = Button(self.frame, image=self.loadimg)
        # self.button_add_cust.pack()
        self.canvas = Canvas(self.root, width=400, height=400, borderwidth=0, highlightthickness=0 )


        self.centrepos = (100,100)
        self.rad  = (50,40,30)
        self.angstart = (45,135,225,315)
        self.angend = (125,215,305,395)
        self.arclise = []
        self.colorlis = ["#2ECC71","#F4D03F","#5DADE2"]
        self.colorlishighlight = ["#28B463","#F1C40F","#3498DB"]
        for j in range(4):
            for i in range(3):
                self.arclise.append(self.circle_arcit(self.centrepos[0], self.centrepos[1], self.rad[i], fill=self.colorlis[i],
                                                      start=self.angstart[j], end=self.angend[j],
                                                      activefill=self.colorlishighlight[i]))

        for i in range(len(self.arclise)):
            a = i%3
            if a == 0:
                self.canvas.tag_bind(self.arclise[i],'<Button-1>', self.cli)
            if a == 1:
                self.canvas.tag_bind(self.arclise[i], '<Button-1>', self.cli2)
            if a == 2:
                self.canvas.tag_bind(self.arclise[i], '<Button-1>', self.cli3)

        self.canvas.pack()
    def cli(self, event):
        print("HI1")
    def cli2(self, event):
        print("HI2")
    def cli3(self, event):
        print("HI3")

    def circle_arcit(self, x, y, r, **kwargs):
        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs["end"] - kwargs["start"]
            del kwargs["end"]
        return self.canvas.create_arc(x - r, y - r, x + r, y + r, **kwargs)

    def circleit(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)
if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)

    tab2(root,root)

    root.mainloop()

















