import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import wave
import soundfile as sf
import sys
import os
import glob
from moviepy.editor import *
from pydub import AudioSegment
#基频提取
bpm=90
s=0.1
#去掉音频前面无声部分
def preprocessing():
    wave,freq=librosa.load('sound4.wav',sr=32000)
    print(wave)
    print(freq)
    now=0
    while(wave[now]==0):
        now=now+1
    sf.write('afterpre.wav',wave[now:len(wave)],32000)
    #TODO  滤波

#自相关 autocorrelation
def ACF(data,t):
    output=np.zeros((int)(len(data)),dtype=float)
    for i in range(0,(int)(len(data))):
        for j in range(t,t+(int)(len(data))):
            output[i]=output[i]+data[j%len(data)]*data[(j+i)%len(data)]
    return output

def ACF2(data,t):
    output = np.zeros((int)(len(data)), dtype=float)
    for i in range(0, (int)(len(data))):
        for j in range(t, t+(int)(len(data)) - i):
            output[i] = output[i] + data[j] * data[j + i]
    return output

#差值函数
def difference(data):
    output = np.zeros((int)(len(data)/2), dtype=float)
    for i in range(0, (int)(len(data)/2)):
        for j in range(0, (int)(len(data)/2)):
            output[i] = output[i] + (data[j % len(data)]-data[(j + i) % len(data)])**2
    return output

#累积均值归一化差函数
def CMNDF(input):
    output=np.zeros(len(input),dtype=float)
    output[0]=1
    for i in range(1,len(input)):
        sum=0
        for j in range(1,i+1):
            sum=sum+input[j]
        output[i]=(float)(input[i])/((1/i)*sum)
    return output

def getkey(period):
    # if(period>=120 and period<=124): #钢琴
    #     return 'C'
    # elif(period>=106 and period<=110):
    #     return 'D'
    # elif(period>=95 and period<=99):
    #     return 'E'
    # elif(period>=89 and period<=93):
    #     return 'F'
    # elif(period>=79 and period<=83):
    #     return 'G'
    # elif(period>=71 and period<=75):
    #     return 'A'
    # elif(period>=63 and period<=67):
    #     return 'B'
    # elif(period>=59 and period<=62):
    #     return 'HC'
    # else:
    #     return 'N'
    if (period >= 54 and period <= 60):    #陶笛
        return 'C'
    elif (period >= 50 and period <= 53):
        return 'D'
    elif (period >= 45 and period <= 49):
        return 'E'
    elif (period >= 42 and period <= 44):
        return 'F'
    elif (period >= 38 and period <= 41):
        return 'G'
    elif (period >= 35 and period <= 37):
        return 'A'
    elif (period >= 33 and period <= 34 ):
        return 'B'
    elif (period >= 29 and period <= 31):
        return 'H'
    else:
        return 'N'
def getperiod(input,result):
    for i in range(0,len(input)-1):
        if (input[i]<input[i+1]):
            if input[i]<s:
                result.append(getkey(i))
                # print(i)
                # print(result)
                return
    result.append('N')
    # print(result)

#进行基频提取
def sampling():
    now=0
    result=[]
    while(now<librosa.get_duration(filename='afterpre.wav')):
        wave,freq=librosa.load('afterpre.wav',sr=32000,offset=now+60/(bpm*16),duration=60/(bpm*16))  #最小音符时值十六分音符，每个音符采样四次，取第二个采样点
        if(len(wave)==0):
            break
        diff=difference(wave)
        cmndf=CMNDF(diff)
        getperiod(cmndf,result)
        # plt.title = ("waveform")
        # plt.plot(np.arange(len(wave)),wave, 'b')
        # # # plt.plot(np.arange(len(ACF(wave,0))), ACF(wave,0), 'r')
        # # # plt.plot(np.arange(len(ACF2(wave,0))), ACF2(wave,0), 'g')
        # plt.plot(np.arange(len(cmndf)),cmndf,'r')
        # plt.show()
        # plt.figure()
        now=now+60/(bpm*4)
    f= open('result.txt','w')
    f.writelines(result)
    f.close()
    return result
if __name__=='__main__':
    preprocessing()
    sampling()