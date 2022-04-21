from tkinter import *
import tkinter.filedialog

from matplotlib.pyplot import connect
from sklearn.preprocessing import scale
import round_controller
import reccontrol
import serial
import time

class tab3:

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.var = DoubleVar()
        self.barbeginn = 0
        self.barend = 500
        self.buttonframe = LabelFrame(self.frame)
        self.portframe = LabelFrame(self.frame)
        self.measureframe = LabelFrame(self.frame)
        self.myLabel = Label(self.frame, text=' ')
        self.e = Entry(self.buttonframe, width=20, font=('Helvetica', 25))



        self.scrollbar = Scrollbar(self.portframe)
        self.scrollbar.pack( side = RIGHT, fill = Y )

        self.mylist = Listbox(self.portframe, yscrollcommand = self.scrollbar.set )
        for line in range(6):
            self.mylist.insert(END, "COM" + str(line))
        self.mylist.pack()
        self.scrollbar.config( command = self.mylist.yview )



        self.portchoice = Button(self.portframe, text="connect", padx=50,command=self.connect3d)
        self.portchoice.pack()
        self.home = Button(self.portframe, text="home", padx=50,command=self.Homexyz)
        self.home.pack()
        self.disconnecrt = Button(self.portframe, text="disconnnect", padx=50,command=self.disconnect3d)
        self.disconnecrt.pack()
        self.portframe.grid(row=3,column=0)

        #measurepart
        self.xcor = Entry(self.measureframe)
        self.xcor.grid(row = 0,column=1)
        self.L1 = Label(self.measureframe, text="x")
        self.L1.grid(row = 0,column=0)
        self.ycor = Entry(self.measureframe)
        self.ycor.grid(row = 1,column=1)
        self.L2 = Label(self.measureframe, text="y")
        self.L2.grid(row = 1,column=0)
        self.measure = Button(self.measureframe,text='measurebeginn')
        self.measure.grid(row = 2,column=1)
        self.measure.bind('<Button-1>',self.measureprocess)
        self.measureframe.grid(row = 3,column=3)


        # add some buttons
        self.Buttonx = Button(self.buttonframe, text="A axis", padx=50,
                              command=lambda cmd="A axis selected": self.clickit(cmd))
        self.Buttony = Button(self.buttonframe, text="B axis", padx=50,
                              command=lambda cmd="B axis selected": self.clickit(cmd))
        self.Buttonz = Button(self.buttonframe, text="C axis", padx=50,
                              command=lambda cmd="C axis selected": self.clickit(cmd))
        self.Buttonminus = Button(self.buttonframe, text="-", padx=50,
                                  command=lambda cmd="movement minus selected": self.clickit(cmd))
        self.Buttonplus = Button(self.buttonframe, text="+", padx=50,
                                 command=lambda cmd="movement plus selected": self.clickit(cmd))

        #self.Buttonconnectto3d = Button(self.portframe, text="port", padx=50)


        # self.Buttonclockwiserotation = Button(self.frame, text="clockwise", padx=50,
        #                                       command=lambda cmd="clockwise rotation "
        #                                                          "selected ": self.clickit(
        #                                           cmd))

        # self.Buttonanticlockwiserotation = Button(self.frame, text="anticlockwise", padx=50,
        #                                           command=lambda cmd="anticlockwise "
        #                                                              "rotation "
        #                                                              "selected ":
        #                                           self.clickit(cmd))

        # self.Buttonvel = Button(self.buttonframe, text="linear vel", padx=50,
        #                         command=lambda cmd="vel control selected": self.linearvelcontrol(cmd))
        # self.Buttonangvel = Button(self.frame, text="angular vel", padx=50,
        #                            command=lambda cmd=" angular control selected ": self.angularvelcontrol(cmd))
        # self.Buttonconfirm = Button(self.buttonframe, text="enter", padx=50, command=self.confirm)
        # self.Buttonload = Button(self.frame, text="load setting", padx=50, command=self.loadsettingfile)
        # self.Labelofscale = Label(self.buttonframe, text='speed control bar')




        # put the button in the plattform

        self.buttonframe.grid(row=0,column=0)
        self.Buttonx.grid(row=0, column=0)
        self.Buttony.grid(row=0, column=1)
        self.Buttonz.grid(row=0, column=2)
        self.Buttonplus.grid(row=1, column=0)
        # self.Buttonvel.grid(row=1, column=1)
        self.Buttonminus.grid(row=1, column=2)
        # self.Buttonclockwiserotation.grid(row=2, column=0)
        # self.Buttonangvel.grid(row=2, column=1)
        # self.Buttonanticlockwiserotation.grid(row=2, column=2)
        # self.Buttonconfirm.grid(row=3, column=2)
        #self.Buttonload.grid(row=5, column=2)
        self.myLabel.grid(row=6, column=0)
        self.e.grid(row=3, column=1)

        # self.Labelofscale.grid(row=5, column=0)
        """
        moving control
        1.connect to port
        """
        self.ser = None


        self.jj = LabelFrame(self.frame)
        self.jj.grid(row=1, column=0)
        self.jg = LabelFrame(self.frame)
        self.jg.grid(row=1, column=1)


        self.control = round_controller.round_controller(self.jj, self.jj)
        """
        round button control binding 
        
        """

        self.control.canvas.tag_bind(self.control.arclise[0], '<Button-1>', self.ymovingplus2)
        self.control.canvas.tag_bind(self.control.arclise[1], '<Button-1>', self.ymovingplus1)
        self.control.canvas.tag_bind(self.control.arclise[2], '<Button-1>', self.ymovingplus0)

        self.control.canvas.tag_bind(self.control.arclise[3], '<Button-1>', self.xmovingminus2)
        self.control.canvas.tag_bind(self.control.arclise[4], '<Button-1>', self.xmovingminus1)
        self.control.canvas.tag_bind(self.control.arclise[5], '<Button-1>', self.xmovingminus0)

        self.control.canvas.tag_bind(self.control.arclise[6], '<Button-1>', self.ymovingminus2)
        self.control.canvas.tag_bind(self.control.arclise[7], '<Button-1>', self.ymovingminus1)
        self.control.canvas.tag_bind(self.control.arclise[8], '<Button-1>', self.ymovingminus0)

        self.control.canvas.tag_bind(self.control.arclise[9], '<Button-1>', self.xmovingplus2)
        self.control.canvas.tag_bind(self.control.arclise[10], '<Button-1>', self.xmovingplus1)
        self.control.canvas.tag_bind(self.control.arclise[11], '<Button-1>', self.xmovingplus0)



        self.control2 = reccontrol.reccontrol(self.jg,self.jg)
        self.control2.canvas.tag_bind(self.control2.trilist[0], '<Button-1>', self.zmovingminus2)
        self.control2.canvas.tag_bind(self.control2.trilist[1], '<Button-1>', self.zmovingminus1)
        self.control2.canvas.tag_bind(self.control2.trilist[2], '<Button-1>', self.zmovingminus0)
        self.control2.canvas.tag_bind(self.control2.trilist[3], '<Button-1>', self.zmovingplus0)
        self.control2.canvas.tag_bind(self.control2.trilist[4], '<Button-1>', self.zmovingplus1)
        self.control2.canvas.tag_bind(self.control2.trilist[5], '<Button-1>', self.zmovingplus2)
    def measureprocess(self,cmd):
        try:
            self.ser.write(str.encode("G90\r\n"))
            self.ser.write(str.encode("G01"+'X'+self.xcor.get()+'Y'+self.ycor.get()))
            self.ser.write(str.encode("G91\r\n"))
            for i in range(10):
                self.ser.write(str.encode("G01"+'X'+'1'))
        except AttributeError:
            print('no machine connected')

    def hel(self, k):
        print('this func is used to test if the widget between two tag can communcate')


    def linearvelcontrol(self, cmd):
        self.barbegin = 60
        self.barend = 500
        self.scale = Scale(self.buttonframe, variable=self.var, orient=HORIZONTAL, from_=self.barbeginn,
                           to=self.barend, command=self.changethroughslide, length=400)
        self.scale.grid(row=4, column=1)
        self.myLabel.config(text=cmd)

    def angularvelcontrol(self, cmd):
        self.myLabel.config(text=cmd)
        self.barbeginn = 0
        self.barend = 180
        self.scale = Scale(self.buttonframe, variable=self.var, orient=HORIZONTAL, from_=self.barbeginn,
                           to=self.barend, command=self.changethroughslide, length=400)
        self.scale.grid(row=4, column=1)

    def confirm(self):
        self.scale.set(self.e.get())

    def connect3d(self):
        try:
            self.ser = serial.Serial(self.mylist.selection_get(), 115200)
            print(self.mylist.selection_get()+' '+"connected")
        except serial.serialutil.SerialException:
            print('port'+ ' '+ self.mylist.selection_get() +' '+'can not connect' )


    def Homexyz(self):
        try:
            self.ser.write(str.encode("G28\r\n"))
        except AttributeError:
            print('no machine connected')
    def disconnect3d(self):
        try:
            print("disconnect")
            self.ser.close()
            self.ser = None
        except AttributeError:
            print('no machine connected')

    def moving(self,direction,scale):
        print(str(direction)+''+str(scale))
        try:
            self.ser.write(str.encode("G91\r\n"))
            self.ser.write(str.encode("G01"+direction+scale+"\r\n"))
        except AttributeError:
            print("moving machine not conneted yet")


    def xmovingminus0(self,default = 0 ):
        dir = 'X'
        sc = '-0.1'
        self.moving(direction=dir,scale=sc)

    def xmovingplus0(self,default = 0 ):
        dir = 'X'
        sc = '0.1'
        self.moving(direction=dir,scale=sc)

    def xmovingminus1(self, default=0):
        dir = 'X'
        sc = '-1'
        self.moving(direction=dir, scale=sc)

    def xmovingplus1(self, default=0):
        dir = 'X'
        sc = '1'
        self.moving(direction=dir, scale=sc)

    def xmovingminus2(self, default=0):
        dir = 'X'
        sc = '-10'
        self.moving(direction=dir, scale=sc)

    def xmovingplus2(self, default=0):
        dir = 'X'
        sc = '10'
        self.moving(direction=dir, scale=sc)



    def ymovingminus0(self,default = 0 ):
        dir = 'Y'
        sc = '-0.1'
        self.moving(direction=dir,scale=sc)

    def ymovingplus0(self,default = 0 ):
        dir = 'Y'
        sc = '0.1'
        self.moving(direction=dir,scale=sc)

    def ymovingminus1(self, default=0):
        dir = 'Y'
        sc = '-1'
        self.moving(direction=dir, scale=sc)

    def ymovingplus1(self, default=0):
        dir = 'Y'
        sc = '1'
        self.moving(direction=dir, scale=sc)

    def ymovingminus2(self, default=0):
        dir = 'y'
        sc = '-10'
        self.moving(direction=dir, scale=sc)

    def ymovingplus2(self, default=0):
        dir = 'Y'
        sc = '10'
        self.moving(direction=dir, scale=sc)



    def zmovingminus2(self,default = 0 ):
        dir = 'Z'
        sc = '-10'
        self.moving(direction=dir,scale=sc)
    def zmovingminus1(self,default = 0 ):
        dir = 'Z'
        sc = '-1'
        self.moving(direction=dir,scale=sc)
    def zmovingminus0(self,default = 0 ):
        dir = 'Z'
        sc = '-0.1'
        self.moving(direction=dir,scale=sc)

    def zmovingplus2(self,default = 0 ):
        dir = 'Z'
        sc = '10'
        self.moving(direction=dir,scale=sc)
    def zmovingplus1(self,default = 0 ):
        dir = 'Z'
        sc = '1'
        self.moving(direction=dir,scale=sc)
    def zmovingplus0(self,default = 0 ):
        dir = 'Z'
        sc = '0.1'
        self.moving(direction=dir,scale=sc)







if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)

    tab3(root, root)

    root.mainloop()
