# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:13:43 2018

@author: wschnupp
"""

import pandas as pd
import glob, os
# import time
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import configparser

class dataHandler:

    def __init__(self, fileName=''):
        self.root = tk.Tk()
        self.root.withdraw()

        self.dataframe=None
        self.rowsSaved=0
        self.autosaveEveryN=5
        self.filename=fileName
        self.onlineFeedback=False # set to true if you want output ont eh console on every trial that gets saved

    
    def statusChange(self,newStatus):
        if newStatus=="start":
            self.createDatafile()
            return
        if newStatus=="chooseNextTrial":
            return
        if newStatus=="waitForStart":
            return
        if newStatus=="presentTrial":
            return
        if newStatus=="getResponse":
            return
        if newStatus=="reward":
            return
        if newStatus=="punish":
            return
        else:
            print("datahandling module received unrecognized status: "+newStatus)
            return

    def createDatafile(self, fname=None, configFile='Behavior.ini', keyword=None):
        if self.filename!='':
            # we already have a data file name
            return
        if fname is None:
            # build a filename using config info
            if keyword is None:
                raise Exception('need keyword to auto create filename')
            config = configparser.ConfigParser()
            if config.read(configFile) ==[]:
                config['DEFAULT'] = {'dataDir': ''}
            dataDir=config['DEFAULT']['dataDir']
            if not os.path.exists(dataDir):
                dataDir=''
            dataDir=filedialog.askdirectory(title="Where to save the data?", initialdir=dataDir)
            config['DEFAULT']['dataDir']=dataDir
            timeStr=datetime.now().strftime('%Y-%m-%d')
            participantID=input('Enter the ID of the experimental subject: ')
            participantID.replace(" ","")
            participantID.replace("\\","")
            participantID.replace("/","")
            session=1
            fileName=f"{dataDir}/{keyword}_{participantID}_{timeStr}_{session}.csv"
            while os.path.exists(fileName):
                session+=1
                fileName=f"{dataDir}/{keyword}_{participantID}_{timeStr}_{session}.csv"                
            print(f'Saving data to {fileName}')
            self.filename = fileName
            with open(configFile, 'w') as configfilehandle:
                config.write(configfilehandle)    
        else:
            self.filename = fname
        if not self.filename[-1]=='v':
            self.filename=self.filename+'.csv'        
        
    
    def saveTrial(self, trialParameters):
        # build a dict that combines all the info of the last trial and add it to a pandas dataframe
        
        if self.dataframe is None:
            self.dataframe=pd.DataFrame(trialParameters, index=[0])
        else:
            # self.dataframe=self.dataframe.append(trialParameters,ignore_index=True)
            self.dataframe=pd.concat([self.dataframe, pd.DataFrame([trialParameters])],ignore_index=True)
            
        if len(self.dataframe)-self.rowsSaved>self.autosaveEveryN:
            self.dumpToFile()
            
        if self.onlineFeedback:
            if 'correct' in self.dataframe.columns:
                Ncorrect=self.dataframe['correct'].sum()
                Ntotal=len(self.dataframe)
                print('*** Current performance: {} out of {} correct ({:.1f}%)'.format(Ncorrect, Ntotal,Ncorrect*100/Ntotal))

            
    def dumpToFile(self):
        if self.dataframe is None:
            return
        if self.filename=='':
            self.createDatafile()
        try:
            self.dataframe.to_csv(self.filename)
            self.rowsSaved=len(self.dataframe)
        except:
            messagebox.showwarning('Could not save data!','Choose a different data file.')
            self.createDatafile()
            self.dumpToFile()
            
    def done(self):
        self.dumpToFile()  
        self.root.quit()
    


