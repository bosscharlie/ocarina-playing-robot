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

Sampling_interval_time = 0.1    #表示力度采样的时间间隔
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
        if(int(a[i]) == 0):
            max = 1850 - int(a[i])
            myplayer.set_separate(False)
            # print("cnm")
            # myplayer.choose_power(0, 0.001)
            # myplayer.choose_power(0, 0.001)
            # myplayer.choose_power(0, 0.001)
            # myplayer.choose_power(0, 0.001)
            myplayer.choose_power(max, (Sampling_interval_time) / 2)
            time.sleep(Sampling_interval_time/ 2)
        else:
            myplayer.set_separate(True)
            myplayer.choose_power(1850 - int(a[i]),(Sampling_interval_time)/2)
            time.sleep(Sampling_interval_time/2)

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

if __name__ == '__main__':

    load_form()
    myplayer.play_sound('C', 1)
    sound_data, sound_rate = sf.read("sound2.wav")
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
        now_interval_intensity = 0
        for i in range(int(now_interval - 1000 / 2), int(now_interval + 1000 / 2)):
            if i >= len(after):
                break
            if (after[i] > now_interval_intensity):
                now_interval_intensity = after[i]
        # intensity.append(now_interval_intensity)
        # now_interval += Sampling_interval
        # print(stand)
        # print(0)
        # print(len(stand))
        # print(after[int(now_interval)])
        p = binarySearch(stand, 0 ,int(len(stand)-1),float(now_interval_intensity))
        intensity.append(stand[p][1])
        # print(after[int(now_interval)],"cnm",stand[p][1])
        now_interval += Sampling_interval
    # mean_intensity = mean(intensity)

    #myplayer.play_sound('C',1)
    myplayer.set_separate(False)
    time.sleep(2)
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




