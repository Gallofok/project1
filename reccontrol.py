from tkinter import *
import numpy as np
class reccontrol():
    def __init__(self, root, frame):

        self.root = root
        self.frame = frame
        self.canvas = Canvas(self.frame, width=200, height=400, borderwidth=0, highlightthickness=0)

        self.colorlis = ["#2ECC71", "#F4D03F", "#5DADE2"]  # green yellow blue
        self.colorlishighlight = ["#28B463", "#F1C40F", "#3498DB"]  # corresponding colors
        self.trilist = []
        for i in range(6):
            
            if np.abs(i-2.5) < 1:
                self.trilist.append(self.canvas.create_rectangle(50,50+i*50,50+100,50+50+i*50,fill = self.colorlis[0],activefill = self.colorlishighlight[0]))
                
            
            if np.abs(i-2.5) < 2 and np.abs(i-2.5) > 1:
                 self.trilist.append(self.canvas.create_rectangle(50+0,50+i*50,50+100,50+50+i*50,fill = self.colorlis[1],activefill = self.colorlishighlight[1]))
            
            if np.abs(i-2.5) > 2:
                 self.trilist.append(self.canvas.create_rectangle(50+0,50+i*50,50+100,50+50+i*50,fill = self.colorlis[2],activefill = self.colorlishighlight[2]))

        self.canvas.create_text(175,100,text='-z')
        self.canvas.create_text(175,300,text='+z')
        self.canvas.pack()



if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)

    reccontrol(root, root)

    root.mainloop()
