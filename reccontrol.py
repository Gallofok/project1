from tkinter import *
import numpy as np
class reccontrol():
    def __init__(self, root, frame):

        self.root = root
        self.frame = frame
        self.canvas = Canvas(self.frame, width=150, height=350, borderwidth=0, highlightthickness=0)

        self.colorlis = ["#2ECC71", "#F4D03F", "#5DADE2"]  # green yellow blue
        self.colorlishighlight = ["#28B463", "#F1C40F", "#3498DB"]  # corresponding colors
        self.trilist = []
        for i in range(6):
            
            if np.abs(i-2.5) < 1:
                self.trilist.append(self.canvas.create_rectangle(0,i*50,100,50+i*50,fill = self.colorlis[0],activefill = self.colorlishighlight[0]))
                
            
            if np.abs(i-2.5) < 2 and np.abs(i-2.5) > 1:
                 self.trilist.append(self.canvas.create_rectangle(0,i*50,100,50+i*50,fill = self.colorlis[1],activefill = self.colorlishighlight[1]))
            
            if np.abs(i-2.5) > 2:
                 self.trilist.append(self.canvas.create_rectangle(0,i*50,100,50+i*50,fill = self.colorlis[2],activefill = self.colorlishighlight[2]))

        self.canvas.create_text(125,50,text='-z',font='Helvetica 15 bold')
        self.canvas.create_text(125,250,text='+z',font='Helvetica 15 bold')
        self.gg = self.trilist
        self.canvas.pack()



if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)

    reccontrol(root, root)

    root.mainloop()
