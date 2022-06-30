from audioop import findmax
from calendar import c
import threading
from tkinter import *
import tkinter.filedialog
import round_controller
import reccontrol
import serial
import numpy as np
import chr_dll2_connection as chr_connection
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk)
import csv
from mpl_toolkits.mplot3d import Axes3D



class tab3:

    def __init__(self, root, frame):

        #the gui include has different sub frames.
        self.root = root
        self.frame = frame
        self.var = DoubleVar()
        self.barbeginn = 0
        self.barend = 500
        #self.buttonframe = LabelFrame(self.frame)
        self.portframe = LabelFrame(self.frame,width=400,height=200)
        self.measureframe = LabelFrame(self.frame,width=400,height=200)
        #self.myLabel = Label(self.frame, text=' ')
        #self.e = Entry(self.buttonframe, width=20, font=('Helvetica', 25))         
        self.resultlx = []
        self.zcoordinats = []
        self.xcoordinats = []

        # this is for the port
        #those codes create the port which can be choosen
        self.mylist = Listbox(self.portframe,width=67)
        for line in range(6):
            str1 = "COM" + str(line)
            theleng = len(str1)+60
            modify = str1.rjust(theleng)
            self.mylist.insert(END,modify)
        self.mylist.pack(fill=X)
        
        self.portchoice = Button(self.portframe, text="connect", width=50,command=self.connect3d)
        self.portchoice.pack()
        self.home = Button(self.portframe, text="home", width=50,command=self.Homexyz)
        self.home.pack()
        self.disconnecrt = Button(self.portframe, text="disconnnect", width=50,command=self.disconnect3d)
        self.disconnecrt.pack()
        self.portframe.grid(row=3,column=0)


        #half auto measure part it includes the key measure parameters 
        self.meatype = StringVar()
        self.meatype.set('type1')
        self.meafun = self.measureprocess1
        self.xbegn = Entry(self.measureframe)
        self.xbegn.grid(row = 0,column=1)
        self.L0 = Label(self.measureframe, text="choose measure type")
        self.L1 = Label(self.measureframe, text="xbeginn")
        self.L1.grid(row = 0,column=0)
        self.ybegn = Entry(self.measureframe)
        self.ybegn.grid(row = 1,column=1)
        self.L2 = Label(self.measureframe, text="ybeginn")
        self.L2.grid(row = 1,column=0)
        self.meachoice1 = Radiobutton(self.measureframe,text = 'type1(high to low)',value='type1',variable=self.meatype,command=self.funchoice)
        self.meachoice2 = Radiobutton(self.measureframe,text = 'type2(low to high)',value='type2',variable=self.meatype,command=self.funchoice)


        self.measure = Button(self.measureframe,text='measurebeginn',command=lambda:threading.Thread(target=self.measureprocess1).start(),width = 25)
        self.emstop = Button(self.measureframe,text='pause result export',command = self.exportdata,width=25)
        self.emstart = Button(self.measureframe,text='start result import',command = self.imoprtdata,width=25)




        self.L0.grid(row = 0,column=2)
        self.meachoice1.grid(row = 1,column=2)
        self.meachoice2.grid(row = 2,column=2)
        self.measure.grid(row = 7,column=1)
        self.emstop.grid(row = 8,column=1)
        self.emstart.grid(row = 9,column=1)
        self.measureframe.grid(row = 3,column=1)



        self.xlen = Entry(self.measureframe)
        self.ylen = Entry(self.measureframe)
        self.xlen.grid(row = 2,column=1)
        self.ylen.grid(row = 3,column=1)
        self.L3 = Label(self.measureframe, text="xlen")
        self.L3.grid(row = 2,column=0)
        self.L4 = Label(self.measureframe, text="ylen")
        self.L4.grid(row = 3,column=0)

        self.L5 = Label(self.measureframe, text="xsamplepkt")
        self.L5.grid(row = 4,column=0)
        self.L6 = Label(self.measureframe, text="ysamplepkt")
        self.L6.grid(row = 5,column=0)

        self.xsample = Entry(self.measureframe)
        self.ysample = Entry(self.measureframe)
        self.xsample.grid(row = 4,column=1)
        self.ysample.grid(row = 5,column=1)


        self.L7 = Label(self.measureframe, text="z dis approx")
        self.L7.grid(row = 6,column=0)
        self.zdis = Entry(self.measureframe)
        self.zdis.grid(row=6,column=1)


        # add some buttons
        # self.Buttonx = Button(self.buttonframe, text="A axis", padx=50,
        #                       command=lambda cmd="A axis selected": self.clickit(cmd))
        # self.Buttony = Button(self.buttonframe, text="B axis", padx=50,
        #                       command=lambda cmd="B axis selected": self.clickit(cmd))
        # self.Buttonz = Button(self.buttonframe, text="C axis", padx=50,
        #                       command=lambda cmd="C axis selected": self.clickit(cmd))
        # self.Buttonminus = Button(self.buttonframe, text="-", padx=50,
        #                           command=lambda cmd="movement minus selected": self.clickit(cmd))
        # self.Buttonplus = Button(self.buttonframe, text="+", padx=50,
        #                          command=lambda cmd="movement plus selected": self.clickit(cmd))





        # put the button in the plattform


        # self.Buttonx.grid(row=0, column=0)
        # self.Buttony.grid(row=0, column=1)
        # self.Buttonz.grid(row=0, column=2)
        # self.Buttonplus.grid(row=1, column=0)
        # self.Buttonminus.grid(row=1, column=2)


        #self.myLabel.grid(row=6, column=0)
        #self.e.grid(row=3, column=1)

        #ser is the serial port instance
        self.ser = None
        self.roundconframe = LabelFrame(self.frame)
        self.roundconframe.grid(row=1, column=0)
        self.rectanframe = LabelFrame(self.frame)
        self.rectanframe.grid(row=1, column=1)
        
        self.control = round_controller.round_controller(self.roundconframe, self.roundconframe)
 
        #round button control bind with the moving function
        
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



        self.control2 = reccontrol.reccontrol(self.rectanframe,self.rectanframe)
        self.control2.canvas.tag_bind(self.control2.trilist[0], '<Button-1>', self.zmovingminus2)
        self.control2.canvas.tag_bind(self.control2.trilist[1], '<Button-1>', self.zmovingminus1)
        self.control2.canvas.tag_bind(self.control2.trilist[2], '<Button-1>', self.zmovingminus0)
        self.control2.canvas.tag_bind(self.control2.trilist[3], '<Button-1>', self.zmovingplus0)
        self.control2.canvas.tag_bind(self.control2.trilist[4], '<Button-1>', self.zmovingplus1)
        self.control2.canvas.tag_bind(self.control2.trilist[5], '<Button-1>', self.zmovingplus2)


        # detector will connect the default ipv4 port with below codes
        #MMD 0 will set the measurement mode to  chromatic confocal
        #n_sample : desired length of autobuffer
        self.chr = chr_connection.CHR_connection('IP: 169.254.2.217',1)
        self.res = self.chr.send_command('$MMD 0')
        self.n_sample = 100
    
        #it will show the real time information while measuring
        # g code can also be sent here

        self.labe = Frame(self.frame)
        self.scrollbar = Scrollbar(self.labe)
        self.scrollbar.pack( side = RIGHT, fill = Y )

        self.mytext = Text(self.labe, yscrollcommand = self.scrollbar.set,width = 45,height=5)
        self.clss = Button(self.labe,command=self.cls,text='clear')
        self.clss.pack(side = LEFT)

        self.sender = Button(self.labe,command=self.sendcmd,text='sendcmd')
        self.sender.pack(side = BOTTOM)

        self.reader = Button(self.labe,command=self.abspos,text=' abspos  ')
        self.reader.pack(side = BOTTOM)

        self.mytext.pack( side = TOP, fill = BOTH )
        self.scrollbar.config( command = self.mytext.yview )
        self.labe.grid(row=4,column=0)


        #two output windows for the results
        self.graph = Frame(self.frame)

        self.zgraph = Button(self.graph,command=self.zplot,text='zdiagramm')
        self.zgraph.pack(side = TOP)

        self.dzgraph = Button(self.graph,command=self.dzplot,text='dzdiagram')
        self.dzgraph.pack(side = TOP)


        self.dcls = Button(self.graph,command=self.clean,text='     clean      ')
        self.dcls.pack(side = TOP)
        self.graph.grid(row=4,column=1)


    #this function will clean the information of the output 
    def clean(self):
        self.resultlx = []
        self.xcoordinats = []
        self.zcoordinats = []
        self.ycoordinate = []
    #this function can switch the measurement methods
    def funchoice(self):
        if(self.meatype.get() == 'type1'):self.meafun = self.measureprocess1
        if(self.meatype.get() == 'type2'):self.meafun = self.measureprocess2
        self.add_txt(self.meatype.get())
    
    #relative distance will be defined in this function and output in the chart
    def dzplot(self): 

        window = Toplevel()
        window.title('dz value')
        fig = Figure(figsize = (8,5), 
                    ) 
        x = [float(i) for i in self.xcoordinats]
        
        resultflot = [float(i) for i in self.resultlx]
        zfloat = [1000*float(i) for i in self.zcoordinats]
        # z = [i for i in zfloat]+[i for i in resultflot]

        # z = [i-z[0] for i in zfloat]

        z = resultflot 
        
        plot1 = fig.add_subplot(111) 

        
        plot1.plot(x,z,'.') 
    
        plot1.set_xlabel('x position')
        plot1.set_ylabel('read result (um)')

        canvas = FigureCanvasTkAgg(fig, 
                                master = window)   
        canvas.draw() 
    
        
        canvas.get_tk_widget().pack() 
    
        
        toolbar = NavigationToolbar2Tk(canvas, 
                                    window) 
        toolbar.update()         
        canvas.get_tk_widget().pack() 
    #absolt distance will be defined in this function and output in the chart
    def zplot(self): 
  
        window = Toplevel()
        window.title('z value')
        fig = Figure(figsize = (8,5 )
                    ) 
        x = [float(i) for i in self.xcoordinats]
        
        z = [float(i) for i in self.zcoordinats] 
        
        y = [float(i) for i in self.ycoordinats] 
        
        plot1 = fig.add_subplot(111) 
        plot1.set_xlabel('x position')
        plot1.set_ylabel('z position(mm)')
        
        plot1.plot(x,z,'.') 
    
        canvas = FigureCanvasTkAgg(fig, 
                                master = window)   
        canvas.draw() 
    
        
        canvas.get_tk_widget().pack() 
    
        toolbar = NavigationToolbar2Tk(canvas, 
                                    window) 
        toolbar.update()         
        canvas.get_tk_widget().pack() 
    #clean all the information on the label
    def cls(self):
        self.mytext.delete("1.0","end")
    #it returns the coordinate value of the point
    def abspos(self):
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(str.encode('M114'+"\r\n"))
            cor = self.ser.readline().decode("UTF-8")
            zpos = cor[cor.find('Z')+2:cor.find('E')]
            xpos = cor[cor.find('X')+2:cor.find('Y')]
            ypos = cor[cor.find('Y')+2:cor.find('Z')]
            self.add_txt(zpos)
            print(cor)
            return cor[:24],zpos,xpos,ypos
        except AttributeError:
            self.add_txt('noting connected yet')

    #this code sent the last line of feedback        
    def sendcmd(self):
        try:
            a = self.mytext.get("1.0", "end")
            idx = len(a.split('\n'))
            want = a.split('\n')[idx-3]
            self.ser.write(str.encode(want+"\r\n"))
            print(want)
        except AttributeError:
            self.add_txt('noting connected yet')
    
    #add the information on the label
    def add_txt(self,cmd):
        if isinstance(cmd,str):
            self.mytext.insert(END,cmd+'\n')
        if isinstance(str(cmd),list):
            self.mytext.insert(END,'result is below' + '\n')
            for i in range(len(cmd)):
                self.mytext.insert(END,cmd[i]+'\n')
        
        self.mytext.yview(END)
    

    #request of the current light intensity
    def gettheintensiti(self):
            self.intensity = self.chr.send_command('$SODX 257')
            self.chr.set_autobuffer_size(self.n_sample)
            self.chr.flush_autobuffer()    
            self.chr.start_autobuffer()
            self.buffer = self.chr.read_autobuffer()
            self.intenmean = np.mean(self.buffer)
            return self.intenmean
    #request of the current distance
    def getthedistance(self):
            self.distan = self.chr.send_command('$SODX 256')
            self.chr.set_autobuffer_size(self.n_sample)
            self.chr.flush_autobuffer()    
            self.chr.start_autobuffer()
            self.buffer2 = self.chr.read_autobuffer()
            self.dismean = np.mean(self.buffer2)
            return self.dismean   
    #checking of the nan value
    def nan_equal(self,a,b):
        try: 
            np.testing.assert_equal(a,b)
        except AssertionError:
            return False
        return True

    # find the max value in a list
    def findmax(self,inputlist):
        inputlist = [float(i) for i in inputlist]
        maxvalue = max(inputlist)
        maxindex = inputlist.index(maxvalue)
        print(maxvalue,maxindex)
        return maxvalue,maxindex

    #the type 1 measurement process.
    def measureprocess1(self):    
        try:
            #clean the buffer before measurement
            self.ser.flushInput()
            self.ser.flushOutput()
            #request of current position            
            _,zpos,xpos,ypos = self.abspos()
            print('zpos is ' + zpos)

            #default value of the measurement parameters
            if self.xbegn.get() == '':
                self.xbegn.insert(0,'0')
            if self.ybegn.get() == '':
                self.ybegn.insert(0,'0')

            if self.xlen.get() == '':
                self.xlen.insert(0,'10')
            if self.ylen.get() == '':
                self.ylen.insert(0,'10') 

            if self.xsample.get() == '':
                self.xsample.insert(0,'2')
            if self.ysample.get() == '':
                self.ysample.insert(0,'1')
            if self.zdis.get() == '':
                self.zdis.insert(0,'15')
            #the integer will be used here   
            lenx = int(self.xlen.get())
            leny = int(self.ylen.get())
            numofy = int(self.ysample.get())
            numofx = int(self.xsample.get())
            #When the number of sampling points is odd, the sampling interval will be evenly divided into even parts
            a = numofx
            if(numofx%2!=0):a = numofx-1
            if (a == 0): a = 1
            
            b = numofy
            if(numofy%2!=0):b = numofy-1
            if (b == 0): b = 1
            #step length of sampling 
            deltax = lenx/a
            deltay = leny/b
            
            #initial defined safety heigth
            dsafe = 6
            steplimit = (int(self.zdis.get())-dsafe)/0.1
            #the integer or float muss be convert to string before send to the machine
            print(deltax,deltay)
            deltax = str(deltax)
            deltay = str(deltay)

            #xbegn and ybegn will set the movement wrt current position
            self.ser.write(str.encode("G91\r\n"))
            self.ser.write(str.encode("G01"+'X'+self.xbegn.get()+'Y'+self.ybegn.get()+'\r\n'))
            print('step lim is     '+str(steplimit))
            for row in range(numofy):
                for column in range(numofx):
                    self.ser.write(str.encode("G91\r\n"))
                    if (row%2)==0:
                        self.add_txt('working on the even row')
                        if (column != 0):
                            self.ser.write(str.encode("G01"+'X'+deltax+'\r\n'))
                    if (row%2)!=0:
                        self.add_txt('working on the odd row')
                        if (column != 0):
                            self.ser.write(str.encode("G01"+'X'+'-'+deltax+'\r\n'))
                    #cod is the current measured distance ,if the distance out of measurement rang,nan could be occured
                    #step record the moving step in z direction
                    cod = 0
                    step = 0
                    while ( step < steplimit) :
                        self.ser.write(str.encode("G01"+'Z'+'-0.1''\r\n'))
                        cod = self.getthedistance()
                        self.add_txt(str(cod))
                        #once the cod reach the the range 60-260.it will be recorded as result
                        if (not self.nan_equal(cod,np.NaN) and np.abs(int(cod) - 160) < 100):
                            self.add_txt('distance is'+ ' : '+ str(cod)+ ' ' + 'um')
                            co,currentz,currentx,currenty = self.abspos()
                            self.resultlx.append(str(cod))
                            self.xcoordinats.append(currentx)
                            self.zcoordinats.append(currentz)
                            self.ycoordinats.append(currenty)
                            dissmaller = 1

                            zpos = str(float(currentz)+dissmaller)
                             
                            self.add_txt('zpos now is   '+ zpos)
                            steplimit = 2*dissmaller/0.1
                            self.add_txt('steplim now is ' + str(steplimit))
                            step = steplimit

                        step=step+1


                    self.ser.write(str.encode("G90\r\n"))
                    self.add_txt('gogog')    
                    self.ser.write(str.encode("G01"+'Z'+zpos+'\r\n'))



                if (row<numofy-1):
                    #once the measurement in one row done ,it will move to the next row
                    self.ser.write(str.encode("G91\r\n"))
                    self.add_txt('next y ........')
                    self.ser.write(str.encode("G01"+'Y'+'-'+deltay+'\r\n'))
            print(self.xcoordinats)
            print(self.resultlx)
            print(self.zcoordinats)
            print(self.ycoordinats)
            
        except serial.serialutil.PortNotOpenError:
            self.add_txt('port closed')   
        except AttributeError:
            self.add_txt('no machine connected')

    def measureprocess2(self):    
        try:
            self.ser.flushInput()
            self.ser.flushOutput()            
            _,zpos,xpos,ypos = self.abspos()
            print('zpos is ' + zpos)
        
            if self.xbegn.get() == '':
                self.xbegn.insert(0,'0')
            if self.ybegn.get() == '':
                self.ybegn.insert(0,'0')

            if self.xlen.get() == '':
                self.xlen.insert(0,'10')
            if self.ylen.get() == '':
                self.ylen.insert(0,'10') 

            if self.xsample.get() == '':
                self.xsample.insert(0,'2')
            if self.ysample.get() == '':
                self.ysample.insert(0,'1')


            if self.zdis.get() == '':
                self.zdis.insert(0,'15')
            lenx = int(self.xlen.get())
            leny = int(self.ylen.get())
            
            numofy = int(self.ysample.get())
            numofx = int(self.xsample.get())
            a = numofx
            if(numofx%2!=0):a = numofx-1
            if (a == 0): a = 1
            
            b = numofy
            if(numofy%2!=0):b = numofy-1
            if (b == 0): b = 1

            deltax = lenx/a
            deltay = leny/b
            
            dsafe = 6
            steplimit = (int(self.zdis.get())-dsafe)/0.1

            print(deltax,deltay)
            deltax = str(deltax)
            deltay = str(deltay)
            self.ser.write(str.encode("G91\r\n"))
            self.ser.write(str.encode("G01"+'X'+self.xbegn.get()+'Y'+self.ybegn.get()+'\r\n'))
            print('step lim is   '+str(steplimit))

            #the mov is used to set the movement in z direction.
    

            mov = '0.1'
            for row in range(numofy):
                for column in range(numofx):
                    self.ser.write(str.encode("G91\r\n"))
                    if (row%2)==0:
                        self.add_txt('working on the even row')
                        if (column != 0):
                            self.ser.write(str.encode("G01"+'X'+deltax+'\r\n'))
                    if (row%2)!=0:
                        self.add_txt('working on the odd row')
                        if (column != 0):
                            self.ser.write(str.encode("G01"+'X'+'-'+deltax+'\r\n'))

                    cod = 0
                    step = 0
                    
                    while ( step < steplimit) :
                        
                        self.ser.write(str.encode("G01"+'Z'+mov+'\r\n'))
        	            

                        cod = self.getthedistance()
                        self.add_txt(str(cod))

                        #once the movement setp in one direciton +z or -z reach 15
                        #the movement will be inversed.
                        if (step == 15):
                            if(mov == '0.1'):
                                mov = '-0.1'
                            else:
                                mov = '0.1'
                            print('inversed mov is' + mov)
                            # self.ser.write(str.encode("G90\r\n"))
                            # self.add_txt('back2Z ')    
                            # self.ser.write(str.encode("G01"+'Z'+zpos+'\r\n'))
                            # self.ser.write(str.encode("G91\r\n"))

                        if (not self.nan_equal(cod,np.NaN) and np.abs(int(cod) - 160) < 100):
                            self.add_txt('distance is'+ ' : '+ str(cod)+ ' ' + 'um')
                            co,currentz,currentx,currenty = self.abspos()
                            self.resultlx.append(str(cod))
                            self.xcoordinats.append(currentx)
                            self.zcoordinats.append(currentz)
                            self.ycoordinats.append(currenty)
                            disbigger = 4

                            zpos = str(float(currentz))
                                
                            self.add_txt('zpos now is   '+ zpos)
                            steplimit = 2*disbigger/0.1
                            self.add_txt('steplim now is ' + str(steplimit))
                            step = steplimit

                        step=step+1


                    # self.ser.write(str.encode("G90\r\n"))
                    # self.add_txt('back2Z ')    
                    # self.ser.write(str.encode("G01"+'Z'+zpos+'\r\n'))


                if (row<numofy-1):
                    self.ser.write(str.encode("G91\r\n"))
                    self.add_txt('next y .....')
                    self.ser.write(str.encode("G01"+'Y'+'-'+deltay+'\r\n'))


            print(self.xcoordinats)
            print(self.resultlx)
            print(self.zcoordinats)
        
        except serial.serialutil.PortNotOpenError:
            self.add_txt('port closed')   
        except AttributeError:
                self.add_txt('no machine connected')

    

    #pause the machine if necessary
    def stoppro(self):
        if(self.ser != None):

            self.add_txt('stop')
            self.ser.write(str.encode("M0\r\n"))
        else:

            self.add_txt('no port connected now')


    # start the machine after pause
    def start(self):
        if(self.ser != None):

            self.add_txt('start')
            self.ser.write(str.encode("M108\r\n"))
        else:

            self.add_txt('no port connected now')
    #connect the 3d drucker
    def connect3d(self):
        try:
            self.ser = serial.Serial(self.mylist.selection_get().strip(), 115200,)

            self.add_txt(self.mytext.selection_get()+' '+"connected")
        except serial.serialutil.SerialException:

            self.add_txt('port'+ ' '+ self.mylist.selection_get().strip() +' '+'can not connect' )
        except tkinter.TclError:

            self.add_txt('one port muss be selected first')
    #go to origianl position.in order to let the machine move ,it is necessary to do it first.
    def Homexyz(self):
        try:
            self.ser.write(str.encode("G28\r\n"))
            self.add_txt('homing')
        except AttributeError:
            self.add_txt('no machine connected')

    #disconnect the machine but it oft used to pause the process if necessary
    def disconnect3d(self):
        
        try:
            if(self.ser != None):
                print("disconnect")
                self.add_txt('disconnect')
                self.ser.close()
                self.ser = None
            else:

                self.add_txt('no port connected now')
        except AttributeError:
            self.add_txt('no machine connected')

    #this basic moving function is used to defined the sub moving function on the gui
    # because the command in button can not input the arguement   
    def moving(self,direction,scale):
        
        try:
            self.ser.write(str.encode("G91\r\n"))
            self.ser.write(str.encode("G01"+direction+scale+"\r\n"))
            self.add_txt(str(direction)+''+str(scale))
        except AttributeError:
            self.add_txt("moving machine not conneted yet")
        except serial.serialutil.SerialException:
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


    #export the measurement result
    def exportdata(self):
        category = ['Pointindex', 'X', 'Z', 'Readvalue'] 
        ptidx =  []
        rows =  []
        for i in range(len(self.xcoordinats)):
            ptidx.append(i)
        for i in range(len(self.xcoordinats)):
            rows.append([ptidx[i],self.xcoordinats[i], self.zcoordinats[i],self.resultlx[i]]) 
        with open('result.csv', 'w') as f: 
            write = csv.writer(f) 
            write.writerow(category) 
            write.writerows(rows) 
        f.close()

    #importing the result from external file
    def imoprtdata(self):
        file = open('result.csv')
        csvreader = csv.reader(file)
        header = []
        header = next(csvreader)
        rows = []
        for row in csvreader:
            if (len(row)!=0):
                rows.append(row)
        for i in range(len(rows)):
            self.xcoordinats.append(rows[i][1])
            self.zcoordinats.append(rows[i][2])
            self.resultlx.append(rows[i][3])

        self.findmax(self.zcoordinats)
        self.add_txt('data imported! ')
#main process if only this script works
if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)

    tab3(root, root)

    root.mainloop()
