from tkinter import *
import re
from tkinter import ttk,messagebox
import sqlite3
import numpy as np
import matplotlib 
from collections import defaultdict
from heapq import *
from matplotlib import pyplot as plt 
from matplotlib.figure import Figure 
import os  
from matplotlib.patches import Polygon
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

class Student:
      def __init__(self,root):
            self.canvases= []
            self.toolbars= []
            self.root=root
            self.flag = "Patient"
            self.root.title("Pandemic Support")
            self.root.geometry("1350x800+0+0")
            self.adj = self.connectgraph(100)
            title=Label(self.root,text="Pandemic Support",font=("times new roman",25,"bold"),
            bg="cyan",fg="black",bd=10,relief=GROOVE)
            title.pack(side=TOP,fill=X)
#=================All Variables1===================

            self.pat_x=DoubleVar(value = 0)
            self.pat_y=DoubleVar(value=0)
            self.hosp_x=DoubleVar(value=0)
            self.hosp_y=DoubleVar(value=0)
            self.cur_x = DoubleVar(value=0)
            self.cur_y = DoubleVar(value=0)
            self.probab = DoubleVar(value=0)

#================MANAGE_FRAME===================
            Manage_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="cyan")
            Manage_Frame.place(x=20,y=70,width=480,height=420)

            m_title=Label(Manage_Frame,text="Add coordinates",bg="black",fg="white",font=("times new roman",20,"bold"))
            m_title.grid(row=0,columnspan=2,pady=20)

            lbl_name=Label(Manage_Frame,text="Current X coodinate",bg="black",fg="white",font=("times new roman",15,"bold"))
            lbl_name.grid(row=1,column=0,pady=10,padx=10,sticky="w")
            txt_name=Entry(Manage_Frame,textvariable=self.pat_x,font=("times new roman",15,"bold"),relief=GROOVE,bd=5)
            txt_name.grid(row=1,column=1,pady=10,padx=10,sticky="w")

            lbl_amt=Label(Manage_Frame,text="Current Y coodinate",bg="black",fg="white",font=("times new roman",15,"bold"))
            lbl_amt.grid(row=2,column=0,pady=10,padx=10,sticky="w")
            txt_amt=Entry(Manage_Frame,textvariable=self.pat_y,font=("times new roman",15,"bold"),relief=GROOVE,bd=5)
            txt_amt.grid(row=2,column=1,pady=10,padx=10,sticky="w")

            Updbtn=Button(Manage_Frame,command=self.add_patient,text="Add Patient",width=20)      
            Updbtn.grid(row=3,column=1,padx=10,pady=10)

            lbl_intrate=Label(Manage_Frame,text="Hospital X coordinate",bg="black",fg="white",font=("times new roman",15,"bold"))
            lbl_intrate.grid(row=4,column=0,pady=10,padx=10,sticky="w")
            txt_intrate=Entry(Manage_Frame,textvariable=self.hosp_x,font=("times new roman",15,"bold"),relief=GROOVE,bd=5)
            txt_intrate.grid(row=4,column=1,pady=10,padx=10,sticky="w")

            lbl_mon=Label(Manage_Frame,text="Hospital Y coordinate",bg="black",fg="white",font=("times new roman",15,"bold"))
            lbl_mon.grid(row=5,column=0,pady=10,padx=10,sticky="w")
            txt_mon=Entry(Manage_Frame,textvariable=self.hosp_y,font=("times new roman",15,"bold"),relief=GROOVE,bd=5)
            txt_mon.grid(row=5,column=1,pady=10,padx=10,sticky="w")
            
            Addbtn=Button(Manage_Frame,text="Add Hospital",width=20,command=self.add_hospital)    
            Addbtn.grid(row=6,column=1,padx=10,pady=10)


#================BUTTON FRAME=====================
            Button_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="cyan")
            Button_Frame.place(x=20,y=500,width=230,height=480)

            m_title=Label(Button_Frame,text="Features:-",bg="black",fg="white",font=("times new roman",18,"bold"))
            m_title.grid(row=0,columnspan=2,pady=10)
            
            Updbtn=Button(Button_Frame,command=self.plot,text="City Map",width=20)      
            Updbtn.grid(row=1,column=0,padx=10,pady=10)

            Updbtn=Button(Button_Frame,command=self.Zone_Marking,text="Zone Marking",width=20)      
            Updbtn.grid(row=2,column=0,padx=10,pady=10)

            Updbtn=Button(Button_Frame,command=self.add_object,text="Add Object",width=20)      
            Updbtn.grid(row=3,column=0,padx=10,pady=10)

            Updbtn=Button(Button_Frame,command=self.mst,text="Lockdown",width=20)      
            Updbtn.grid(row=4,column=0,padx=10,pady=10)

            Updbtn=Button(Button_Frame,command=self.busstop,text="Bus Stop",width=20)      
            Updbtn.grid(row=5,column=0,padx=10,pady=10)

            Updbtn=Button(Button_Frame,command=self.feature5,text="Path for Vaccination",width=20)      
            Updbtn.grid(row=6,column=0,padx=10,pady=10)

            Updbtn=Button(Button_Frame,command=self.newmap2,text="Quarantine Zones",width=20)      
            Updbtn.grid(row=7,column=0,padx=10,pady=10)


#================Navigate Frame==========================

            Navigate_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="cyan")
            Navigate_Frame.place(x=270,y=500,width=230,height=480)

            lbl_name=Label(Navigate_Frame,text="Patient X coodinate",bg="black",fg="white",font=("times new roman",15,"bold"))
            lbl_name.grid(row=1,column=0,pady=10,padx=10,sticky="w")
            txt_name=Entry(Navigate_Frame,width = 15,textvariable=self.cur_x,font=("times new roman",15,"bold"),relief=GROOVE,bd=5)
            txt_name.grid(row=2,column=0,pady=10,padx=10,sticky="w")

            lbl_amt=Label(Navigate_Frame,text="Patient Y coodinate",bg="black",fg="white",font=("times new roman",15,"bold"))
            lbl_amt.grid(row=3,column=0,pady=10,padx=10,sticky="w")
            txt_amt=Entry(Navigate_Frame,width = 15,textvariable=self.cur_y,font=("times new roman",15,"bold"),relief=GROOVE,bd=5)
            txt_amt.grid(row=4,column=0,pady=10,padx=10,sticky="w")

            self.t_btn = Button(Navigate_Frame,text="Patient", width=12, command=self.toggle)
            self.t_btn.grid(row=5,column=0,padx=10,pady=10)

            Updbtn1=Button(Navigate_Frame,command=self.handler,text="Path to Nearest Hospital",width=20)      
            Updbtn1.grid(row=6,column=0,padx=10,pady=10)

            Updbtn1=Button(Navigate_Frame,command=self.probability,text="Infection Probability",width=20)      
            Updbtn1.grid(row=7,column=0,padx=10,pady=10)

            txt_amt=Entry(Navigate_Frame,width = 15,textvariable=self.probab,font=("times new roman",15,"bold"),relief=GROOVE,bd=5)
            txt_amt.grid(row=8,column=0,pady=10,padx=10,sticky="w")

            
            self.feature2()
            # self.busstop(100)
            # self.mst(100)
            # self.feature5(100)
            # self.newmap2(100)
            self.plot()
            
      def add_hospital(self):
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            hosx=self.hosp_x.get()
            hosy=self.hosp_y.get()
            try:
                  cur.execute('''CREATE TABLE IF NOT EXISTS HOSPITALS
                  (
                        X real,
                        Y real,
                        PRIMARY KEY (X,Y)
                  );
                  ''')
                  cur.execute('''INSERT INTO HOSPITALS 
                        (X,Y) 
                        VALUES(?,?)''',
                        (hosx,hosy))
                  con.commit()
            except:
                  print("Error")
            self.clear_data()
            con.close()
            self.plot()

      def toggle(self):
            if self.t_btn.config('text')[-1] == 'Patient':
                  self.t_btn.config(text='Not a Patient')
                  self.flag = "NPatient"
            else:
                  self.t_btn.config(text='Patient')
                  self.flag = "Patient"

      def add_object(self):
            print('''
            1. for rectangle
            2. for circle
            3. for triangle
            4. end
            ''')
            n =int(input("Enter your choice"))
            if(n==1):
                  self.add_square()
            elif(n==2):
                  self.add_circle()
            elif (n==3):
                  self.add_triangle()
            else:
                  return
      def add_square(self):
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            bottomleftx = int(input("Enter bottom left X: "))
            bottomlefty = int(input("Enter bottom left Y: "))
            width = int(input("Enter width: "))
            height  = int(input("Enter height: "))
            try:
                  cur.execute('''CREATE TABLE IF NOT EXISTS SQUARE
                  (
                        X real,
                        Y real,
                        width real,
                        height real,
                        PRIMARY KEY (X,Y,width,height)
                  );
                  ''')
                  cur.execute('''INSERT INTO SQUARE 
                        (X,Y,width,height) 
                        VALUES(?,?,?,?)''',
                        (bottomleftx ,bottomlefty ,width,height))
                  con.commit()
            except:
                  print("Error")
            self.plot()
      
      def add_triangle(self):
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            x1 = int(input("Enter X1: "))
            y1 = int(input("Enter Y1: "))
            x2 = int(input("Enter X2: "))
            y2 = int(input("Enter Y2: "))
            x3 = int(input("Enter X3: "))
            y3 = int(input("Enter Y3: "))
            try:
                  cur.execute('''CREATE TABLE IF NOT EXISTS TRIANGLE
                  (
                        x1 real,
                        y1 real,
                        x2 real,
                        y2 real,
                        x3 real,
                        y3 real,
                        PRIMARY KEY (x1,y1,x2,y2,x3,y3)
                  );
                  ''')
                  cur.execute('''INSERT INTO TRIANGLE 
                        (x1,y1,x2,y2,x3,y3) 
                        VALUES(?,?,?,?,?,?)''',
                        (x1,y1,x2,y2,x3,y3))
                  con.commit()
            except:
                  print("Error")

      def add_circle(self):
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            x = int(input("Enter centreX: "))
            y = int(input("Enter centreY: "))
            r = int(input("Enter radius: "))
   
            try:
                  cur.execute('''CREATE TABLE IF NOT EXISTS CIRCLE
                  (
                        x real,
                        y real,
                        r real,
                        PRIMARY KEY (x,y,r)
                  );
                  ''')
                  cur.execute('''INSERT INTO CIRCLE 
                        (x,y,r) 
                        VALUES(?,?,?)''',
                        (x,y,r))
                  con.commit()
            except:
                  print("Error")
            self.plot()

      def newmap(self,offset):
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            row = []
            locality = []
            newmaplist = defaultdict(list)
            try:
                  cur.execute('''SELECT * FROM LOCALITY;''')
                  row = cur.fetchall()
            except:
                  print("error in newmap")
            for i in row:
                  x = int(i[0])
                  y = int(i[1])
                  u = self.converttoidx(x,y,offset)
                  locality.append(u)
            for i in range(len(locality)):
                  #--q is min heap---------
                  #---parent is array for backtracking-------
                  #--Dijkstras Algo---------
                  q, parent = [(0,locality[i])],{locality[i]: -1}
                  dist = np.full((offset*offset+4),20000)
                  dist[locality[i]]=0
                  while q:
                        (cost,v1) = heappop(q)
                        for c, v2 in self.adj.get(v1,()):
                              if (dist[v1]+c < dist[v2]):
                                    dist[v2] = dist[v1]+c 
                                    parent[v2] = v1
                                    heappush(q, (dist[v2], v2))
                  for j in range(len(locality)):
                        if locality[i] == locality[j]:
                              continue
                        newmaplist[locality[i]].append((dist[locality[j]],locality[j]))

            file1 = open("input.txt", "w+")
            sz = len(locality)
            n = (sz*(sz-1))
            file1.write(str(n)+"\n")
            for i  in newmaplist:
                  for j in range(len(newmaplist[i])):
                        file1.write(str(i)+" "+str(newmaplist[i][j][1])+" "+str(newmaplist[i][j][0])+"\n")
            file1.close() 
                  
      def add_patient(self):
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            patx=self.pat_x.get()
            paty=self.pat_y.get()
            try:
                  cur.execute('''CREATE TABLE IF NOT EXISTS PATIENT
                  (
                        X real,
                        Y real,
                        PRIMARY KEY (X,Y)
                  );
                  ''')
                  cur.execute('''INSERT INTO PATIENT 
                        (X,Y) 
                        VALUES(?,?)''',
                        (patx,paty))
                  con.commit()
            except:
                  print("Error")
            self.clear_data()
            con.close()
            self.feature2()
            self.plot()

      def mst(self):
            offset=100
            dist1x =[]
            dist1y =[]
            dist2x =[]
            dist2y = []
            dist1x,dist1y,dist2x,dist2y = self.getpoints()
            self.newmap(100)
            cmd = 'g++ mst.cpp'
            os.system(cmd)
            cmd = './a.out'
            os.system(cmd)
            file1 = open("output.txt", "r")
            out = re.split(' ',file1.read())

            # print(out)
            #----PLOT
            for i in self.canvases:
                  i.get_tk_widget().pack_forget() 
            for i in self.toolbars:
                  i.destroy()
            self.canvases.clear()
            self.toolbars.clear()

            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            patients = []
            circles= []
            square = []
            triangles = []
            hospitals = []
            localities = []
            try:
                  cur.execute('''SELECT * FROM PATIENT;''')
                  patients = cur.fetchall()
                  cur.execute('''SELECT * FROM HOSPITALS''')
                  hospitals = cur.fetchall()
                  cur.execute('''SELECT * FROM LOCALITY''')
                  localities = cur.fetchall()
                  cur.execute('''SELECT * FROM SQUARE;''')
                  square = cur.fetchall()
                  cur.execute('''SELECT * FROM TRIANGLE;''')
                  triangles = cur.fetchall()
                  cur.execute('''SELECT * FROM CIRCLE;''')
                  circles = cur.fetchall()
                  hospitals = np.array(hospitals,dtype=np.dtype(int))
                  patients = np.array(patients,dtype=np.dtype(int))
                  localities = np.array(localities,dtype=np.dtype(int))
            except:
                  print("Error")
            con.close() 
            fig = Figure(figsize = (13, 10),dpi = 100) 

            # adding the subplot 
            rect=[]
            rect1=[]
            rect3 = []
            plot1 = fig.add_subplot(111)

            for sq in square:
                  rectangle = matplotlib.patches.Rectangle((sq[0],sq[1]), sq[2], sq[3], color='orange', alpha =0.5)
                  plot1.add_patch(rectangle)
            for cir in circles:
                  circle = matplotlib.patches.Circle((cir[0],cir[1]),radius = cir[2], color='green',alpha=0.5)
                  plot1.add_patch(circle)
            for tri in triangles:
                  li = []
                  li.append((tri[0],tri[1]))
                  li.append((tri[2],tri[3]))
                  li.append((tri[4],tri[5]))
                  li = np.array(li)
                  # print(li)
                  trian = matplotlib.patches.Polygon(li, closed=True,fill=True,color = 'orange', alpha = 0.5)
                  plot1.add_patch(trian)
            plot1.scatter(hospitals[:,0],hospitals[:,1],color='green',marker="P") 
            plot1.scatter(patients[:,0],patients[:,1],color='red')
            # plot1.scatter(localities[:,0],localities[:,1],color='black')
            
            i=0
            i=int(i)

            # while(i<len(out)):
            #       path = []
            #       path.append(self.getoriginal(out[i],100))
            #       i+=1
            #       path.append(self.getoriginal(out[i],100))
            #       i+=1
            #       path = np.array(path)
            #       plot1.plot(path[:,0],path[:,1],color = 'blue')
            
            
            final= []
            for i in out:
                  node1 = i
                  node1 = self.getoriginal(node1,100)
                  plot1.scatter(node1[0],node1[1],color='black')
            for i in range(len(out)-1):
                  initpos = int(out[i])
                  cur = int(out[i+1])
                  dist = np.full((offset*offset+4),np.inf)
                  dist[initpos] = 0
                  q, parent = [(0,initpos)],{initpos: -1}
                  while q:
                        (cost,v1) = heappop(q)
                        for c, v2 in self.adj.get(v1,()):
                              if (dist[v1]+c < dist[v2]):
                                    dist[v2] = dist[v1]+c 
                                    parent[v2] = v1
                                    heappush(q, (dist[v2], v2))

                  #-----get required path
                  path = []
                  par = parent[cur]
                  path.append(self.getoriginal(cur,offset))
                  while (par!=-1):
                        path.append(self.getoriginal(par,offset))
                        par = parent[par]
                  path.reverse()
                  final = final + path
           
            final = np.array(final)

            plot1.plot(final[:,0],final[:,1],color = 'blue')


            # plotting the graph 
            for i in range (len(dist1x)):
                  rect.append(matplotlib.patches.Circle((dist1x[i],dist1y[i]),radius = 0.5, color='red',alpha=0.4))
                  plot1.add_patch(rect[i])

            for i in patients:
                  temp = matplotlib.patches.Circle((i[0],i[1]),radius = 0.5, color='red',alpha=0.4)
                  plot1.add_patch(temp)
                  
            for i in range (len(dist2x)):
                  rect1.append(matplotlib.patches.Circle((dist2x[i],dist2y[i]),radius = 0.5, color='yellow',alpha=0.4))
                  plot1.add_patch(rect1[i])
            # creating the Tkinter canvas 
            # containing the Matplotlib figure 
            canvas = FigureCanvasTkAgg(fig,master = self.root)   
            self.canvases.append(canvas)
            
            canvas.draw() 
            
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)
            
            # creating the Matplotlib toolbar s
            toolbar = NavigationToolbar2Tk(canvas,self.root)
            toolbar.update() 
            self.toolbars.append(toolbar)
            
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)


      def plot(self): 
            for i in self.canvases:
                  i.get_tk_widget().pack_forget() 
            for i in self.toolbars:
                  i.destroy()
            self.canvases.clear()
            self.toolbars.clear()
            hospital_x = []
            infected_x = []
            infected_y = []
            hospital_y = []
            square = []
            circles = []
            triangles = []
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            try:
                  cur.execute('''SELECT X from HOSPITALS''')
                  hospital_x = cur.fetchall()
                  cur.execute('''SELECT Y from HOSPITALS''')
                  hospital_y = cur.fetchall()
                  cur.execute('''SELECT * FROM SQUARE;''')
                  square = cur.fetchall()
                  cur.execute('''SELECT * FROM TRIANGLE;''')
                  triangles = cur.fetchall()
                  cur.execute('''SELECT * FROM CIRCLE;''')
                  circles = cur.fetchall()
                  cur.execute('''SELECT X from PATIENT''')
                  infected_x = cur.fetchall()
                  cur.execute('''SELECT Y from PATIENT''')
                  infected_y = cur.fetchall()
            except:
                  print("error")
            # the figure that will contain the plot 
            fig = Figure(figsize = (13, 10),dpi = 100) 

            # adding the subplot 
            plot1 = fig.add_subplot(111)
            for sq in square:
                  rectangle = matplotlib.patches.Rectangle((sq[0],sq[1]), sq[2], sq[3], color='orange', alpha =0.5)
                  plot1.add_patch(rectangle)
            for cir in circles:
                  circle = matplotlib.patches.Circle((cir[0],cir[1]),radius = cir[2], color='green',alpha=0.5)
                  plot1.add_patch(circle)
            for tri in triangles:
                  li = []
                  li.append((tri[0],tri[1]))
                  li.append((tri[2],tri[3]))
                  li.append((tri[4],tri[5]))
                  li = np.array(li)
                  # print(li)
                  trian = matplotlib.patches.Polygon(li, closed=True,fill=True,color = 'orange', alpha = 0.5)
                  plot1.add_patch(trian)
            plot1.scatter(hospital_x,hospital_y,color='green',marker="P") 
            plot1.scatter(infected_x,infected_y,color='red')
            # plotting the graph 
            
            # creating the Tkinter canvas 
            # containing the Matplotlib figure 
            canvas = FigureCanvasTkAgg(fig,master = self.root)   
            self.canvases.append(canvas)
            
            canvas.draw() 
            
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)
            
            # creating the Matplotlib toolbar s
            toolbar = NavigationToolbar2Tk(canvas,self.root)
            toolbar.update() 
            self.toolbars.append(toolbar)
            
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)       

      def clear_data(self):
            self.pat_y.set(0)
            self.hosp_x.set(0)
            self.hosp_y.set(0)
            self.pat_x.set(0)

      def getpoints(self):
            dist = np.full((104, 104), np.inf)
            hospitals = []
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            try:
                  cur.execute('''SELECT * FROM PATIENT;''')
                  row = cur.fetchall()
                  cur.execute('''SELECT * FROM HOSPITALS''')
                  hospitals = cur.fetchall()
            except:
                  print("Error")
            hospitals = np.array(hospitals,dtype=np.dtype(int))
            con.close()
            queue = []  
            for i in row:
                  queue.append(i)
                  x = int(i[0])
                  y = int(i[1])
                  dist[x][y]=0
            while queue: 
                  s = queue.pop(0) 
                  x = int(s[0])
                  y = int (s[1])
                  d = [(-1,0),(0,1),(1,0),(0,-1)]
                  for coord in d:
                        xn=x+coord[0]
                        yn=y+coord[1]
                        if (dist[xn][yn]>dist[x][y]+1):
                              dist[xn][yn]=dist[x][y]+1
                              if(dist[xn][yn] <= 2):
                                    queue.append((xn,yn))
            dist1x = []
            dist1y  = [] 
            for i in range(100):
                  for j in range(100):
                        if(dist[i][j]==1):
                              dist1x.append(i)
                              dist1y.append(j)
            dist2x = []
            dist2y  = [] 
            for i in range(100):
                  for j in range(100):
                        if(dist[i][j]==2):
                              dist2x.append(i)
                              dist2y.append(j)
            return dist1x,dist1y,dist2x,dist2y

      def Zone_Marking(self):
            
            dist = np.full((104, 104), np.inf)
            hospitals = []
            square = []
            circles = []
            triangles = []
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            try:
                  cur.execute('''SELECT * FROM PATIENT;''')
                  row = cur.fetchall()
                  cur.execute('''SELECT * FROM HOSPITALS''')
                  hospitals = cur.fetchall()
                  cur.execute('''SELECT * FROM SQUARE;''')
                  square = cur.fetchall()
                  cur.execute('''SELECT * FROM TRIANGLE;''')
                  triangles = cur.fetchall()
                  cur.execute('''SELECT * FROM CIRCLE;''')
                  circles = cur.fetchall()
                  
            except:
                  print("Error")
            hospitals = np.array(hospitals,dtype=np.dtype(int))
            con.close()
            queue = []  
            for i in row:
                  queue.append(i)
                  x = int(i[0])
                  y = int(i[1])
                  dist[x][y]=0
            while queue: 
                  s = queue.pop(0) 
                  x = int(s[0])
                  y = int (s[1])
                  d = [(-1,0),(0,1),(1,0),(0,-1)]
                  for coord in d:
                        xn=x+coord[0]
                        yn=y+coord[1]
                        if (dist[xn][yn]>dist[x][y]+1):
                              dist[xn][yn]=dist[x][y]+1
                              if(dist[xn][yn] <= 2):
                                    queue.append((xn,yn))
            for i in self.canvases:
                  i.get_tk_widget().pack_forget() 
            for i in self.toolbars:
                  i.destroy()
            self.canvases.clear()
            self.toolbars.clear()
            dist1x = []
            dist1y  = [] 
            for i in range(100):
                  for j in range(100):
                        if(dist[i][j]==1):
                              dist1x.append(i)
                              dist1y.append(j)
            dist2x = []
            dist2y  = [] 
            for i in range(100):
                  for j in range(100):
                        if(dist[i][j]==2):
                              dist2x.append(i)
                              dist2y.append(j)

            fig = Figure(figsize = (13, 10),dpi = 100) 
            plot1=fig.add_subplot(111)
            # for sq in square:
            #       rectangle = matplotlib.patches.Rectangle((sq[0],sq[1]), sq[2], sq[3], color='snow3', alpha =0.5)
            #       plot1.add_patch(rectangle)
            # for cir in circles:
            #       circle = matplotlib.patches.Circle((cir[0],cir[1]),radius = cir[2], color='green',alpha=0.5)
            #       plot1.add_patch(circle)
            # for tri in triangles:
            #       li = []
            #       li.append((tri[0],tri[1]))
            #       li.append((tri[2],tri[3]))
            #       li.append((tri[4],tri[5]))
            #       li = np.array(li)
            #       # print(li)
            #       trian = matplotlib.patches.Polygon(li, closed=True,fill=True,color = 'snow3', alpha = 0.5)
            #       plot1.add_patch(trian)
            rect=[]
            rect1=[]
            rect3 = []
            infected_x = []
            infected_y = []
            for i in row:
                  infected_x.append(i[0])
                  infected_y.append(i[1])

            for i in range (len(dist1x)):
                  rect.append(matplotlib.patches.Circle((dist1x[i],dist1y[i]),radius = 0.5, color='red',alpha=0.4))
                  plot1.add_patch(rect[i])

            for i in range (len(infected_x)):
                  rect3.append(matplotlib.patches.Circle((infected_x[i],infected_y[i]),radius = 0.5, color='red',alpha=0.4))
                  plot1.add_patch(rect3[i])
                  
            for i in range (len(dist2x)):
                  rect1.append(matplotlib.patches.Circle((dist2x[i],dist2y[i]),radius = 0.5, color='yellow',alpha=0.4))
                  plot1.add_patch(rect1[i])

            plot1.scatter(hospitals[:,0],hospitals[:,1],color='green',marker="P") 
            plot1.scatter(infected_x,infected_y,color='black',marker="X")

            canvas = FigureCanvasTkAgg(fig,master = self.root)   
            self.canvases.append(canvas)
            
            canvas.draw() 
            
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)
            
            # creating the Matplotlib toolbar s
            toolbar = NavigationToolbar2Tk(canvas,self.root)
            toolbar.update() 
            self.toolbars.append(toolbar)
            
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)

       

      def getoriginal(self,idx,offset):
            idx = int(idx)
            offset = int(offset)
            x = idx%offset
            y = int(idx/offset)
            return x,y

      def converttoidx(self,x,y,offset):
            x = int(x)
            y = int(y)
            return x+y*offset

      def connectgraph(self,offset):
            d = [(-1,0),(0,1),(1,0),(0,-1)]
            adj = defaultdict(list)
            for i in range(offset):
                  for j in range(offset):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<0 or int(x)>=offset):
                                    continue
                              if(int(y)<0 or int(y)>=offset):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))
                              if ((1,u) not in adj[v]):             
                                    adj[v].append((1,u))
            return adj
      
      def feature2(self):
            dist1x =[]
            dist1y =[]
            dist2x =[]
            dist2y = []
            circles =[]
            square = []
            triangles = []
            dist1x,dist1y,dist2x,dist2y = self.getpoints()
            offset = 100
            x = self.cur_x.get()
            y =  self.cur_y.get()
            initpos = self.converttoidx(x,y,offset)
            #---VARIABLES--------------
            
            hospitals = []
            

            #----INPUT OF CURRENT POSITION-----------

            #----DATABSE QUERY----------------
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            row = []
            try:
                  cur.execute('''SELECT * FROM HOSPITALS;''')
                  row = cur.fetchall()
            except:
                  print("Error")
            con.close()

            for i in row:
                  x = int(i[0])
                  y = int(i[1])
                  idx = self.converttoidx(x,y,offset)
                  hospitals.append(idx)
 
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            patients = []
            try:
                  cur.execute('''SELECT * FROM PATIENT;''')
                  patients = cur.fetchall()
                  ocalities = cur.fetchall()
                  cur.execute('''SELECT * FROM SQUARE;''')
                  square = cur.fetchall()
                  cur.execute('''SELECT * FROM TRIANGLE;''')
                  triangles = cur.fetchall()
                  cur.execute('''SELECT * FROM CIRCLE;''')
                  circles = cur.fetchall()
            except:
                  print("Error")
            con.close() 

            # for i in self.adj[407]:
            #       print(i)
            #-----UPDATION OF ADJACENCY LIST------------
            d = [(-1,0),(0,1),(1,0),(0,-1)]
            for i in patients:
                  x = int(i[0])
                  y = int(i[1])
                  u = self.converttoidx(x,y,offset)
                  for k in d:
                        xi = x + k[0]
                        yi = y + k[1]
                        v = self.converttoidx(xi,yi,offset)
                        if((1,v) in self.adj[u]):
                              it = [j for j in range(len(self.adj[u])) if self.adj[u][j]==(1,v)]
                              self.adj[u][it[0]] = (100,v)
                              it = [j for j in range(len(self.adj[v])) if self.adj[v][j]==(1,u)]
                              self.adj[v][it[0]] = (100,u)

            for i in range(len(dist1x)):
                  x = int(dist1x[i])
                  y = int(dist1y[i])
                  u = self.converttoidx(x,y,offset)
                  for k in d:
                        xi = x + k[0]
                        yi = y + k[1]
                        v = self.converttoidx(xi,yi,offset)
                        if((1,v) in self.adj[u]):
                              it = [j for j in range(len(self.adj[u])) if (self.adj[u][j]==(1,v))]
                              self.adj[u][it[0]] = (100,v)
                              it = [j for j in range(len(self.adj[v])) if self.adj[v][j]==(1,u)]
                              self.adj[v][it[0]] = (100,u)
            
            for i in range(len(dist2x)):
                  x = int(dist2x[i])
                  y = int(dist2y[i])
                  u = self.converttoidx(x,y,offset)
                  for k in d:
                        xi = x + k[0]
                        yi = y + k[1]
                        v = self.converttoidx(xi,yi,offset)
                        if(((1,v) in self.adj[u])):
                              it = [j for j in range(len(self.adj[u])) if (self.adj[u][j]==(1,v))]
                              self.adj[u][it[0]] = (50,v)
                              it = [j for j in range(len(self.adj[v])) if self.adj[v][j]==(1,u)]
                              self.adj[v][it[0]] = (50,u)
            

            #--q is min heap---------
            #---parent is array for backtracking-------
            #--Dijkstras Algo---------
            dist = np.full((offset*offset+4),20000)
            dist[initpos]=0
            q, parent = [(0,initpos)],{initpos: -1}
            while q:
                  (cost,v1) = heappop(q)
                  for c, v2 in self.adj.get(v1,()):
                        if (dist[v1]+c < dist[v2]):
                              dist[v2] = dist[v1]+c 
                              parent[v2] = v1
                              heappush(q, (dist[v2], v2))

            #-----get nearest Hopital
            cur = initpos
            mini = np.inf
            for i in hospitals:
                  if(mini>dist[i]):
                        mini=dist[i]
                        cur = i

            #-----get required path
            path = []
            par = parent[cur]
            path.append(self.getoriginal(cur,offset))
            while (par!=-1):
                  path.append(self.getoriginal(par,offset))
                  par = parent[par]
            path.reverse()
            path = np.array(path)

            #----PLOT
            for i in self.canvases:
                  i.get_tk_widget().pack_forget() 
            for i in self.toolbars:
                  i.destroy()
            self.canvases.clear()
            self.toolbars.clear()

            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            patients = []
            hospitals = []
            try:
                  cur.execute('''SELECT * FROM PATIENT;''')
                  patients = cur.fetchall()
                  cur.execute('''SELECT * FROM HOSPITALS''')
                  hospitals = cur.fetchall()
                  hospitals = np.array(hospitals,dtype=np.dtype(int))
                  patients = np.array(patients,dtype=np.dtype(int))
            except:
                  print("Error")
            con.close() 
            fig = Figure(figsize = (13, 10),dpi = 100) 

            # adding the subplot 
            rect=[]
            rect1=[]
            rect3 = []
            plot1 = fig.add_subplot(111)
            for sq in square:
                  rectangle = matplotlib.patches.Rectangle((sq[0],sq[1]), sq[2], sq[3], color='orange', alpha =0.5)
                  plot1.add_patch(rectangle)
            for cir in circles:
                  circle = matplotlib.patches.Circle((cir[0],cir[1]),radius = cir[2], color='green',alpha=0.5)
                  plot1.add_patch(circle)
            for tri in triangles:
                  li = []
                  li.append((tri[0],tri[1]))
                  li.append((tri[2],tri[3]))
                  li.append((tri[4],tri[5]))
                  li = np.array(li)
                  # print(li)
                  trian = matplotlib.patches.Polygon(li, closed=True,fill=True,color = 'orange', alpha = 0.5)
                  plot1.add_patch(trian)
            plot1.scatter(hospitals[:,0],hospitals[:,1],color='green',marker="P") 
            plot1.scatter(patients[:,0],patients[:,1],color='red')
            curpos = self.getoriginal(initpos,offset)
            plot1.scatter(curpos[0],curpos[1],color='black')
            plot1.plot(path[:,0],path[:,1])
            # plotting the graph 
            for i in range (len(dist1x)):
                  rect.append(matplotlib.patches.Circle((dist1x[i],dist1y[i]),radius = 0.5, color='red',alpha=0.4))
                  plot1.add_patch(rect[i])

            for i in patients:
                  temp = matplotlib.patches.Circle((i[0],i[1]),radius = 0.5, color='red',alpha=0.4)
                  plot1.add_patch(temp)
                  
            for i in range (len(dist2x)):
                  rect1.append(matplotlib.patches.Circle((dist2x[i],dist2y[i]),radius = 0.5, color='yellow',alpha=0.4))
                  plot1.add_patch(rect1[i])
            # creating the Tkinter canvas 
            # containing the Matplotlib figure 
            canvas = FigureCanvasTkAgg(fig,master = self.root)   
            self.canvases.append(canvas)
            
            canvas.draw() 
            
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)
            
            # creating the Matplotlib toolbar s
            toolbar = NavigationToolbar2Tk(canvas,self.root)
            toolbar.update() 
            self.toolbars.append(toolbar)
            
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False) 

      def handler(self):
            if(self.flag=="Patient"):
                  self.pathforpatient()
            else:
                  self.feature2()

      def pathforpatient(self):
            dist1x =[]
            dist1y =[]
            dist2x =[]
            dist2y = []
            dist1x,dist1y,dist2x,dist2y = self.getpoints()
            offset = 100
            x = self.cur_x.get()
            y =  self.cur_y.get()
            initpos = self.converttoidx(x,y,offset)
            #---VARIABLES--------------
            
            hospitals = []
            circles = []
            square = []
            triangles = []

            #----INPUT OF CURRENT POSITION-----------

            #----DATABSE QUERY----------------
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            row = []
            try:
                  cur.execute('''SELECT * FROM HOSPITALS;''')
                  row = cur.fetchall()
                  cur.execute('''SELECT * FROM SQUARE;''')
                  square = cur.fetchall()
                  cur.execute('''SELECT * FROM TRIANGLE;''')
                  triangles = cur.fetchall()
                  cur.execute('''SELECT * FROM CIRCLE;''')
                  circles = cur.fetchall()
            except:
                  print("Error")
            con.close()

            for i in row:
                  x = int(i[0])
                  y = int(i[1])
                  idx = self.converttoidx(x,y,offset)
                  hospitals.append(idx)
 
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            patients = []
            try:
                  cur.execute('''SELECT * FROM PATIENT;''')
                  patients = cur.fetchall()
            except:
                  print("Error")
            con.close() 

            d = [(-1,0),(0,1),(1,0),(0,-1)]
            adj = defaultdict(list)
            for i in range(offset):
                  for j in range(offset):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<0 or int(x)>=offset):
                                    continue
                              if(int(y)<0 or int(y)>=offset):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((100000,v) not in adj[u]):
                                    adj[u].append((100000,v))
                              if ((100000,u) not in adj[v]):             
                                    adj[v].append((100000,u))

            #-----UPDATION OF ADJACENCY LIST------------
      
            for i in patients:
                  x = int(i[0])
                  y = int(i[1])
                  u = self.converttoidx(x,y,offset)
                  for k in d:
                        xi = x + k[0]
                        yi = y + k[1]
                        v = self.converttoidx(xi,yi,offset)
                        if((100000,v) in adj[u]):
                              it = [j for j in range(len(adj[u])) if adj[u][j]==(100000,v)]
                              adj[u][it[0]] = (1,v)
                              it = [j for j in range(len(adj[v])) if adj[v][j]==(100000,u)]
                              adj[v][it[0]] = (1,u)

            for i in range(len(dist1x)):
                  x = int(dist1x[i])
                  y = int(dist1y[i])
                  u = self.converttoidx(x,y,offset)
                  for k in d:
                        xi = x + k[0]
                        yi = y + k[1]
                        v = self.converttoidx(xi,yi,offset)
                        if((100000,v) in adj[u]):
                              it = [j for j in range(len(adj[u])) if (adj[u][j]==(100000,v))]
                              adj[u][it[0]] = (20,v)
                              it = [j for j in range(len(adj[v])) if adj[v][j]==(100000,u)]
                              adj[v][it[0]] = (20,u)
            
            for i in range(len(dist2x)):
                  x = int(dist2x[i])
                  y = int(dist2y[i])
                  u = self.converttoidx(x,y,offset)
                  for k in d:
                        xi = x + k[0]
                        yi = y + k[1]
                        v = self.converttoidx(xi,yi,offset)
                        if(((100000,v) in adj[u])):
                              it = [j for j in range(len(adj[u])) if (adj[u][j]==(100000,v))]
                              adj[u][it[0]] = (50,v)
                              it = [j for j in range(len(adj[v])) if adj[v][j]==(100000,u)]
                              adj[v][it[0]] = (50,u)
            

            #--q is min heap---------
            #---parent is array for backtracking-------
            #--Dijkstras Algo---------
            dist = np.full((offset*offset+4),np.inf)
            dist[initpos]=0
            q, parent = [(0,initpos)],{initpos: -1}
            while q:
                  (cost,v1) = heappop(q)
                  for c, v2 in adj.get(v1,()):
                        if (dist[v1]+c < dist[v2]):
                              dist[v2] = dist[v1]+c 
                              parent[v2] = v1
                              heappush(q, (dist[v2], v2))

            #-----get nearest Hopital
            cur = initpos
            mini = np.inf
            for i in hospitals:
                  if(mini>dist[i]):
                        mini=dist[i]
                        cur = i

            #-----get required path
            path = []
            par = parent[cur]
            path.append(self.getoriginal(cur,offset))
            while (par!=-1):
                  path.append(self.getoriginal(par,offset))
                  par = parent[par]
            path.reverse()
            path = np.array(path)

            #----PLOT
            for i in self.canvases:
                  i.get_tk_widget().pack_forget() 
            for i in self.toolbars:
                  i.destroy()
            self.canvases.clear()
            self.toolbars.clear()

            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            patients = []
            hospitals = []
            try:
                  cur.execute('''SELECT * FROM PATIENT;''')
                  patients = cur.fetchall()
                  cur.execute('''SELECT * FROM HOSPITALS''')
                  hospitals = cur.fetchall()
                  hospitals = np.array(hospitals,dtype=np.dtype(int))
                  patients = np.array(patients,dtype=np.dtype(int))
            except:
                  print("Error")
            con.close() 
            fig = Figure(figsize = (13, 10),dpi = 100) 

            # adding the subplot 
            rect=[]
            rect1=[]
            rect3 = []
            plot1 = fig.add_subplot(111)
            for sq in square:
                  rectangle = matplotlib.patches.Rectangle((sq[0],sq[1]), sq[2], sq[3], color='orange', alpha =0.5)
                  plot1.add_patch(rectangle)
            for cir in circles:
                  circle = matplotlib.patches.Circle((cir[0],cir[1]),radius = cir[2], color='green',alpha=0.5)
                  plot1.add_patch(circle)
            for tri in triangles:
                  li = []
                  li.append((tri[0],tri[1]))
                  li.append((tri[2],tri[3]))
                  li.append((tri[4],tri[5]))
                  li = np.array(li)
                  # print(li)
                  trian = matplotlib.patches.Polygon(li, closed=True,fill=True,color = 'orange', alpha = 0.5)
                  plot1.add_patch(trian)
            plot1.scatter(hospitals[:,0],hospitals[:,1],color='green',marker="P") 
            plot1.scatter(patients[:,0],patients[:,1],color='red')
            curpos = self.getoriginal(initpos,offset)
            plot1.scatter(curpos[0],curpos[1],color='black')
            plot1.plot(path[:,0],path[:,1])
            # plotting the graph 
            for i in range (len(dist1x)):
                  rect.append(matplotlib.patches.Circle((dist1x[i],dist1y[i]),radius = 0.5, color='red',alpha=0.4))
                  plot1.add_patch(rect[i])

            for i in patients:
                  temp = matplotlib.patches.Circle((i[0],i[1]),radius = 0.5, color='red',alpha=0.4)
                  plot1.add_patch(temp)
                  
            for i in range (len(dist2x)):
                  rect1.append(matplotlib.patches.Circle((dist2x[i],dist2y[i]),radius = 0.5, color='yellow',alpha=0.4))
                  plot1.add_patch(rect1[i])
            # creating the Tkinter canvas 
            # containing the Matplotlib figure 
            canvas = FigureCanvasTkAgg(fig,master = self.root)   
            self.canvases.append(canvas)
            
            canvas.draw() 
            
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)
            
            # creating the Matplotlib toolbar s
            toolbar = NavigationToolbar2Tk(canvas,self.root)
            toolbar.update() 
            self.toolbars.append(toolbar)
            
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False) 
      def busstop(self):
            offset=100
            st = [4,5]
            en = [80,78]
            stp1 =[32,45]
            stp2 = [90,98]
            final  =[]
            path = []
            path1 = []
            path2= []
            dist1x =[]
            dist1y =[]
            dist2x =[]
            dist2y = []
            dist1x,dist1y,dist2x,dist2y = self.getpoints()
            dist = np.full((offset*offset+4),20000)
            initpos = self.converttoidx(st[0],st[1],offset)            
            dist[initpos]=0

            q, parent = [(0,initpos)],{initpos: -1}
            while q:
                  (cost,v1) = heappop(q)
                  for c, v2 in self.adj.get(v1,()):
                        if (dist[v1]+c < dist[v2]):
                              dist[v2] = dist[v1]+c 
                              parent[v2] = v1
                              heappush(q, (dist[v2], v2))
            cur = self.converttoidx(stp1[0],stp1[1],offset)
            par = parent[cur]
            path.append(self.getoriginal(cur,offset))
            while (par!=-1):
                  path.append(self.getoriginal(par,offset))
                  par = parent[par]
            path.reverse()

            dist = np.full((offset*offset+4),20000)
            initpos = self.converttoidx(stp1[0],stp1[1],offset)
            dist[initpos]=0
            q, parent = [(0,initpos)],{initpos: -1}
            while q:
                  (cost,v1) = heappop(q)
                  for c, v2 in self.adj.get(v1,()):
                        if (dist[v1]+c < dist[v2]):
                              dist[v2] = dist[v1]+c 
                              parent[v2] = v1
                              heappush(q, (dist[v2], v2))
            cur = self.converttoidx(stp2[0],stp2[1],offset)
            par = parent[cur]
            path1.append(self.getoriginal(cur,offset))
            while (par!=-1):
                  path1.append(self.getoriginal(par,offset))
                  par = parent[par]
            path1.reverse()

            dist = np.full((offset*offset+4),20000)
            initpos = self.converttoidx(stp2[0],stp2[1],offset)
            dist[initpos]=0
            q, parent = [(0,initpos)],{initpos: -1}
            while q:
                  (cost,v1) = heappop(q)
                  for c, v2 in self.adj.get(v1,()):
                        if (dist[v1]+c < dist[v2]):
                              dist[v2] = dist[v1]+c 
                              parent[v2] = v1
                              heappush(q, (dist[v2], v2))
            cur = self.converttoidx(en[0],en[1],offset)
            par = parent[cur]
            path2.append(self.getoriginal(cur,offset))
            while (par!=-1):
                  path2.append(self.getoriginal(par,offset))
                  par = parent[par]
            path2.reverse()

            final = path + path1 + path2

            final = np.array(final)

            for i in self.canvases:
                  i.get_tk_widget().pack_forget() 
            for i in self.toolbars:
                  i.destroy()
            self.canvases.clear()
            self.toolbars.clear()

            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            patients = []
            hospitals = []
            square= []
            circles=[]
            triangles= []
            try:
                  cur.execute('''SELECT * FROM PATIENT;''')
                  patients = cur.fetchall()
                  cur.execute('''SELECT * FROM HOSPITALS''')
                  hospitals = cur.fetchall()
                  cur.execute('''SELECT * FROM SQUARE;''')
                  square = cur.fetchall()
                  cur.execute('''SELECT * FROM TRIANGLE;''')
                  triangles = cur.fetchall()
                  cur.execute('''SELECT * FROM CIRCLE;''')
                  circles = cur.fetchall()
                  hospitals = np.array(hospitals,dtype=np.dtype(int))
                  patients = np.array(patients,dtype=np.dtype(int))
            except:
                  print("Error")
            con.close() 
            fig = Figure(figsize = (13, 10),dpi = 100) 
            plot1 = fig.add_subplot(111)
            for sq in square:
                  rectangle = matplotlib.patches.Rectangle((sq[0],sq[1]), sq[2], sq[3], color='orange', alpha =0.5)
                  plot1.add_patch(rectangle)
            for cir in circles:
                  circle = matplotlib.patches.Circle((cir[0],cir[1]),radius = cir[2], color='green',alpha=0.5)
                  plot1.add_patch(circle)
            for tri in triangles:
                  li = []
                  li.append((tri[0],tri[1]))
                  li.append((tri[2],tri[3]))
                  li.append((tri[4],tri[5]))
                  li = np.array(li)
                  # print(li)
                  trian = matplotlib.patches.Polygon(li, closed=True,fill=True,color = 'orange', alpha = 0.5)
                  plot1.add_patch(trian)
            # adding the subplot 
            rect=[]
            rect1=[]
            rect3 = []
            
            plot1.scatter(hospitals[:,0],hospitals[:,1],color='green',marker="P") 
            plot1.scatter(patients[:,0],patients[:,1],color='red')
            curpos = self.getoriginal(initpos,offset)
            plot1.scatter(curpos[0],curpos[1],color='black')
            plot1.plot(final[:,0],final[:,1])
            plot1.scatter(st[0],st[1],color = 'purple')
            plot1.scatter(stp1[0],stp1[1],color = 'purple')
            plot1.scatter(stp2[0],stp2[1],color = 'purple')
            plot1.scatter(en[0],en[1],color = 'purple')
            # plotting the graph 
            for i in range (len(dist1x)):
                  rect.append(matplotlib.patches.Circle((dist1x[i],dist1y[i]),radius = 0.5, color='red',alpha=0.4))
                  plot1.add_patch(rect[i])

            for i in patients:
                  temp = matplotlib.patches.Circle((i[0],i[1]),radius = 0.5, color='red',alpha=0.4)
                  plot1.add_patch(temp)
                  
            for i in range (len(dist2x)):
                  rect1.append(matplotlib.patches.Circle((dist2x[i],dist2y[i]),radius = 0.5, color='yellow',alpha=0.4))
                  plot1.add_patch(rect1[i])
            # creating the Tkinter canvas 
            # containing the Matplotlib figure 
            canvas = FigureCanvasTkAgg(fig,master = self.root)   
            self.canvases.append(canvas)
            
            canvas.draw() 
            
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)
            
            # creating the Matplotlib toolbar s
            toolbar = NavigationToolbar2Tk(canvas,self.root)
            toolbar.update() 
            self.toolbars.append(toolbar)
            
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)

      def probability(self):

                  #-----INPUT------

            x= self.cur_x.get()
            y= self.cur_y.get()
            offset = 100
            pos = self.converttoidx(x,y,offset)

                  #------DATABASE QUERY-------

            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            row = []
            patients = []
            try:
                  cur.execute('''SELECT * FROM PATIENT;''')
                  row = cur.fetchall()
            except:
                  print("Error")
            con.close() 

            for i in row:
                  x = int(i[0])
                  y = int(i[1])
                  idx = self.converttoidx(x,y,offset)
                  patients.append(idx)

            #-----Distance Calculation------

            dist = np.full((offset*offset+4),100000)
            dist[pos]=0
            adj = self.connectgraph(offset)
            q = [(0,pos)]
            while q:
                  (cost,v1) = heappop(q)
                  for c, v2 in adj.get(v1,()):
                        if (dist[v1]+c < dist[v2]):
                              dist[v2] = dist[v1]+c 
                              heappush(q, (dist[v2], v2))

            #---------Probability Calculation---------
            product = 1
            n = 0
            probability = 100
            alpha = 1.5
            for i in patients:
                     # print(dist[i])
                     if(dist[i]<=100):
                        # product = product*dist[i]
                        n=n+1
            for i in patients:
                     # print(dist[i])
                     if(dist[i]<=100):
                        product = product*(dist[i]**(1.0/n))
                        n=n+1
                     # print(product)

            # print(product)
            probability = 0.0
            if(product<10):
                  probability = 100.0 - 1.25*product
            elif(product>=10 and product<15):
                  probability = 100 - 1.5*product
            elif(product>=15 and product<20):
                  probability = 100.0 - 3*product
            elif(product>=20 and product<25):
                  probability = 100.0 - 2.3*product
            elif(product>=25 and product <40):
                  probability = 100.0 - 2.3*product
            elif(product>=40 and product<75):
                  probability = 100 - 1.5*product
            else:
                  probability = 100 - product

            if(probability<0):
                  probability = 0.0

            self.probab.set(round(probability,2))

            return
      
      def retrace_optimal_path(self,memo, n):
            points_to_retrace = tuple(range(n))
            full_path_memo = dict((k, v) for k, v in memo.items() if k[0] == points_to_retrace)

            # print(full_path_memo)
            path_key = min(full_path_memo.keys(), key=lambda x: full_path_memo[x][0])

            # print(path_key)
            last_point = path_key[1]
            optimal_cost, next_to_last_point = memo[path_key]
            optimal_path = [last_point]

            # print(optimal_path)

            # print(points_to_retrace)
            while next_to_last_point is not None:
                  points_to_retrace = tuple(sorted(set(points_to_retrace).difference({last_point})))
                  last_point = next_to_last_point
                  path_key = (points_to_retrace, last_point)
                  _, next_to_last_point = memo[path_key]
                  optimal_path = [last_point] + optimal_path
            return optimal_path, optimal_cost


      def DP_TSP(self,distances_array):

            n = len(distances_array)
            all_points_set = set(range(n))
            
            # memo keys: tuple(sorted_points_in_path, last_point_in_path)
            # memo values: tuple(cost_thus_far, next_to_last_point_in_path)
            memo = {(tuple([i]), i): tuple([0, None]) for i in range(1)}
            queue = [(tuple([i]), i) for i in range(1)]
      
            while queue:
                  prev_visited, prev_last_point = queue.pop(0)
                  prev_dist, _ = memo[(prev_visited, prev_last_point)]
                  to_visit = all_points_set.difference(set(prev_visited))
                  #     print("in")
                  for new_last_point in to_visit:
                        new_visited = tuple(sorted(list(prev_visited) + [new_last_point]))
                        new_dist = (prev_dist + distances_array[prev_last_point][new_last_point])
                        
                        if (new_visited, new_last_point) not in memo:
                              memo[(new_visited, new_last_point)] = (new_dist, prev_last_point)
                              queue += [(new_visited, new_last_point)]
                        else:
                              if new_dist < memo[(new_visited, new_last_point)][0]:
                                    memo[(new_visited, new_last_point)] = (new_dist, prev_last_point)
            # for i in memo:
            #       print(i, memo[i])
            optimal_path, optimal_cost = self.retrace_optimal_path(memo, n)
            return optimal_path, optimal_cost
      
      def feature5(self):
            offset=100
            con=sqlite3.connect('Pandemic.db')
            cur = con.cursor()
            row = []
            houses = []
            patients = []
            hospitals = []
            square= []
            circles=[]
            triangles= []
            localities = []
            dist1x =[]
            dist1y =[]
            dist2x =[]
            dist2y = []
            dist1x,dist1y,dist2x,dist2y = self.getpoints()
            newmaplist = defaultdict(list)
            try:
                  cur.execute('''SELECT * FROM LOCALITY;''')
                  row = cur.fetchall()
                  cur.execute('''SELECT * FROM PATIENT;''')
                  patients = cur.fetchall()
                  cur.execute('''SELECT * FROM HOSPITALS''')
                  hospitals = cur.fetchall()
                  cur.execute('''SELECT * FROM LOCALITY''')
                  localities = cur.fetchall()
                  cur.execute('''SELECT * FROM SQUARE;''')
                  square = cur.fetchall()
                  cur.execute('''SELECT * FROM TRIANGLE;''')
                  triangles = cur.fetchall()
                  cur.execute('''SELECT * FROM CIRCLE;''')
                  circles = cur.fetchall()
            except:
                  print("error in newmap")
            for i in row:
                  x = int(i[0])
                  y = int(i[1])
                  u = self.converttoidx(x,y,offset)
                  houses.append(u)
            for i in range(len(houses)):
                  #--q is min heap---------
                  #---parent is array for backtracking-------
                  #--Dijkstras Algo---------
                  q, parent = [(0,houses[i])],{houses[i]: -1}
                  dist = np.full((offset*offset+4),np.inf)
                  dist[houses[i]]=0
                  while q:
                        (cost,v1) = heappop(q)
                        for c, v2 in self.adj.get(v1,()):
                              if (dist[v1]+c < dist[v2]):
                                    dist[v2] = dist[v1]+c 
                                    parent[v2] = v1
                                    heappush(q, (dist[v2], v2))
                  for j in range(len(houses)):
                        newmaplist[houses[i]].append((dist[houses[j]],houses[j]))
            sz = len(houses)
            arr = np.full((sz, sz), np.inf)
            for i in houses:
                  for j in range(len(newmaplist[i])):
                        node1 = houses.index(i)
                        node2 = houses.index(newmaplist[i][j][1])
                        cost = newmaplist[i][j][0]
                        arr[node1][node2]=cost
            # for i in range(sz):
            #       for j in range(sz):
            #             print(str(arr[i][j])+" ",end='')
            #       print("\n")
            a,b = self.DP_TSP(arr)

            #----PLOT
            for i in self.canvases:
                  i.get_tk_widget().pack_forget() 
            for i in self.toolbars:
                  i.destroy()
            final =[]
            self.canvases.clear()
            self.toolbars.clear()
            fig = Figure(figsize = (13, 10),dpi = 100) 
            plot1 = fig.add_subplot(111)

            #TYPE1
            # for i in a:
            #       node1 = houses[i]
            #       node1 = self.getoriginal(node1,100)
            #       plot1.scatter(node1[0],node1[1],color='black')
            #       final.append(node1)

            # final = np.array(final)

            # plot1.plot(final[:,0],final[:,1],color = 'blue')

            #TYPE-2
            final= []
            for i in a:
                  node1 = houses[i]
                  node1 = self.getoriginal(node1,100)
                  plot1.scatter(node1[0],node1[1],color='black')
            for i in range(len(a)-1):
                  initpos = houses[a[i]]
                  cur = houses[a[i+1]]
                  dist = np.full((offset*offset+4),20000)
                  dist[initpos]=0
                  q, parent = [(0,initpos)],{initpos: -1}
                  while q:
                        (cost,v1) = heappop(q)
                        for c, v2 in self.adj.get(v1,()):
                              if (dist[v1]+c < dist[v2]):
                                    dist[v2] = dist[v1]+c 
                                    parent[v2] = v1
                                    heappush(q, (dist[v2], v2))

                  #-----get required path
                  path = []
                  par = parent[cur]
                  path.append(self.getoriginal(cur,offset))
                  while (par!=-1):
                        path.append(self.getoriginal(par,offset))
                        par = parent[par]
                  path.reverse()
                  final = final + path
           
            final = np.array(final)

            plot1.plot(final[:,0],final[:,1],color = 'blue')

            hospitals = np.array(hospitals,dtype=np.dtype(int))
            patients = np.array(patients,dtype=np.dtype(int))
            localities = np.array(localities,dtype=np.dtype(int))
            rect=[]
            rect1=[]
            rect3 = []
            plot1 = fig.add_subplot(111)
            for sq in square:
                  rectangle = matplotlib.patches.Rectangle((sq[0],sq[1]), sq[2], sq[3], color='orange', alpha =0.5)
                  plot1.add_patch(rectangle)
            for cir in circles:
                  circle = matplotlib.patches.Circle((cir[0],cir[1]),radius = cir[2], color='green',alpha=0.5)
                  plot1.add_patch(circle)
            for tri in triangles:
                  li = []
                  li.append((tri[0],tri[1]))
                  li.append((tri[2],tri[3]))
                  li.append((tri[4],tri[5]))
                  li = np.array(li)
                  # print(li)
                  trian = matplotlib.patches.Polygon(li, closed=True,fill=True,color = 'orange', alpha = 0.5)
                  plot1.add_patch(trian)

            # plot1.scatter(hospitals[:,0],hospitals[:,1],color='green',marker="P") 
            plot1.scatter(patients[:,0],patients[:,1],color='red')
            
            for i in range (len(dist1x)):
                  rect.append(matplotlib.patches.Circle((dist1x[i],dist1y[i]),radius = 0.5, color='red',alpha=0.4))
                  plot1.add_patch(rect[i])

            for i in patients:
                  temp = matplotlib.patches.Circle((i[0],i[1]),radius = 0.5, color='red',alpha=0.4)
                  plot1.add_patch(temp)
                  
            for i in range (len(dist2x)):
                  rect1.append(matplotlib.patches.Circle((dist2x[i],dist2y[i]),radius = 0.5, color='yellow',alpha=0.4))
                  plot1.add_patch(rect1[i])

            canvas = FigureCanvasTkAgg(fig,master = self.root)   
            self.canvases.append(canvas)
            
            canvas.draw() 
            
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)
            
            # creating the Matplotlib toolbar s
            toolbar = NavigationToolbar2Tk(canvas,self.root)
            toolbar.update() 
            self.toolbars.append(toolbar)
            
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)

      def newmap2(self):
            offset=100
            d = [(-1,0),(0,1),(1,0),(0,-1)]
            adj = defaultdict(list)
            rand = 80
            offset = 100
            scamu1cord = 90
            scamu2cord = 90
            scamd1cord = 87
            scamd2cord = 87
            scamd3cord = 96
            scamd4cord = 96 
            newvar1 = 94
            newvar2 = 97
            newvar3 = 93
            checkvar=101
            for i in range(rand,scamd1cord):
                  for j in range(rand,scamu1cord):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<rand or int(x)>scamd1cord):
                                    continue
                              if(int(y)<rand or int(y)>scamu1cord):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))
                              

            for i in range(scamd2cord,scamd3cord):
                  for j in range(rand,scamu1cord):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<scamd2cord or int(x)>scamd3cord):
                                    continue
                              if(int(y)<rand or int(y)>scamu1cord):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))
                              

            for i in range(scamd4cord,checkvar):
                  for j in range(rand,scamu1cord):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<scamd4cord or int(x)>offset):
                                    continue
                              if(int(y)<rand or int(y)>scamu1cord):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))
                              
            
            for i in range(rand,scamd1cord):
                  for j in range(scamu2cord,checkvar):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<rand or int(x)>scamd1cord):
                                    continue
                              if(int(y)<scamu2cord or int(y)>offset):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))
                        


            for i in range(scamu2cord,checkvar):
                  for j in range(newvar1,checkvar):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<scamu2cord or int(x)>offset):
                                    continue
                              if(int(y)<newvar1 or int(y)>offset):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))
            

            for i in range(scamd1cord,scamu2cord):
                  for j in range(scamu2cord,newvar1):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<scamd1cord or int(x)>scamu2cord):
                                    continue
                              if(int(y)<scamu2cord or int(y)>=newvar1):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))
            
            for i in range(scamd1cord,scamu2cord):
                  for j in range(newvar1,newvar2):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<scamd1cord or int(x)>scamu2cord):
                                    continue
                              if(int(y)<newvar1 or int(y)>=newvar2):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))
            
            for i in range(scamd1cord,scamu2cord):
                  for j in range(newvar2,checkvar):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<scamd1cord or int(x)>scamu2cord):
                                    continue
                              if(int(y)<newvar2 or int(y)>offset):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))
            

            for i in range(scamu2cord,newvar3):
                  for j in range(scamu2cord,newvar1):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<scamu2cord or int(x)>=newvar3):
                                    continue
                              if(int(y)<scamu2cord or int(y)>=newvar1):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))

            for i in range(newvar3,scamd4cord):
                  for j in range(scamu2cord,newvar1):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<newvar3 or int(x)>scamd4cord):
                                    continue
                              if(int(y)<scamu2cord or int(y)>=newvar1):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))

            for i in range(scamd4cord,checkvar):
                  for j in range(scamu2cord,newvar1):
                        u = self.converttoidx(i,j,offset)
                        for k in d:
                              x = i + k[0]
                              y = j + k[1]
                              if(int(x)<scamd4cord or int(x)>offset):
                                    continue
                              if(int(y)<scamu2cord or int(y)>=newvar1):
                                    continue
                              v = self.converttoidx(x,y,offset)
                              if ((1,v) not in adj[u]):
                                    adj[u].append((1,v))

            adj[8993].append((1,9093))
            adj[9094].append((1,8994))
            adj[9397].append((1,9497))
            adj[9498].append((1,9398))
            adj[9390].append((1,9490))
            adj[9491].append((1,9391))
            adj[9989].append((1,9990))
            adj[9890].append((1,9889))


            sz = 0
            for i  in adj:
                  for j in range(len(adj[i])):
                        sz += 1
            file1 = open("input1.txt", "w+")
            file1.write(str(sz)+'\n')
            for i  in adj:
                  for j in range(len(adj[i])):
                        file1.write(str(i)+" "+str(adj[i][j][1])+"\n")
            # print(sz)
            file1.close() 

            cmd = 'g++ scc.cpp'
            os.system(cmd)
            cmd = './a.out'
            os.system(cmd)
            file1 = open("output1.txt", "r")
            # out = file1.readlines
            out = [line.rstrip() for line in file1.readlines()]

            for i in self.canvases:
                  i.get_tk_widget().pack_forget() 
            for i in self.toolbars:
                  i.destroy()
            self.canvases.clear()
            self.toolbars.clear()
            fig = Figure(figsize = (13, 10),dpi = 100) 
            plot1 = fig.add_subplot(111)

            lx = []
            ly = []
            for a in out:
                  if(a=='-'):
                        plot1.scatter(lx,ly)
                        lx = []
                        ly = []
                  else:
                        node1 = int(a)
                        temp = self.getoriginal(node1,offset)
                        if(temp[0] >= 100 or temp[1]>= 100):
                              continue
                        lx.append(temp[0])
                        ly.append(temp[1])
            plot1.scatter(lx,ly)

            # for i  in adj:
            #       for j in range(len(adj[i])):
            #             p1 = self.getoriginal(i,100)
            #             p2 = self.getoriginal(adj[i][j][1],100)
            #             lx = []
            #             ly= []
            #             lx.append(p1[0])
            #             lx.append(p2[0])
            #             ly.append(p1[1])
            #             ly.append(p2[1])
            #             plot1.plot(lx,ly,color = 'blue')
            plot1.set_ylim(30,101)
            plot1.set_xlim(30,101)
            canvas = FigureCanvasTkAgg(fig,master = self.root)   
            self.canvases.append(canvas)
            
            canvas.draw() 
            
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)
            
            # creating the Matplotlib toolbar s
            toolbar = NavigationToolbar2Tk(canvas,self.root)
            toolbar.update() 
            self.toolbars.append(toolbar)
            
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack(side=RIGHT, expand=False)

            return
      
            



            
root=Tk()
root.attributes("-zoomed", True)

ob=Student(root)
root.mainloop()
