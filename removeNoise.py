import time
from datetime import timedelta as td
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf
from librosa.core import istft
import scipy
import time
import fundamental
import _thread
from scipy.io import wavfile
import noisereduce as nr
from player import player

# myplayer=player('COM3','COM9','COM4','COM10',90,1)
#fundamental.preprocessing()
#result=fundamental.sampling()
Sampling_interval_time = 0.1    #表示力度采样的时间间隔
standard_value_num = 700
stand = []
intensity = []

def intensity_change(mean,each):
    return int(standard_value_num * each / mean)

def mean(a):
    sum = 0
    num = 0
    for each in a:
        if each >= 0.001:
            sum += each
            num += 1
    return sum/num

def load_form():
    with open("form.txt","r") as f:
        line = f.readline()
        while line:
            a = line.split(" ")
            stand.append(a)
            if int(a[1]) > 1840:
                return
            line = f.readline()


def binarySearch(arr, l, r, x):
    x = abs(x)
    if r >= l:
        mid = int(l + (r - l) / 2)
        if mid < 16:
            if float(arr[mid][0]) <= x and float(arr[mid + 1][0]) >= x:
                return mid
            elif float(arr[mid][0]) > x:
                return binarySearch(arr, l, mid - 1, x)
            elif float(arr[mid + 1][0]) < x:
                return binarySearch(arr, mid + 1, r, x)
        else:
            return 16
    else:
        return -1

def play_control():
    a=open('result.txt')
    result=[]
    for line in a.readline():
        result.append(line)
    print('end')
    for i in range(0,len(result)):
        if(result[i]=='N'):
            continue
        myplayer.play_sound(result[i],60/(fundamental.bpm*4))

def start():
    load_form()
    sound_data, sound_rate = sf.read("sound4.wav")
    sound_data.shape = -1
    noise_data, noise_rate = sf.read("noise.wav")
    noise_data.shape = -1
    after = nr.reduce_noise(audio_clip=sound_data, noise_clip=noise_data)
    plt.plot(np.arange(len(after)), after, 'r')
    plt.show()
    Sampling_interval = Sampling_interval_time / 1 * 100000
    now_interval = 0
    while now_interval < len(after):
        now_interval_intensity = 0
        for i in range(int(now_interval - Sampling_interval / 2), int(now_interval + Sampling_interval / 2)):
            if i >= len(after):
                break
            if (after[i] > now_interval_intensity):
                now_interval_intensity = after[i]
        p = binarySearch(stand, 0, int(len(stand) - 1), float(now_interval_intensity))
        intensity.append(stand[p][1])
        now_interval += Sampling_interval

if __name__ == '__main__':
    load_form()
    sound_data, sound_rate = sf.read("sound2.wav")
    sound_data.shape = -1
    noise_data, noise_rate = sf.read("sound.wav")
    noise_data.shape = -1
    after = nr.reduce_noise(audio_clip=sound_data, noise_clip=noise_data)
    plt.plot(np.arange(len(after)), after, 'r')
    plt.show()
    Sampling_interval = Sampling_interval_time / 1 * 100000
    now_interval = 0
    intensity = []
    valve_num = []
    while now_interval < len(after):
        now_interval_intensity = 0
        for i in range(int(now_interval - 5000 / 2), int(now_interval + 5000 / 2)):
            if i >= len(after):
                break
            if (after[i] > now_interval_intensity):
                now_interval_intensity = after[i]
        p = binarySearch(stand, 0 ,int(len(stand)-1),float(now_interval_intensity))
        intensity.append(stand[p][1])
        now_interval += Sampling_interval

    myplayer.play_sound('C',1)
    myplayer.set_separate(False)
    time.sleep(2)
    try:
        _thread.start_new_thread(air_control, (intensity,))
        _thread.start_new_thread(play_control, ())
    except:
        print("Error: 无法启动线程")
    while 1:
        pass
    # for each in valve_num:
    #     # myplayer.choose_power(each,Sampling_interval_time/2)
    #     print(each)
    #     time.sleep(Sampling_interval_time)




