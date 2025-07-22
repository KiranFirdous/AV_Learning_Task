#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 10:55:08 2025

How to harvest spoken words for word lists and test them.

@author: jan
"""
#%%
import scipy.io.wavfile as wav
from scipy.signal import resample
import ClickTrainLibrary as cl
# import PicsWithSounds as ps
cl.soundPlayer=cl.pygameSoundHardware() # this will initialize pygame
import time
import numpy as np
from matplotlib import pyplot as plt
# from random import shuffle
# from copy import deepcopy
# import psyPhysConfig as config
# from math import isnan
from glob import glob
from os import path
import numpy as np
import scipy.io.wavfile as wav

pictureDir='stimuli/pictures/'

# """

# Step one: we need one word for each picture in the pictureDir.
# List those so the can be copied and pasted, first into translation to Chinese, then text-to-speech
    
# """
# availableStimTypes=[ path.basename(x) for x in glob(pictureDir+'*.jpeg')]        
# availableStimTypes=[ x[:-5] for x in availableStimTypes]
# availableStimTypes.remove('Fail')
# availableStimTypes.remove('Success')
# # availableStimTypes.remove('Sweet Potato') 
# # availableStimTypes.remove('Spanish') 
# # availableStimTypes.remove('WaxApple') 
# # availableStimTypes.remove('YellowPitaya') 
# availableStimTypes.sort()
# print()
# for word in availableStimTypes:
#     print(word+', ', end="")
    
""" 

This created the list 

Apple, Apricot, Asparagus, Avocado, Banana, Basil, BeanSprout, Beetroot, BellPepper, Blueberry, Broccoli, Cabbage, Carrot, Cashew, Celery, Cherry, Chili, ChineseCabbage, ChineseChives, ChoiSum, Cinnamon, Coconut, Corn, Cranberry, Cucumber, Daikon, Date, DragonFruit, Durian, Eggplant, Fig, Garlic, Ginger, Gooseberry, Grape, Grapefruit, Guava, Jackfruit, Jasmine, Kale, Kiwi, Lemon, Lettuce, Lime, Longan, Louqat, Lychee, Mango, Mangosteen, Melon, Mint, Mulberry, Mushroom, Okra, Olive, Onion, Orange, Oregano, Papaya, Parsley, PassionFruit, Pea, Peach, Pear, Pepper, Peppermint, Persimmon, Pineapple, Plum, Pomegranate, Pomelo, Potato, Prune, Pumpkin, Radish, Rambutan, Raspberry, Rosemary, Soybean, Spice, Spinach, Squash, StarFruit, Strawberry, Tamarind, Taro, Thyme, Tomato, Turnip, Watermelon, WaxApple, Zuccini
    
#%% Now copy the list into translate.google.com to get it translated to Chinese. 

This genereates the list 

Canto:
           "蘋果", "杏桃", "蘆筍", "酪梨", "香蕉", "羅勒", "豆芽", "甜菜根", "燈籠椒", "藍莓", "綠花椰菜", "高麗菜", "胡蘿蔔", "腰果", "芹菜", "櫻桃", "辣椒", "大白菜", "韭菜", "菜心", "肉桂", "椰子", "玉米", "蔓越莓", "黃瓜", "白蘿蔔", "椰棗", "火龍果", "榴槤", "茄子", "無花果", "大蒜", "生薑", "醋栗", "葡萄", "西柚", "番石榴", "菠蘿蜜", "茉莉", "羽衣甘藍", "奇異果", "檸檬", "生菜", "青檸", "龍眼", "枇杷", "荔枝", "芒果", "山竹", "甜瓜", "薄荷", "桑葚", "蘑菇", "秋葵", "橄欖", "洋蔥", "柳橙", "牛至", "木瓜", "歐芹", "百香果", "豌豆", "桃子", "梨子", "胡椒", "薄荷", "柿子", "鳳梨", "李子", "石榴槤", "柚子", "馬鈴薯", "西梅干", "南瓜", "蘿蔔", "紅毛丹", "覆盆子", "迷迭香", "大豆", "香料", "菠菜", "南瓜", "楊桃", "草莓", "羅望子", "芋頭", "百里香", "番茄", "蕪菁", "西瓜", "蓮霧", "西葫蘆"

Simplified Chinese
"苹果", "杏", "芦笋", "鳄梨", "香蕉", "罗勒", "豆芽", "甜菜根", "灯笼椒", "蓝莓", "西兰花", "卷心菜", "胡萝卜", "腰果", "芹菜", "樱桃", "辣椒", "大白菜", "韭菜", "菜心", "肉桂", "椰子", "玉米", "蔓越莓", "黄瓜", "白萝卜", "枣", "火龙果", "榴莲", "茄子", "无花果", "大蒜", "生姜", "醋栗", "葡萄", "柚子", "番石榴", "菠萝蜜", "茉莉花", "羽衣甘蓝", "猕猴桃", "柠檬", "生菜", "酸橙", "龙眼", "枇杷", "荔枝", "芒果", "山竹", "甜瓜", "薄荷", "桑葚", "蘑菇", "秋葵", "橄榄", "洋葱", "橙子", "牛至", "木瓜", "欧芹", "百香果", "豌豆", "桃子", "梨", "胡椒", "薄荷", "柿子", "菠萝", "李子", "石榴柚子", "土豆", "西梅", "南瓜", "萝卜", "红毛丹", "覆盆子", "迷迭香", "大豆", "香料", "菠菜", "南瓜", "杨桃", "草莓", "罗望子", "芋头", "百里香", "番茄", "芜菁", "西瓜", "莲雾", "西葫芦"

Paste this into https://www.narakeet.com/languages/chinese-text-to-speech/ to generate mandarin audio files
Or https://www.narakeet.com/languages/cantonese-text-to-speech/ to generate canto audio 
Or https://www.narakeet.com/languages/american-accent-generator/ to generate US english audio

Make sure you choose teh SLOW option

Save these as WAV files.

"""

availableStimTypes = ["Apple", "Apricot", "Asparagus", "Avocado", "Banana", "Basil", "BeanSprout", "Beetroot", "BellPepper", "Blueberry", "Broccoli", "Cabbage", "Carrot", "Cashew", "Celery", "Cherry", "Chili", "ChineseCabbage", "ChineseChives", "ChoiSum", "Cinnamon", "Coconut", "Corn", "Cranberry", "Cucumber", "Daikon", "Date", "DragonFruit", "Durian", "Eggplant", "Fig", "Garlic", "Ginger", "Gooseberry", "Grape", "Grapefruit", "Guava", "Jackfruit", "Jasmine", "Kale", "Kiwi", "Lemon", "Lettuce", "Lime", "Longan", "Louqat", "Lychee", "Mango", "Mangosteen", "Melon", "Mint", "Mulberry", "Mushroom", "Okra", "Olive", "Onion", "Orange", "Oregano", "Papaya", "Parsley", "PassionFruit", "Pea", "Peach", "Pear", "Pepper", "Peppermint", "Persimmon", "Pineapple", "Plum", "Pomegranate", "Pomelo", "Potato", "Prune", "Pumpkin", "Radish", "Rambutan", "Raspberry", "Rosemary", "Soybean", "Spice", "Spinach", "Squash", "StarFruit", "Strawberry", "Tamarind", "Taro", "Thyme", "Tomato", "Turnip", "Watermelon", "WaxApple", "Zuccini"]
cantoStim=["蘋果", "杏桃", "蘆筍", "酪梨", "香蕉", "羅勒", "豆芽", "甜菜根", "燈籠椒", "藍莓", "綠花椰菜", "高麗菜", "胡蘿蔔", "腰果", "芹菜", "櫻桃", "辣椒", "大白菜", "韭菜", "菜心", "肉桂", "椰子", "玉米", "蔓越莓", "黃瓜", "白蘿蔔", "椰棗", "火龍果", "榴槤", "茄子", "無花果", "大蒜", "生薑", "醋栗", "葡萄", "西柚", "番石榴", "菠蘿蜜", "茉莉", "羽衣甘藍", "奇異果", "檸檬", "生菜", "青檸", "龍眼", "枇杷", "荔枝", "芒果", "山竹", "甜瓜", "薄荷", "桑葚", "蘑菇", "秋葵", "橄欖", "洋蔥", "柳橙", "牛至", "木瓜", "歐芹", "百香果", "豌豆", "桃子", "梨子", "胡椒", "薄荷", "柿子", "鳳梨", "李子", "石榴槤", "柚子", "馬鈴薯", "西梅干", "南瓜", "蘿蔔", "紅毛丹", "覆盆子", "迷迭香", "大豆", "香料", "菠菜", "南瓜", "楊桃", "草莓", "羅望子", "芋頭", "百里香", "番茄", "蕪菁", "西瓜", "蓮霧", "西葫蘆"]

#%%
for word in availableStimTypes:
    print(word)

#%% 




fs,signal=wav.read('stimuli/MandarinAudio.wav')
# fs,signal=wav.read('stimuli/CantoneseAudio.wav')
# fs,signal=wav.read('stimuli/USenglishAudio.wav')

# Check that this is high sample rate
fs

# Check if signal is mono
signal.shape

# Now let's think about segmentation. 
plt.figure(1)
plt.clf()
plt.plot(signal)
# plt.plot(signal[:800000])

# Zoom in and inspect. We see that words in this example are separated by relative silences of over 4000 samples
#%%
# wdwlen=8000 # good for Canto
wdwlen=6000 # good for Mandarin
steplen = np.floor(wdwlen / 4)
# wdwlen=5000 # good for Mandarin?

absSig=np.abs(signal)
nsteps=int(np.floor(len(absSig)/steplen))
ampvals=np.zeros((nsteps))
for ii in range(nsteps):
    x=int(ii*steplen)
    ampvals[ii]=absSig[x:x+wdwlen].sum()
ampvals/=ampvals.max()
ampvals[0]=0    
plt.figure(2)
plt.clf()
plt.plot(ampvals,'.-')
plt.tight_layout()


# plt.figure()
# plt.hist(ampvals,300)
#%% by inspection we set a threshold of 0.035
# silences must have amp points below thresh
# thresh=0.01 # worked well for USenglish
# thresh=0.04  # worked well for Mandarin

thresh=0.16  # worked well for Canto
minima=[]

inValley=False
localMin=10e10

# in the canto audio we find long silences probably because the audio skipeed words it didin't know.
# We need to keep track of these in suspiciousValleys and suspiciousIdx

valleyLen=0
valleyCount=0
suspiciousValleys=[]
suspiciousIdx=[]

for ii in range(nsteps):
    if ampvals[ii]<thresh:
        # we are in  a valley. Find the bottom of it
        if not inValley:
            # entering valley
            inValley=True
            valleyCount+=1
            valleyLen=0
            localMin=ampvals[ii]
            x=ii
            continue
        else:
            # progressing through valley
            valleyLen+=1
            if valleyLen > 5:
                if (len(suspiciousValleys)==0) or (not suspiciousValleys[-1]==valleyCount):
                    if valleyCount < len(availableStimTypes):
                        suspiciousValleys.append(valleyCount)
                        suspiciousIdx.append(ii)
            if localMin>ampvals[ii]:
                localMin=ampvals[ii]
                x=ii
            continue
    else:
        # we are not in a valley. If we just exited valley we note last minimum
        if inValley:
            minima.append([x,localMin])
            inValley=False


            
# We want the number of minima to be equal to the number of availableStimTypes.
# If there are fewer minima then thresh is too low. 
print(f'We have {len(minima)} minima, {len(suspiciousValleys)} suspicious valleys, and {len(cantoStim)} stimulus tokens')     
minima=np.array(minima)

plt.figure(2)
plt.clf()
plt.plot(ampvals,'.-')
plt.plot(minima[:,0],minima[:,1],'r*')
for ii in range(len(minima)):
    plt.text(minima[ii,0]-1,-0.05,ii)
plt.tight_layout()

plt.figure(3)
plt.plot(minima[:,1])
#%%

boundaries=minima[:,0]*steplen+wdwlen/2
boundaries[0]=0
boundaries=np.append(boundaries,steplen*(len(ampvals)-1))

    
#%% Canto has a missing boundary at Nr 58
# So do this ONLY when processinghte Canto output
boundaries=np.insert(boundaries,59,1588000)
boundaries=np.insert(boundaries,86,2311490)

#%% Madarin is missing a boundary at 70
boundaries=np.insert(boundaries,70,1561090)
#%%
plt.figure(1)
plt.clf()
plt.plot(signal)
plt.plot(boundaries, np.zeros(boundaries.shape),'r.')  
plt.tight_layout()

for ii in range(len(boundaries)-1):
    plt.text(boundaries[ii],1000,ii)

#%% 
import subprocess
outdir='stimuli/soundsMandarin/'
# outdir='stimuli/USenglishSounds/'
# outdir='stimuli/soundsCanto/'
stimIdx=0
#%%
while stimIdx < len(availableStimTypes):
# for stimIdx, stim in enumerate(availableStimTypes):
    #%%
    stim=availableStimTypes[stimIdx]
    print(f'****** ')
    print(f'{stimIdx}: {stim}  {cantoStim[stimIdx]}')
    outfile=outdir+stim+'.wav'
    outsig=signal[int(boundaries[stimIdx]):int(boundaries[stimIdx+1])]
    # at this point we upsample the output to slow it down
    # outsig=resample(outsig,int(len(outsig)*1.5))
    wav.write(outfile, fs, outsig.astype(np.int16))
    subprocess.call(["play", outfile],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(0.6)
    stimIdx+=1
    
        


