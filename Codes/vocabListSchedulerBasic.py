#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 14:56:52 2025

@author: jan
"""

import numpy as np
import time
import psyPhysConfig as config
if not hasattr(config,'maxResponseTime'):
    config.maxResponseTime=15 # max interval between start spout lick and response in seconds
# import os
# clSource = '/home/colliculus/behaviourBoxes/software'
# if not os.path.exists(clSource+'/ratCageProgramsV3/ClickTrainLibrary.py'):
#     clSource = '/home/pi'  # <-- qingjie: change this path to what works on the RPi
# if not os.path.exists(clSource+'/ratCageProgramsV3/ClickTrainLibrary.py'):
#     clSource = 'c:/users/colliculus'
# if not os.path.exists(clSource+'/ratCageProgramsV3/ClickTrainLibrary.py'):
#     clSource = 'c:/jan/behavbox'
# if not os.path.exists(clSource+'/ratCageProgramsV3/ClickTrainLibrary.py'):
#     clSource = 'd:/behavbox'
# if not os.path.exists(clSource+'/ratCageProgramsV3/ClickTrainLibrary.py'):
#     raise Exception('No valid path to ratCageProgramsV2 and 3 libraries')
# from sys import path as syspath
# from sys import stdout
# syspath.append(clSource+'/ratCageProgramsV3')
# syspath.append(clSource+'/ratCageProgramsV2')

import listScheduler2 as sc
import PicsWithSounds as sl
successStim=sl.pictureAndSoundStimulus(ID='Success')
successStim.ready()
failStim=sl.pictureAndSoundStimulus(ID='Fail')
failStim.ready()

""" 
adapt listScheduler to teh fact that there is no start spout but there are three choice spouts:
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
        
        
                
    
