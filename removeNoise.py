import time
from datetime import timedelta as td
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf
from librosa.core import istft
import scipy
from scipy.io import wavfile
import noisereduce as nr


sound_data,sound_rate = sf.read("sound.wav")
sound_data.shape = -1
plt.plot(np.arange(len(sound_data)),sound_data,'r')
plt.show()
noise_data,noise_rate = sf.read("noise.wav")
noise_data.shape = -1
plt.plot(np.arange(len(noise_data)),noise_data,'r')
plt.show()
a = nr.reduce_noise(audio_clip=sound_data,noise_clip=noise_data)
plt.plot(np.arange(len(a)),a,'r')
plt.show()