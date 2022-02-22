from tkinter import *
import tkinter.filedialog
import round_controller


class tab3:

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.var = DoubleVar()

        self.barbeginn = 0
        self.barend = 500

        self.myLabel = Label(self.frame, text=' ')
        self.e = Entry(self.frame, width=20, font=('Helvetica', 25))

        # add some buttons
        self.Buttonx = Button(self.frame, text="A axis", padx=50,
                              command=lambda cmd="A axis selected": self.clickit(cmd))
        self.Buttony = Button(self.frame, text="B axis", padx=50,
                              command=lambda cmd="B axis selected": self.clickit(cmd))
        self.Buttonz = Button(self.frame, text="C axis", padx=50,
                              command=lambda cmd="C axis selected": self.clickit(cmd))
        self.Buttonminus = Button(self.frame, text="-", padx=50,
                                  command=lambda cmd="movement minus selected": self.clickit(cmd))
        self.Buttonplus = Button(self.frame, text="+", padx=50,
                                 command=lambda cmd="movement plus selected": self.clickit(cmd))
        self.Buttonclockwiserotation = Button(self.frame, text="clockwise", padx=50,
                                              command=lambda cmd="clockwise rotation "
                                                                 "selected ": self.clickit(
                                                  cmd))

        self.Buttonanticlockwiserotation = Button(self.frame, text="anticlockwise", padx=50,
                                                  command=lambda cmd="anticlockwise "
                                                                     "rotation "
                                                                     "selected ":
                                                  self.clickit(cmd))

        self.Buttonvel = Button(self.frame, text="linear vel", padx=50,
                                command=lambda cmd="vel control selected": self.linearvelcontrol(cmd))
        self.Buttonangvel = Button(self.frame, text="angular vel", padx=50,
                                   command=lambda cmd=" angular control selected ": self.angularvelcontrol(cmd))
        self.Buttonconfirm = Button(self.frame, text="enter", padx=50, command=self.confirm)
        self.Buttonload = Button(self.frame, text="load setting", padx=50, command=self.loadsettingfile)
        self.Labelofscale = Label(self.frame, text='speed control bar')
        self.scale = Scale(self.frame, variable=self.var, orient=HORIZONTAL, from_=self.barbeginn, to=self.barend,
                           command=self.changethroughslide, length=400)

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
        self.myLabel.grid(row=6, column=0)
        self.e.grid(row=3, column=1)
        self.scale.grid(row=4, column=1)
        self.Labelofscale.grid(row=5, column=0)

        self.jj = LabelFrame(self.frame)
        self.jj.grid(row=6, column=1)
        self.jg = LabelFrame(self.frame)
        self.jg.grid(row=6, column=2)
        self.zbar = Scale(self.jg, length=200, background='red')
        self.lab = Label(self.jg, text='+y')
        self.lab.grid(row=0, column=0)
        self.lab2 = Label(self.jg, text='-y')
        self.lab2.grid(row=2, column=0)
        self.zbar.grid(row=1, column=0)
        self.control = round_controller.round_controller(self.jj, self.jj)
        self.control.canvas.tag_bind(self.control.tri1, '<Button-1>', self.hel)

    def hel(self, k):
        print('this func is used to test if the widget between two tag can communcate')

    def changethroughslide(self, value):
        self.e.delete(0, END)
        self.var = value
        self.e.insert(0, str(self.var))

    def clickit(self, cmd):
        self.myLabel.config(text=cmd)

    def linearvelcontrol(self, cmd):
        self.barbegin = 60
        self.barend = 1600
        self.scale = Scale(self.frame, variable=self.var, orient=HORIZONTAL, from_=self.barbeginn,
                           to=self.barend, command=self.changethroughslide, length=400)
        self.scale.grid(row=4, column=1)
        self.myLabel.config(text=cmd)

    def angularvelcontrol(self, cmd):
        self.myLabel.config(text=cmd)
        self.barbeginn = 0
        self.barend = 180
        self.scale = Scale(self.frame, variable=self.var, orient=HORIZONTAL, from_=self.barbeginn,
                           to=self.barend, command=self.changethroughslide, length=400)
        self.scale.grid(row=4, column=1)

    def confirm(self):
        self.scale.set(self.e.get())

    def loadsettingfile(self):
        tkinter.filedialog.askopenfilename(title="load setting file")


if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)

    tab3(root, root)

    root.mainloop()
