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

wave,freq=librosa.load('test.wav',sr=32000,offset=2,duration=0.1)
sf.write('test2.wav',wave,32000)
plt.title=("waveform")
plt.plot(np.arange(len(wave)),wave,'r')
plt.show()
plt.figure()