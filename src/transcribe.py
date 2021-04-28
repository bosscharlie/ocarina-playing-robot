import wave
import pyaudio
def audio_record(outfile,rectime):
    CHUNK=1024
    FORMAT=pyaudio.paInt16
    CHANNELS=1
    RATE=16000

    p=pyaudio.PyAudio()
    stream=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    print("start________________")
    frames=[]
    for i in range(0,int(RATE/CHUNK*rectime)):
        data=stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("end_______________")
    wf=wave.open(outfile,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()