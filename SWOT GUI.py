#####################################
###  UCLA Geography               ###
###  2015 Summer C  Geog 199      ###
###  Beta Version:                ###
###                 Colin Gleason ###
###                 Yuxi Suo      ###
#####################################

#Create the Window, remember to capital T in py2, but t in py3 (open the fuction)

### import all librarys                           ###

from Tkinter import *
import csv
import tkFileDialog
import tkFont
import tkMessageBox
import math
import os
from math import *
import numpy
from tkFileDialog import askopenfilename
from itertools import izip
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

##########--------------------------            Input                -------------------------------###########
class Window:

    def __init__(self, master):


        #Total  11 buttons
            ##   Input Part###
            #(I) 3 Browse Buttons
        '''When you click on Browse W/Browse H/Browse Q individually,
        it will pop the file picking window, and the only available file type is CVS file and excel file(xlsx)'''
        
            #1. Width File Button
        self.wbutton= Button(root, text="Browse Width      ", command=self.browsecsv1)
        self.wbutton.grid(row=2, column=0,sticky=W)

            #2. Height File Button
        self.hbutton= Button(root, text="Browse Height     ", command=self.browsecsv2)
        self.hbutton.grid(row=10, column=0,sticky=W)
        

            #3. Discharge File Button
        self.qbutton= Button(root, text="Browse Discharge", command=self.browsecsv3)
        self.qbutton.grid(row=20, column=0,sticky=W)
        
            #(II)5 Execute Buttons
        
            #4. User input already reached averaged data, only need to be proceed to algorithm
        self.pbutton= Button(root, text="Proceed to Algorithm", command=self.ProceedToAlgorithm,  fg= "white", bg= "cyan")
        self.pbutton.grid(row=28, column=1,sticky = W)
        self.pbutton.configure(state='disabled')

            #5.Reach-Average Button, GUI will take raw data and reach average it for algorithm
        self.cbutton= Button(root, text="Reach Average then proceed to Algorithm", command=self.process_csv,  fg= "white", bg= "orange")
        self.cbutton.grid(row=34, column=1, sticky = W)

            ##   Output Part###
            #6.Hydrograph Button, a timeseries plot
        self.button1 = Button(root, text= "1)Save as Hydrograph", command=self.hydrograph,fg= "white", bg="brown")
        self.button1.grid(row=36, column=0, sticky=W)

            #7.Plot button, GUI will pop the figure that can be saved as PNG file
        self.button2 = Button(root, text= "Plot", command=self.plot, fg= "white", bg="purple")
        self.button2.grid(row=43, column=1, sticky=W)
        
            #8.Analyze button, a matrix will pop out that has detailed statistic of four algorithms comparison
        self.button3 = Button(root, text= "Analyze",command=self.matrix, fg= "white", bg="sea green")
        self.button3.grid(row=43, column=2, sticky=W)
        self.button3.configure(state="disabled")
        
            #(III)one Sub Button

            #When the Cross-Section checkbutton is checked, the A Propri buttons is clickable
            #9. A Propri 
        self.subabutton= Button(root, text="Input User Defined Data", command=self.browsecsv4,justify=CENTER)
        self.subabutton.grid(row=30, column=2,sticky = W)
        self.subabutton.configure(state='disabled')


            ######   Total 7 Textbox, which is the blank text box in GUI ##################

            #Variable that in the textboxes
        self.path1 = StringVar()
        self.path2 = StringVar()
        self.path3 = StringVar()
        self.path4 = StringVar()
        self.path5 = IntVar()
        self.path6 = DoubleVar()
        self.path7 = StringVar()

        
            #1. Width File Pathname 
        self.barw=Entry(root, textvariable=self.path1).grid(row=2, column=1,sticky=W)
        
            #2. Height File Pathname 
        self.barh=Entry(root, textvariable=self.path2).grid(row=10, column=1,sticky=W)
        
            #3. Discharge File Pathname
        self.barq=Entry(root, textvariable=self.path3).grid(row=20, column=1,sticky=W)
        
            #4. Input User Defined File Pathname 
        self.bara=Entry(master, textvariable=self.path4).grid(row=30, column=1,sticky=W)
        
            #5. Reaches Number Return 
        self.barn=Entry(root, textvariable=self.path5).grid(row=31, column=1,sticky=W)

            #6. Desired distance Return
        self.barn=Entry(root, textvariable=self.path6).grid(row=32, column=1,sticky=W)
        
            #7. Reach-averaged data folder pathname
        self.barf=Entry(root, textvariable=self.path7).grid(row=33, column=1,sticky=W)
 # C:\Users\Yuxi\Desktop\data


        ##########        Total 7  Checkboxes, 2 Radiobutton         ###########
        #Radiobutton sns, stands for station=1 and nonstation=2
        self.sns = IntVar()
        self.checkS=Radiobutton(master, text="Station", variable=self.sns, value=1,command=self.stationcheck).grid(row=26, column=0, sticky=W)
        self.checkNS=Radiobutton(master, text="Non-station", variable=self.sns, value=2,command=self.stationcheck).grid(row=27, column=0, sticky=W)

        #Radiobutton sb, clickable only if cross-section is checked, 
        self.sb = IntVar()
        #A Propri=1
        self.subcheck1 = Radiobutton(master, text="A Priori", variable=self.sb, value=1,command = self.A_priori_oncheck)
        self.subcheck1.grid(row=30, column=0, sticky=W)
        self.subcheck1.configure(state='disabled')
        #Number =2
        self.subcheck2 = Radiobutton(master, text="Number", variable=self.sb, value=2)
        self.subcheck2.grid(row=31, column=0, sticky=W)
        self.subcheck2.configure(state='disabled')
        #Distance=3
        self.subcheck3 = Radiobutton(master, text="Distance", variable=self.sb,value=3)
        self.subcheck3.grid(row=32, column=0, sticky=W)
        self.subcheck3.configure(state='disabled')

        
        #cross-section checkbox, it is checkable if only sns has value 
        self.cb3 = IntVar()
        self.checkCS = Checkbutton(master, text="Cross-section", variable=self.cb3, command=self.naccheck)
        self.checkCS.grid(row=29, column=0,sticky=W)
        self.checkCS.configure(state='disabled')

        #Already Reach-averaged checkbox, it is checkable if only sns has value 
        self.cb4 = IntVar()
        self.checkRA = Checkbutton(master, text="Already Reach-averaged", variable=self.cb4,command = self.ARA_oncheck)
        self.checkRA.grid(row=28, column=0,sticky=W)
        self.checkRA.configure(state='disabled')



        ############         5 in Output frame, Algorithm checkboxes       #############
        chooseAlgo_label = Label(root, text="2).Choose Algorithms")
        chooseAlgo_label.grid(row=37, column=0, sticky=W)
        
        self.algo1 = IntVar()
        self.a1 = Checkbutton(root, text="AMHG Discharge Algorithm", variable=self.algo1, command = self.AMHG)
        self.a1.grid(row=38, column=0, sticky=W)


        self.algo2 = IntVar()
        self.a2 = Checkbutton(master, text="Garambois-Munier Discharge Algorithm", variable=self.algo2, command = self.GaramboisMunier)
        self.a2.grid(row=39, column=0, sticky=W)

        self.algo3 = IntVar()
        self.a3 = Checkbutton(master, text="MetroMan Discharge Algorithm ", variable=self.algo3,command = self.MetroMan)
        self.a3.grid(row=40, column=0, sticky=W)

        self.algo4 = IntVar()
        self.a4 = Checkbutton(master, text="Bjerklie Discharge Algorithm", variable=self.algo4, command = self.Bjerklie)
        self.a4.grid(row=41, column=0, sticky=W)

        self.algo5 = IntVar()
        self.a5 = Checkbutton(master, text="Synergistic Algorithm", variable=self.algo5, command = self.Synergistic)
        self.a5.grid(row=42, column=0, sticky=W)


        #Total 6 Labels
        titlelabel= Label(root, text="SWOT Discharge Algorithms Tool",
                          bg="blue", fg="white")
        titlelabel.grid(row=0, column=1, sticky=W)

        input_label = Label(root, text="Input")
        input_label.grid(row=1, column=0, sticky=W)
        
        data_label = Label(root, text="Data Type")
        data_label.grid(row=25, column=0, sticky=W)
        
        output_label = Label(root, text="Output")
        output_label.grid(row=35, column=0, sticky=W)
        
        beta_label = Label(root, text="Beta Version:Yuxi Suo, Colin Gleason. UCLA Geography")
        beta_label.grid(row=100, column=1, sticky=W)

        outputfolder_label = Label(root, text="Insert the path to save the data ")
        outputfolder_label.grid(row=33, column=0, sticky=W)

 
        
####Browsecsv_Input____________Total 4, user input data___________________________________________________________________
    #browse file in CSV or Excel format
    #1. Width Data                                     
    def browsecsv1(self):
        Tk().withdraw() 
        self.filename_w = askopenfilename(filetypes = (("CSV Files", "*.csv"),("Excel File","*.xlsx"),))  
        self.path1.set(str(self.filename_w))
        print(self.filename_w)

    #2. Height Data
    def browsecsv2(self):
        Tk().withdraw() 
        self.filename_h = askopenfilename(filetypes = (("CSV Files", "*.csv"),("Excel File","*.xlsx"),))
        self.path2.set(str(self.filename_h))
        print(self.filename_h)

    #3. Discharge Data   
    def browsecsv3(self):
        Tk().withdraw() 
        self.filename_q = askopenfilename(filetypes = (("CSV Files", "*.csv"),("Excel File","*.xlsx"),))
        self.path3.set(str(self.filename_q))
        print(self.filename_q)
        #The Q data control the Analyze, which is the matrix function in the output section
        if len(str(self.filename_q)) > 0: #data provided
            self.button3.configure(state="normal")#normalize the button
        elif len(str(self.filename_q)) <= 0:#no data provided
            self.button3.configure(state="disabled")#disabel the button
        
    #4. User Input Data
    def browsecsv4(self):
        Tk().withdraw() 
        self.filename_a = askopenfilename(filetypes = (("CSV Files", "*.csv"),("Excel File","*.xlsx"),))
        self.path4.set(str(self.filename_a))
        print(self.filename_a)

        if len(str(self.filename_a)) > 0:
            self.subabutton.configure(state="normal")
        elif len(str(self.filename_a)) <= 0:
            self.subabutton.configure(state="disabled")

#5 functions for checkbox, on check and disable check____________________________________
    #1
    def stationcheck(self):
        #this block grays out the Already Reach-averaged(RA) checkbox and the Cross-section(CS) checkbox
        if self.sns.get() >0:
            self.checkRA.configure(state='normal')
            self.checkCS.configure(state='normal')
        else:
            self.checkRA.configure(state='disabled')
            self.checkCS.configure(state='disabled')
        
    #3
    def ARA_oncheck(self):
        #this is the Already Reach-averaged checkbox, which when enabled
        #grays out everything in the Input section except the Proceed to Algorithm(pbutton)
        if self.cb4.get() == 1:
            self.checkCS.configure(state='disabled')
            self.pbutton.configure(state='normal')
            self.cbutton.configure(state='disabled')
        else:
            self.checkCS.configure(state='normal')
            self.pbutton.configure(state='disabled')
            self.cbutton.configure(state='normal')
    #4       
    def A_priori_oncheck(self):
        #If A_priori checkbox been checked, the button of browsing user defined data will be activate
        if self.sb.get() == 1:
            self.subabutton.configure(state='normal')
        else:
            self.subabutton.configure(state='disabled')
     
    #5
    def naccheck(self):
        if self.cb3.get() == 1:#this is the cross-section checkbox, the 3 radiobuttons will be activated
            self.subcheck1.configure(state='normal')
            self.subcheck2.configure(state='normal')
            self.subcheck3.configure(state='normal')
            self.subabutton.configure(state='disabled')
            self.checkRA.configure(state='disabled')#the Already Reach_averaged checkbox is gray-out
        else:
            self.subcheck1.configure(state='disabled')
            self.subcheck2.configure(state='disabled')
            self.subcheck3.configure(state='disabled')
            self.subabutton.configure(state='disabled')  
            self.checkRA.configure(state='normal')

###########       Reach-averaging     #############

    #If the data is already been reach-averaged, user can hit the button Proceed to Algorithm
        #and the data will be passed to the Algorithm with some specified name
    def ProceedToAlgorithm(self):
        print('Proceed To Algorithm')
    def process_csv(self):
        #make a new folder to store reach-averaged data
        if not os.path.exists(self.path7.get()+'\Reach_Averaged_Data'): os.makedirs(self.path7.get()+'\Reach_Averaged_Data')

        #If the NumberOfReaches checkbox is checked--------------------------------------------------------
        if self.sb.get() == 2:
            #CSV_W_____________________________________________________________
            if len(str(self.path1.get())) > 0:
                W_filename = open(self.filename_w)
                W_data = numpy.genfromtxt(W_filename,delimiter=",")
                W_size=W_data.shape
                numrows=W_size[0]
                numcols=W_size[1]

                if self.sns.get() ==1:#if station is checked
                    if self.path5.get() <=20:
                        print ('you want', self.path5.get(), ' reaches')
                    else :
                        self.msgbox_numberswarning = tkMessageBox.showinfo("Warning",
                        "number of desired reaches leads to reach-averaging 20 or less cross sections. Please choose a lower number of desired reaches.")
                        #set the userinput and pass it to reach_average function     
                        self.desired_reaches=self.path5.get()
                    
                    reach_averaged_W=numpy.zeros((self.path5.get(),numcols-1))
                    reach_length= numpy.rint(numrows/self.path5.get())
                    W_data_nostation=W_data[:,1:numcols]
            #this removes the station column from the data by keeping all the rows [:, and all the columns but the first ,1:numcols]
                    counter=0
                    for i in range(0,int(numrows-reach_length-1),int(reach_length)):
                #numrows-reach_length says we are going to stop before the end of the data
                #numrows - reach_length -1 accounts for the difference in 0 based indexing and the length function
                #the ,reach_length defines the step of each loop
                #we need to convert them to integers so the for loop can run
        
                        current_reach=W_data_nostation[i:i+reach_length,:]#this takes rows i to i + reach length and all columns
                # for the first iteration, this would be rows 0 through the end of the first reach, or row 15 becuase we have
                # 15 reaches

                #at this point, we have just the data we want, and we need to reach average it
                        averaged_reach=numpy.mean(current_reach,0) #this is perhaps simpler to understand than my other version, which
                #combined this step and last step in the averaging

                        reach_averaged_W[counter,:]=averaged_reach
                #place the averaged reach into the output
                #normally, I would reset averaged_reach, but since it is always the same size, its ok
                        counter=counter+1
                    print "reach_averaged_W1"
                    print reach_averaged_W
                    numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_W.csv',reach_averaged_W, fmt='%.18f',delimiter=',')

                if self.sns.get() ==2:#if nonstation is checked
                    
                    reach_averaged_W=numpy.zeros((self.path5.get(),numcols))
            #makes us a space to put the output data that has the right
            #number of rows and columns, again with the -1 offest for 0 based indexing
                    reach_length= numpy.rint(numrows/self.path5.get())
            # the rint function rounds to the nearest integer. This yields the number of rows per reach
                #W_data_nostation=W_data[:,1:numcols]
            #this removes the station column from the data by keeping all the rows [:, and all the columns but the first ,1:numcols]
                    counter=0

                    for i in range(0,int(numrows-reach_length-1),int(reach_length)):
                #numrows-reach_length says we are going to stop before the end of the data
                #numrows - reach_length -1 accounts for the difference in 0 based indexing and the length function
                #the ,reach_length defines the step of each loop
                #we need to convert them to integers so the for loop can run
        
                        current_reach=W_data[i:i+reach_length,:]#this takes rows i to i + reach length and all columns
                # for the first iteration, this would be rows 0 through the end of the first reach, or row 15 becuase we have
                # 15 reaches

                #at this point, we have just the data we want, and we need to reach average it
                        averaged_reach=numpy.mean(current_reach,0) #this is perhaps simpler to understand than my other version, which
                #combined this step and last step in the averaging

                        reach_averaged_W[counter,:]=averaged_reach
                #place the averaged reach into the output
                #normally, I would reset averaged_reach, but since it is always the same size, its ok
                        counter=counter+1
                    print "reach_averaged_W1"
                    print reach_averaged_W
                #save the data to the new folder
                    numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_W.csv',reach_averaged_W, fmt='%.18f',delimiter=',')


            #CSV_H_________________________________________________________________
            if len(str(self.path2.get())) > 0:
                H_filename = open(self.filename_h)
                H_data = numpy.genfromtxt(H_filename,delimiter=",") 
                H_size=H_data.shape
                numrows=H_size[0]
                numcols=H_size[1]
                if self.path5.get() <=20:
                    print ('you want', self.path5.get(), ' reaches')
                else :
                    self.msgbox_numberswarning = tkMessageBox.showinfo("Warning",
                    "number of desired reaches leads to reach-averaging 20 or less cross sections. Please choose a lower number of desired reaches.")
                       
                    self.desired_reaches=self.path5.get()
                
               
                if self.sns.get() ==1:    
                    reach_averaged_H=numpy.zeros((self.path5.get(),numcols-1))
           
                    reach_length= numpy.rint(numrows/self.path5.get())
           
                    H_data_nostation=H_data[:,1:numcols]
            
                    counter=0
                    for i in range(0,int(numrows-reach_length-1),int(reach_length)):
               
        
                        current_reach=H_data_nostation[i:i+reach_length,:]
                        averaged_reach=numpy.mean(current_reach,0) 
                        reach_averaged_H[counter,:]=averaged_reach
              
                        counter=counter+1
                    print "reach_averaged_H1"
                    print reach_averaged_H
                    numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_H.csv',reach_averaged_H, fmt='%.18f',delimiter=',')

                if self.sns.get() ==2:
                    reach_averaged_H=numpy.zeros((self.path5.get(),numcols))
                    reach_length= numpy.rint(numrows/self.path5.get())
                    counter=0
                    for i in range(0,int(numrows-reach_length-1),int(reach_length)):
                        current_reach=H_data[i:i+reach_length,:]
                        averaged_reach=numpy.mean(current_reach,0) 
                        reach_averaged_H[counter,:]=averaged_reach
               
                        counter=counter+1
                    print "reach_averaged_H1"
                    print reach_averaged_H
                    numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_H.csv',reach_averaged_H, fmt='%.18f',delimiter=',')

        #CSV_Q___________________________________________________________________

            elif len(str(self.path3.get())) > 0:   
                Q_filename = open(self.filename_q)
                Q_data = numpy.genfromtxt(Q_filename,delimiter=",") 
                Q_size=Q_data.shape
                numrows=Q_size[0]
                numcols=Q_size[1]
                
                if self.path5.get() <=20:
                    print ('you want', self.path5.get(), ' reaches')
                else :
                    self.msgbox_numberswarning = tkMessageBox.showinfo("Warning",
                    "number of desired reaches leads to reach-averaging 20 or less cross sections. Please choose a lower number of desired reaches.")
                    
                    self.desired_reaches=self.path5.get()
 
                if self.sns.get() ==1:
                    reach_averaged_Q=numpy.zeros((self.path5.get(),numcols-1))
    
                    reach_length= numpy.rint(numrows/self.path5.get())
                    Q_data_nostation=Q_data[:,1:numcols]
                    counter=0

                    for i in range(0,int(numrows-reach_length-1),int(reach_length)):

        
                        current_reach=Q_data_nostation[i:i+reach_length,:]
                        averaged_reach=numpy.mean(current_reach,0)

                        reach_averaged_Q[counter,:]=averaged_reach

                        counter=counter+1
                    print "reach_averaged_Q1"
                    print reach_averaged_Q

                    numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_Q.csv',reach_averaged_Q, fmt='%.18f',delimiter=',')
                    
                if self.sns.get() ==2:
                    reach_averaged_Q=numpy.zeros((self.path5.get(),numcols))
                    reach_length= numpy.rint(numrows/self.path5.get())
                    counter=0

                    for i in range(0,int(numrows-reach_length-1),int(reach_length)):
        
                        current_reach=Q_data[i:i+reach_length,:]
                        averaged_reach=numpy.mean(current_reach,0)
                        reach_averaged_Q[counter,:]=averaged_reach

                        counter=counter+1
                    print "reach_averaged_Q1"
                    print reach_averaged_Q

                    numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_Q.csv',reach_averaged_Q, fmt='%.18f',delimiter=',')
            msgbox_CSVsavingwarning = tkMessageBox.showinfo("Warning","Reach-Averaged data saved to the GUI folder.")




        #If the Distance checkbox is checked--------------------------------------------------------
        #Station_Distance______________________________________________________________________
        elif self.sb.get() == 3:
            #CSV_W_________________________________________________________
            if len(str(self.path1.get())) > 0:
                W_filename = open(self.filename_w) #set filename
                W_data = numpy.genfromtxt(W_filename,delimiter=",") #open the data
                W_size=W_data.shape#get the size of the array as [m,n]
                numrows=W_size[0]# m = number of rows
                numcols=W_size[1]# n = number of columns

##            #get the max of the station number
                Max_W_station=max(W_data[:,0])        
                if self.path6.get()> Max_W_station:
                    msgbox_Distancewarning = tkMessageBox.showinfo("Warning","Your distance is longer than the longest one in your data, please enter again.")

                else:

                    station_vector=W_data[:,0]# get just the station numbers
                    
                    first_station=station_vector[0]
     
                    next_station=first_station - self.path6.get()#how far away is the next station? This gives the station number
        #we want
                    distance_vector=station_vector-next_station#by minimizing the distance on this array, we get the index of the
        #station we want


                    reach_end_index=numpy.argmin(numpy.absolute(distance_vector))#Return the indices of the minimum values along an axis. This tells us where the distance
        #vector is at a minimum. if a station were exactly desired_distance away from the first station, then
        #distvect would equal 0. we are looking for the closest station to this 0 distance
                    reach_index=[0,reach_end_index]
                    while True: #this sets up an infitie loop to be broken later
                        next_station=station_vector[reach_end_index]-self.path6.get()#how far away is the next station? This gives the station number
            #we want
                        distance_vector=station_vector-next_station
                        reach_end_index=numpy.argmin(numpy.absolute(distance_vector))
                        reach_index.append(reach_end_index)#normally, i always make an empty array first, rather than grow one like
            #this, but beacuse we dont know how long it will be, it makes sense to append here
                        check_value= station_vector[reach_end_index]-self.path6.get() #will the next station be beyond the range of the data?
        
                        if check_value < station_vector[numpy.argmin(station_vector)]: #if the next station would be less than the minimum station value
                #break the loop
                            break
                    print "reach_index"    
                    print reach_index
                    flag=0;
                    for i in range(0 , len(reach_index)-2):
                        numrows_between= numpy.absolute(reach_index[i]-reach_index[i+1])
                        if numrows_between <=5:
                            flag= flag+1;

                    if flag >=1:
                        msgbox_reach_indexwarning = tkMessageBox.showinfo("Warning","There are several reaches built from averaging 5 or less cross sections")
                    
                     

        #now, lets do another reach averaging
                    counter=0
                    reach_averaged_W=numpy.zeros((len(reach_index)-1,numcols-1))
                    W_data_nostation=W_data[:,1:numcols]
        
                    for i in range(0,len(reach_index)-1):
                        current_reach=W_data_nostation[reach_index[i]:reach_index[i+1],:]
                        averaged_reach=numpy.mean(current_reach,0) 
                        reach_averaged_W[counter,:]=averaged_reach 
                        counter=counter+1
                    print "reach_averaged_W2"
                    print reach_averaged_W
                    numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_W.csv',reach_averaged_W, fmt='%.18f',delimiter=',')
            #CSV_H_________________________________________________________
            if len(str(self.path2.get())) > 0:
                H_filename = open(self.filename_h) 
                H_data = numpy.genfromtxt(H_filename,delimiter=",") 
                H_size=H_data.shape
                numrows=H_size[0]
                numcols=H_size[1]

                Max_H_station=max(H_data[:,0])            
                if self.path6.get()> Max_H_station:
                    msgbox_Distancewarning = tkMessageBox.showinfo("Warning","Your distance is longer than the longest one in your data, please enter again.")

                else:

                    station_vector=H_data[:,0]
                    first_station=station_vector[0]
     
                    next_station=first_station - self.path6.get()
                    distance_vector=station_vector-next_station


                    reach_end_index=numpy.argmin(numpy.absolute(distance_vector))
                    reach_index=[0,reach_end_index]
                    while True: 
                        next_station=station_vector[reach_end_index]-self.path6.get()
                        distance_vector=station_vector-next_station
                        reach_end_index=numpy.argmin(numpy.absolute(distance_vector))
                        reach_index.append(reach_end_index)
                        check_value= station_vector[reach_end_index]-self.path6.get() 
        
                        if check_value < station_vector[numpy.argmin(station_vector)]: 
                            break
                    print "reach_index"    
                    print reach_index

                    counter=0
                    reach_averaged_H=numpy.zeros((len(reach_index)-1,numcols-1))
                    H_data_nostation=H_data[:,1:numcols]
        
                    for i in range(0,len(reach_index)-1):
                        current_reach=H_data_nostation[reach_index[i]:reach_index[i+1],:]
                        averaged_reach=numpy.mean(current_reach,0) 
                        reach_averaged_H[counter,:]=averaged_reach 
                        counter=counter+1
                    print "reach_averaged_H2"
                    print reach_averaged_H
                    numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_H.csv',reach_averaged_H, fmt='%.18f',delimiter=',')

            
            #CSV_Q______________________________________________________________________
            if len(str(self.path3.get())) > 0:
                Q_filename = open(self.filename_q)
                Q_data = numpy.genfromtxt(Q_filename,delimiter=",")
                Q_size=Q_data.shape
                numrows=Q_size[0]
                numcols=Q_size[1]
        
                Max_Q_station=max(Q_data[:,0])#get the max of the station number
                
                if self.path6.get()> Max_Q_station:
                    msgbox_Distancewarning = tkMessageBox.showinfo("Warning","Your distance is longer than the longest one in your data, please enter again.")

                else:

                    station_vector=Q_data[:,0]
                    first_station=station_vector[0]
     
                    next_station=first_station - self.path6.get()
                    distance_vector=station_vector-next_station

                    reach_end_index=numpy.argmin(numpy.absolute(distance_vector))
                    reach_index=[0,reach_end_index]
                    while True: 
                        next_station=station_vector[reach_end_index]-self.path6.get()
                        distance_vector=station_vector-next_station
                        reach_end_index=numpy.argmin(numpy.absolute(distance_vector))
                        reach_index.append(reach_end_index)
                        check_value= station_vector[reach_end_index]-self.path6.get()
        
                        if check_value < station_vector[numpy.argmin(station_vector)]: 
                #break the loop
                            break
                    print reach_index

                    counter=0
                    reach_averaged_Q=numpy.zeros((len(reach_index)-1,numcols-1))
                    Q_data_nostation=Q_data[:,1:numcols]
        
                    for i in range(0,len(reach_index)-1):
                        current_reach=Q_data_nostation[reach_index[i]:reach_index[i+1],:]
                        averaged_reach=numpy.mean(current_reach,0) 
                        reach_averaged_Q[counter,:]=averaged_reach 
                        counter=counter+1
                    print "reach_averaged_Q2"
                    print reach_averaged_Q
                    numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_Q.csv',reach_averaged_Q, fmt='%.18f',delimiter=',')
                msgbox_CSVsavingwarning = tkMessageBox.showinfo("Warning","Reach-Averaged data saved to the GUI folder.")



                #If the A Priori checkbox is checked--------------------------------------------------------
            elif self.sb.get() == 1:
                A_filename = open(self.filename_a)
                A_data = numpy.genfromtxt(A_filename,delimiter=",") 
                A_size=A_data.shape
                numrows=A_size[0]
                numcols=A_size[1]
                counter=0
                reach_averaged_A=numpy.zeros((len(reach_index)-1,numcols-1))
                A_data_nostation=A_data[:,1:numcols]
        
                for i in range(0,len(reach_index)-1):
                    current_reach=A_data_nostation[reach_index[i]:reach_index[i+1],:]
                    averaged_reach=numpy.mean(current_reach,0) 
                    reach_averaged_A[counter,:]=averaged_reach 
                    counter=counter+1
                print "reach_averaged_A2"
                print reach_averaged_A
                numpy.savetxt(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_A.csv',reach_averaged_A, fmt='%.18f',delimiter=',')
                
                msgbox_CSVsavingwarning = tkMessageBox.showinfo("Warning","Reach-Averaged data saved to the GUI folder.")
 
##########--------------------------            Output                -------------------------------###########

    def hydrograph(self):
        #make a new folder to store reach-averaged data
        if not os.path.exists(self.path7.get()+'\Hydrograph_Data'): os.makedirs(self.path7.get()+'\Hydrograph_Data')
               
    ####CSV_W-----------------------------------
        
        if len(str(self.path1.get())) > 0:#If user input W data
            read_W = open(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_W.csv')#open the reach_averaged_data
            csv_read_W = csv.reader(read_W)#read the data
            row1 = csv_read_W.next()#read row by row
            column_count = len(row1)#count the number of columns
            average_list = []       #create a list for hydrograph data
            for x in range(0, column_count):
                average_list.append(float(row1[x]))
            row_count=1             #append the first row
            for row in csv_read_W:
                for x in range(0,column_count):
                    average_list[x]+=float(row[x])
                row_count += 1      #until the last row 
            for n in range(0,column_count):
                average_list[n]=average_list[n]/row_count #average
                #save the list as a new csv in the Hydrograph_data folder
                numpy.savetxt(self.path7.get()+'\Hydrograph_Data\Hydrograph_W.csv',average_list, fmt='%.18f',delimiter=',')


####CSV_H
        if len(str(self.path2.get())) > 0:
            read_H = open(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_H.csv')
            csv_read_H = csv.reader(read_H)
            row1 = csv_read_H.next()
            column_count = len(row1)
            
            average_list = []
            for x in range(0, column_count):
                average_list.append(float(row1[x]))
            row_count=1
            for row in csv_read_H:
                for x in range(0,column_count):
                    average_list[x]+=float(row[x])
                row_count += 1
            for n in range(0,column_count):
                average_list[n]=average_list[n]/row_count
            numpy.savetxt(self.path7.get()+'\Hydrograph_Data\Hydrograph_H.csv',average_list, fmt='%.18f',delimiter=',')

####CSV_Q
        if len(str(self.path3.get())) > 0:
            read_Q = open(self.path7.get()+'\\Reach_Averaged_Data\\Reach_Averaged_Q.csv')
            csv_read_Q = csv.reader(read_Q)
            row1 = csv_read_Q.next()
            column_count = len(row1)

            average_list = []
            for x in range(0, column_count):
                average_list.append(float(row1[x]))

            row_count=1
            for row in csv_read_Q:
                for x in range(0,column_count):
                    average_list[x]+=float(row[x])
                row_count += 1
            for n in range(0,column_count):
                average_list[n]=average_list[n]/row_count
                
            numpy.savetxt(self.path7.get()+'\Hydrograph_Data\Hydrograph_Q.csv',average_list, fmt='%.18f',delimiter=',')    
            print "Done with Hydrpgraph"


##########            Algorithm             ###########
#5 Algorithm that need to be translated
    def AMHG(self):
        if self.algo1.get() == 1:
            print "amhg"
        else:
            print "hah"
    def GaramboisMunier(self):
        if self.algo2.get() == 1:
            print "GM"
        else:
            print "hah"
    def MetroMan(self):
        if self.algo3.get() == 1:
            print "MM"
        else:
            print "hah"
    def Bjerklie(self):
        if self.algo4.get() == 1:
            print "bj"
        else:
            print "hah"
    def Synergistic(self):
        if self.algo5.get() == 1:
            print "s"
        else:
            print "hah"
#plot the data, and save as a PNG
    def plot(self):
        days, impressions = numpy.loadtxt("page-impressions.csv", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y-%m-%d')})
        plt.plot_date(x=days, y=impressions,fmt="r-")
        plt.title("Hydrograph Dischage")
        plt.ylabel("Discharge")
        plt.grid(True)
        plt.show()
#compare different matrix
    def matrix(self):
        numpy.zeros((5, 5))
        msgbox_CSVsavingwarning = tkMessageBox.showinfo("Warning","The fuction 'Analyze' algorithm can only be exceute if only the Discharge data is provided, make sure you provided discahrge data!")
        

    

root = Tk()
root.title("SWOT GUI")
root.geometry("800x650")
window=Window(root)
root.mainloop()
