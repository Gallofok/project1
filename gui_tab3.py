from calendar import c
import threading
from tkinter import *
import tkinter.filedialog
import sys
from matplotlib.pyplot import connect
from sklearn.preprocessing import scale
import round_controller
import reccontrol
import serial
import time
import numpy as np
import chr_dll2_connection as chr_connection
import re


class tab3:

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.var = DoubleVar()
        self.barbeginn = 0
        self.barend = 500
        self.buttonframe = LabelFrame(self.frame)
        self.portframe = LabelFrame(self.frame,width=400,height=200)
        self.measureframe = LabelFrame(self.frame,width=400,height=200)
        self.myLabel = Label(self.frame, text=' ')
        self.e = Entry(self.buttonframe, width=20, font=('Helvetica', 25))



        self.scrollbar = Scrollbar(self.portframe)
        self.scrollbar.pack( side = RIGHT, fill = Y )

        self.mylist = Listbox(self.portframe, yscrollcommand = self.scrollbar.set,width=67)
        for line in range(6):
            self.mylist.insert(END, "COM" + str(line))
        self.mylist.pack(fill=X)
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
        self.measure = Button(self.measureframe,text='measurebeginn',command=lambda:threading.Thread(target=self.measureprocess).start())
        self.emstop = Button(self.measureframe,text='pause',command = self.stoppro,width=26)

        self.measure.grid(row = 2,column=1)
        self.emstop.grid(row = 3,column=1)
        self.measureframe.grid(row = 3,column=1)


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

        #self.buttonframe.grid(row=0,column=0)
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


        #this code is for the detector
        self.chr = chr_connection.CHR_connection('IP: 169.254.2.217',1)
        self.res = self.chr.send_command('$MMD 0')
        self.n_sample = 100

        """
        Label
        """
        self.labe = LabelFrame(self.frame)
        self.display_text = StringVar()
        self.display = Label(self.labe, textvariable=self.display_text,width=60, height=10)
        self.display.grid(row=0, columnspan=3)
        self.labe.grid(row=4,column=0)

        
    def add_txt(self,cmd):
        s = self.display_text.get()
        fid = [go.start() for go in re.finditer('\n',s)]
        if(len(fid)==5):
            s = ' '
        s += cmd+'\n'
        self.display_text.set(s)


    def gettheintensiti(self):
            self.intensity = self.chr.send_command('$SODX 257')
            self.chr.set_autobuffer_size(self.n_sample)
            self.chr.flush_autobuffer()    
            self.chr.start_autobuffer()
            self.buffer = self.chr.read_autobuffer()
            self.intenmean = np.mean(self.buffer)
            return self.intenmean
    def getthedistance(self):
            self.distan = self.chr.send_command('$SODX 256')
            self.chr.set_autobuffer_size(self.n_sample)
            self.chr.flush_autobuffer()    
            self.chr.start_autobuffer()
            self.buffer2 = self.chr.read_autobuffer()
            self.dismean = np.mean(self.buffer2)
            return self.dismean   

    def measureprocess(self):
        try:
            #self.ser.reset_input_buffer()
            self.ser.write(str.encode("G91\r\n"))
            if self.xcor.get() == '':
                self.xcor.get() == 0
            if self.ycor.get() == '':
                self.ycor.get() == 0
            self.ser.write(str.encode("G01"+'X'+self.xcor.get()+'Y'+self.ycor.get()+'\r\n'))
            self.ser.write(str.encode("M0 P2500\r\n"))

            for i in range(25):
                print(self.ser.readline().decode("utf-8"))
                #self.ser.write(str.encode("M0 P3500\r\n"))
                print('moving to the position')
                self.ser.write(str.encode("G01"+'X'+'1'+'\r\n'))
                cod = 0
                while (cod<25000) :
                    #self.ser.write(str.encode("G01"+'Z'+'-0.1''\r\n'))
                    self.ser.write(str.encode("M0 P1000\r\n"))
                    cod = self.gettheintensiti()
                    #print('dis now is ' + str(cod) + ' um')
                    print(cod)
                    time.sleep(0.1)
                
                print('distance is'+ ' : '+ str(self.getthedistance())+ ' ' + 'um')
                #self.ser.write(str.encode("G01"+'Z'+'5'+'\r\n'))
                time.sleep(3.5)

        except serial.serialutil.PortNotOpenError:
            print('port closed')            
            self.add_txt('port closed')   
        except AttributeError:
            print('no machine connected')
            self.add_txt('no machine connected')
    

    def stoppro(self):
        if(self.ser != None):
            print("disconnect")
            self.add_txt('disconnect')
            self.ser.close()
            self.ser = None
        else:
            print('no port connected now')
            self.add_txt('no port connected now')
    
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
            self.add_txt(self.mylist.selection_get()+' '+"connected")
        except serial.serialutil.SerialException:
            print('port'+ ' '+ self.mylist.selection_get() +' '+'can not connect' )
            self.add_txt('port'+ ' '+ self.mylist.selection_get() +' '+'can not connect' )
        except tkinter.TclError:
            print('one port muss be selected first')
            self.add_txt('one port muss be selected first')


    def Homexyz(self):
        try:
            self.ser.write(str.encode("G28\r\n"))
        except AttributeError:
            print('no machine connected')
            self.add_txt('no machine connected')
    def disconnect3d(self):
        
        try:
            if(self.ser != None):
                print("disconnect")
                self.add_txt('disconnect')
                self.ser.close()
                self.ser = None
            else:
                print('no port connected now')
                self.add_txt('no port connected now')
        except AttributeError:
            print('no machine connected')
            self.add_txt('no machine connected')   
    def moving(self,direction,scale):
        
        try:
            print(str(direction)+''+str(scale))
            self.ser.write(str.encode("G91\r\n"))
            self.ser.write(str.encode("G01"+direction+scale+"\r\n"))
            self.add_txt(str(direction)+''+str(scale))
        except AttributeError:
            print("moving machine not conneted yet")
            self.add_txt("moving machine not conneted yet")
        except serial.serialutil.SerialException:
            print("no connection")
            self.add_txt("no connection")

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
        dir = 'Y'
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
