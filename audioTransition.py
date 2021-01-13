from moviepy.editor import *
#从视频中提取音频

video = VideoFileClip('test.mp4')
audio = video.audio
audio.write_audiofile('test.mp3')