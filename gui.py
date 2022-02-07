from tkinter import *

root = Tk()

beginn = 0
end = 100


def clickit(cmd):
    myLabel.config(text=cmd)

def linearvelcontrol(cmd):
    myLabel.config(text=cmd)
    global beginn, end, scale
    beginn = 60
    end = 1600
    scale = Scale(root, variable=DoubleVar(), orient=HORIZONTAL, from_=beginn, to=end)
    scale.grid(row=4, column=1)



def angularvelcontrol(cmd):
    myLabel.config(text=cmd)
    global beginn, end, scale
    beginn = 0
    end = 180
    scale = Scale(root, variable=DoubleVar(), orient=HORIZONTAL, from_=beginn, to=end)
    scale.grid(row=4, column=1)


def confirm():
    scale.set(e.get())


myLabel = Label(root, text=' ')
myLabel.grid(row=6, column=1)

e = Entry(root, width=50, font=('Helvetica', 24))
e.grid(row=3, column=1)
e.insert(0, "65")

Buttonx = Button(root, text="X axis", padx=50, command=lambda cmd="x axis selected": clickit(cmd))
Buttony = Button(root, text="Y axis", padx=50, command=lambda cmd="y axis selected": clickit(cmd))
Buttonz = Button(root, text="Z axis", padx=50, command=lambda cmd="z axis selected": clickit(cmd))
Buttonplus = Button(root, text="+", padx=100, command=lambda cmd="movement plus selected": clickit(cmd))
Buttonminus = Button(root, text="-", padx=100, command=lambda cmd="movement minus selected": clickit(cmd))
Buttonclockwiserotation = Button(root, text="clockwise rotation", padx=50, command=lambda cmd="clockwise rotation "
                                                                                              "selected ": clickit(
    cmd))

Buttonanticlockwiserotation = Button(root, text="anticlockwise rotation", padx=50, command=lambda cmd="anticlockwise "
                                                                                                      "rotation "
                                                                                                      "selected ":
clickit(cmd))

Buttonvel = Button(root, text="linear vel", padx=50, command=lambda cmd="vel control selected": linearvelcontrol(cmd))
Buttonangvel = Button(root, text="angular vel", padx=50,
                      command=lambda cmd=" angular control selected ": angularvelcontrol(cmd))
Buttonconfirm = Button(root, text="enter", padx=50, command=confirm)
Buttonx.grid(row=0, column=0)
Buttony.grid(row=0, column=1)
Buttonz.grid(row=0, column=2)
Buttonplus.grid(row=1, column=0)
Buttonvel.grid(row=1, column=1)
Buttonminus.grid(row=1, column=2)
Buttonclockwiserotation.grid(row=2, column=0)
Buttonangvel.grid(row=2, column=1)
Buttonanticlockwiserotation.grid(row=2, column=2)
Buttonconfirm.grid(row=3, column=2)

scale = Scale(root, variable=DoubleVar(), orient=HORIZONTAL, from_=beginn, to=end)
scale.grid(row=4, column=1)

Labelofscale = Label(root, text='this is speed control bar')
Labelofscale.grid(row=5, column=1)

root.mainloop()
