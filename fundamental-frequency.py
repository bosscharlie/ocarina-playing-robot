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

video = VideoFileClip('test.mp4')
audio = video.audio
audio.write_audiofile('test.mp3')