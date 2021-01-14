import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import wave
import soundfile as sf
import os
import glob
from moviepy.editor import *
from pydub import AudioSegment
#基频提取
bpm=90
#去掉音频前面无声部分
def preprocessing():
    wave,freq=librosa.load('single.wav',sr=32000)
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
#进行基频提取
def sampling():
    now=0
    while(now<librosa.get_duration(filename='afterpre.wav')):
        wave,freq=librosa.load('afterpre.wav',sr=32000,offset=now+60/(bpm*32),duration=60/(bpm*32))  #最小音符时值十六分音符，每个音符采样四次，取第二个采样点
        diff=difference(wave)
        cmndf=CMNDF(diff)
        plt.title = ("waveform")
        plt.plot(np.arange(len(wave)),wave, 'b')
        # # plt.plot(np.arange(len(ACF(wave,0))), ACF(wave,0), 'r')
        # # plt.plot(np.arange(len(ACF2(wave,0))), ACF2(wave,0), 'g')
        plt.plot(np.arange(len(cmndf)),cmndf,'r')
        plt.show()
        plt.figure()
        now=now+60/(bpm*8)

if __name__=='__main__':
    preprocessing()
    sampling()