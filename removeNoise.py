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
import _thread
from scipy.io import wavfile
import noisereduce as nr
from main import myplayer
from player import player

Sampling_interval_time = 0.01    #表示力度采样的时间间隔
standard_value_num = 700
stand = []

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

def air_control(a):
    for i in range(len(a)):
        if(a[i - 1] == 0 and a[i] !=0):
            max = 1850 - a[i]
            myplayer.set_separate(False)
            # print("cnm")
            # myplayer.choose_power(0, 0.001)
            # myplayer.choose_power(0, 0.001)
            # myplayer.choose_power(0, 0.001)
            # myplayer.choose_power(0, 0.001)
            if((1850 - a[i]) > 1450):
                max = 1450
            myplayer.choose_power(max, (Sampling_interval_time) / 2)
            time.sleep(Sampling_interval_time/ 2)
        else:
            myplayer.set_separate(True)
            myplayer.choose_power(1850 - a[i],(Sampling_interval_time)/2)
            time.sleep(Sampling_interval_time/2)

def load_form():
    with open("form.txt","r") as f:
        line = f.readline()
        while line:
            a = line.split(" ")
            print(a)
            stand.append(a)
            if int(a[1]) > 1850:
                return
            line = f.readline()


def binarySearch(arr, l, r, x):
    if r >= l:
        mid = int(l + (r - l) / 2)
        if arr[mid][0] <= x and arr[mid + 1][0] >= x:
            return mid
        elif arr[mid][0] > x:
            return binarySearch(arr, l, mid - 1, x)
        elif arr[mid + 1][0] < x:
            return binarySearch(arr, mid + 1, r, x)
    else:
        return -1

if __name__ == '__main__':

    load_form()
    myplayer.play_sound('C', 1)
    sound_data, sound_rate = sf.read("sound3.wav")
    sound_data.shape = -1
    noise_data, noise_rate = sf.read("noise.wav")
    noise_data.shape = -1
    after = nr.reduce_noise(audio_clip=sound_data, noise_clip=noise_data)
    plt.plot(np.arange(len(after)), after, 'r')
    plt.show()
    Sampling_interval = Sampling_interval_time / 1 * 100000
    now_interval = 0

    

    intensity = []
    valve_num = []
    while now_interval < len(after):
        # now_interval_intensity = 0
        # for i in range(int(now_interval - 50 / 2), int(now_interval + 50 / 2)):
        #     if i >= len(after):
        #         break
        #     if (after[i] > now_interval_intensity):
        #         now_interval_intensity = after[i]
        # intensity.append(now_interval_intensity)
        # now_interval += Sampling_interval
        p = binarySearch(stand,0,len(stand),after[now_interval])
        intensity.append(stand[p][1])
        now_interval += Sampling_interval
    # mean_intensity = mean(intensity)

    #myplayer.play_sound('C',1)
    myplayer.set_separate(True)
    try:
        _thread.start_new_thread(air_control, (intensity,))
    except:
        print("Error: 无法启动线程")
    while 1:
        pass
    # for each in valve_num:
    #     # myplayer.choose_power(each,Sampling_interval_time/2)
    #     print(each)
    #     time.sleep(Sampling_interval_time)




