
import noisereduce as nr
import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np
#from test import Sampling_interval_time,time


Sampling_interval_time = 10
time = 0.5

if __name__ == '__main__':
    sound_data, sound_rate = sf.read("强度.wav")
    sound_data.shape = -1
    plt.plot(np.arange(len(sound_data)), sound_data, 'r')
    plt.show()
    print(len(sound_data))
    noise_data, noise_rate = sf.read("噪声.wav")
    noise_data.shape = -1
    plt.plot(np.arange(len(noise_data)), noise_data, 'r')
    plt.show()
    after = nr.reduce_noise(audio_clip=sound_data, noise_clip=noise_data)
    plt.plot(np.arange(len(after)), after, 'r')
    plt.show()
    now_time = time / 2 * 100000
    time = time * 100000
    max = 0
    with open("form.txt", "w") as f:
        now_position = 0
        while now_time < len(after):
            for i in range(int(now_time - 50 / 2), int(now_time + 50 / 2)):
                if i >= len(after):
                    break
                if (after[i] > max):
                    max = after[i]
            a = str(max) + " " + str(now_position)
            f.write(a+" "+ "\n")
            now_time += time
            print(now_time)
            now_position += Sampling_interval_time


