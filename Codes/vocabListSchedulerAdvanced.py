#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  14th 2025

@author: jan


Scheduler for spaced repetition vocab training.

Steps: 
    1) Check sessions log to find out whether participant has been tested before.
    2) Register start weight for participant
    3) find out whether, for a given participants, there are items to review.
       If this is a new participant, the answer is no. 
    XX) register end weight for participant. Save to sessions log. 
       Give feedback on weights

"""

import numpy as np
import pandas as pd
import time
import psyPhysConfig as config
if not hasattr(config,'maxResponseTime'):
    config.maxResponseTime=15 # max interval between start spout lick and response in seconds
from sys import path as syspath
# syspath.append(config.clSource+'/ratCageProgramsV3')
sourcePath=config.clSource+'/RatVocabTrainer'
syspath.append(sourcePath)

import configparser

cPars = configparser.ConfigParser()
if cPars.read(sourcePath+'/SpacedRepetition.ini') ==[]:
    cPars['DEFAULT'] = {'dataDir': ''}
dataDir=cPars['DEFAULT']['dataDir']




import listScheduler2 as sc
import PicsWithSounds as sl
successStim=sl.pictureAndSoundStimulus(ID='Success')
successStim.ready()
failStim=sl.pictureAndSoundStimulus(ID='Fail')
failStim.ready()

""" 
adapt listScheduler to the fact that there is no start spout but there are three choice spouts:
    - waitForStart does not wait for detector
    - 
"""
class vocabScheduler(sc.scheduler):
    
    def waitForStart(self):
        # successStim.hide()
        # listen to detectors and wait for a START signal
        self.broadCastStatus('waitForStart')
        # check if a minimum ISI is required and if it has elapsed
        if hasattr(self,'minimumISI'):
            timeElapsedSinceLastStart=time.time()-self.lastStart
            if timeElapsedSinceLastStart < self.minimumISI:
                self.dblog('Pausing for {:3.5} s for minimum ISI to elapse.'.format(self.minimumISI-timeElapsedSinceLastStart))
                time.sleep(self.minimumISI-timeElapsedSinceLastStart)
        failStim.hide()
        return self.presentTrial
    
    def handleCenterReward(self):
        pass # no center rewards for starting
        
    def punish(self):
        failStim.hide()
        failStim.show()
        failStim.play()
        self.dblog('Wrong response. Starting timeout then repeating trial')
        self.broadCastStatus('punish')
        time.sleep(0.5)
        return self.waitForStart # we will present same again, correction trial
        
    def reward(self):
        failStim.hide()
        successStim.show()
        successStim.play()
        self.dblog('Correct response. Giving reward then choosing next trial')
        self.broadCastStatus('reward')
        time.sleep(1)
        return self.chooseNextTrial
        
        
                
#%% 
if __name__ == '__main__':
    
