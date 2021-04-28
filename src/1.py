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

def mean(a):
    sum = 0
    num = 0
    for each in a:
        if each >= 0.05:
            sum += each
            num += 1
    return sum/num

def air_control(a):
    for i in range(len(a)):
        if (a[i - 1] == 0 and a[i] != 0):
            max = 1850 - a[i]
            myplayer.set_separate(False)
            # print("cnm")
            # myplayer.choose_power(0, 0.001)
            # myplayer.choose_power(0, 0.001)
            # myplayer.choose_power(0, 0.001)
            # myplayer.choose_power(0, 0.001)
            if ((1850 - a[i]) > 1450):
                max = 1450
            myplayer.choose_power(max, (Sampling_interval_time) / 2)
            time.sleep(Sampling_interval_time / 2)
        else:
            myplayer.set_separate(True)
            myplayer.choose_power(1850 - a[i], (Sampling_interval_time) / 2)
            time.sleep(Sampling_interval_time / 2)


if __name__ == '__main__':

    myplayer.set_separate(False)
    sound_data, sound_rate = sf.read("../wav/sound2.wav")
    sound_data.shape = -1
    noise_data, noise_rate = sf.read("../wav/noise.wav")
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
        for i in range(int(now_interval - Sampling_interval / 2), int(now_interval + Sampling_interval / 2)):
            if i >= len(after):
                break
            if (after[i] > now_interval_intensity):
                now_interval_intensity = after[i]
        intensity.append(now_interval_intensity)
        now_interval += Sampling_interval

    mean_intensity = mean(intensity)

    for each in intensity:
        if each < 0.05:
            valve_num.append(0)
        else:
            valve_num.append(int(standard_value_num * each/mean_intensity))
    try:
        _thread.start_new_thread(air_control, (valve_num,))
    except:
        print("Error: 无法启动线程")
    while 1:
        pass
    # for each in valve_num:
    #     # myplayer.choose_power(each,Sampling_interval_time/2)
    #     print(each)
    #     time.sleep(Sampling_interval_time)