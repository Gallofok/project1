from tkinter import *
import tkinter.filedialog

class tab1:

    def __init__(self,root,frame):
        self.root = root
        self.frame = frame
        self.barbeginn = 0
        self.barend = 100

        self.myLabel = Label(self.root, text=' ')
        

        self.e = Entry(width=50, font=('Helvetica', 24))
        
        self.e.insert(0, "65")

        
        # add some buttons
        self.Buttonx = Button(root, text="X axis", padx=50, command=lambda cmd="x axis selected": self.clickit(cmd))
        self.Buttony = Button(root, text="Y axis", padx=50, command=lambda cmd="y axis selected": self.clickit(cmd))
        self.Buttonz = Button(root, text="Z axis", padx=50, command=lambda cmd="z axis selected": self.clickit(cmd))
        self.Buttonminus = Button(root, text="-", padx=100, command=lambda cmd="movement minus selected": self.clickit(cmd))
        self.Buttonclockwiserotation = Button(root, text="clockwise rotation", padx=50, command=lambda cmd="clockwise rotation "
                                                                                                      "selected ": self.clickit(
            cmd))

        self.Buttonanticlockwiserotation = Button(root, text="anticlockwise rotation", padx=50,
                                             command=lambda cmd="anticlockwise "
                                                                "rotation "
                                                                "selected ":
                                             self.clickit(cmd))

        self.Buttonvel = Button(root, text="linear vel", padx=50,
                           command=lambda cmd="vel control selected": self.linearvelcontrol(cmd))
        self.Buttonangvel = Button(root, text="angular vel", padx=50,
                              command=lambda cmd=" angular control selected ": self.angularvelcontrol(cmd))
        self.Buttonconfirm = Button(root, text="enter", padx=50, command=self.confirm)
        self.Buttonload = Button(root, text="load setting", padx=50, command=self.loadsettingfile)

        # put the button in the plattform
        self.Buttonx.grid(row=0, column=0)
        self.Buttony.grid(row=0, column=1)
        self.Buttonz.grid(row=0, column=2)
        self.Buttonplus.grid(row=1, column=0)
        self.Buttonvel.grid(row=1, column=1)
        self.Buttonminus.grid(row=1, column=2)
        self.Buttonclockwiserotation.grid(row=2, column=0)
        self.Buttonangvel.grid(row=2, column=1)
        self.Buttonanticlockwiserotation.grid(row=2, column=2)
        self.Buttonconfirm.grid(row=3, column=2)
        self.Buttonload.grid(row=5, column=2)
        self.myLabel.grid(row=6, column=1)
        self.e.grid(row=3, column=1)
        self.scale.grid(row=4, column=1)
        self.Labelofscale.grid(row=5, column=1)
        
        self.scale = Scale(self.root, variable=DoubleVar(), orient=HORIZONTAL, from=self.barbeginn, to= self.barend)
        

        self.Labelofscale = Label(self.root, text='this is speed control bar')
        
    #def fine some basic functions
    def clickit(self,cmd):
        self.myLabel.config(text=cmd)

    def linearvelcontrol(self,cmd):
        self.myLabel.config(text=cmd)

        self.barbegin = 60
        self.barend = 1600



    def angularvelcontrol(self,cmd):
        self.myLabel.config(text=cmd)
        self.barbeginn = 0
        self.barend = 180
        scale = Scale(self.root, variable=DoubleVar(), orient=HORIZONTAL, from = self.barbeginn, to=self.barend)
        scale.grid(row=4, column=1)


    def confirm(self):
        self.scale.set(self.e.get())
    def loadsettingfile(self):
        tkinter.filedialog.askopenfilename(title="load setting file")


    #this is message box



    #this input box will be used to control vel


