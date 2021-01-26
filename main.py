from player import player
import fundamental
import _thread
import time
from removeNoise import start,stand,intensity
from transcribe import audio_record

audio_record('sound4.wav',5)
myplayer=player('COM9','COM3','COM4','COM10',90,1)  #par 串口地址（左手、右手、控制阀）、BPM、id标号
Sampling_interval_time = 0.1   #表示力度采样的时间间隔
standard_value_num = 700
# myplayer.init()
# fundamental.preprocessing()
# result=fundamental.sampling()
time_a = 0
time_b = 0
start()
print(intensity)
def air_control(a):
    starttime = time.time()
    totaltime = 0.
    for i in range(len(a)):
        if(int(a[i]) == 0):
            max = 1850 - int(a[i])
            # starttime = time.time()
            t = myplayer.set_separate(False,Sampling_interval_time)
            myplayer.choose_power(max,t)
            # time.sleep((Sampling_interval_time)/ 2)
            # endtime = time.time()
            # print("cnm",endtime - starttime)
            totaltime += Sampling_interval_time
        else:
            # starttime = time.time()
            t = myplayer.set_separate(True,Sampling_interval_time)
            myplayer.choose_power(1850 - int(a[i]),t)
            # endtime = time.time()
            # print("nmh", endtime - starttime)
            # time.sleep((Sampling_interval_time - 0.01)/2)
            totaltime += Sampling_interval_time
    endtime = time.time()
    print(totaltime)

def play_control():
    a=open('result.txt')
    result=[]
    for line in a.readline():
        result.append(line)
    for i in range(0,len(result)):
        if(result[i]=='N'):
            myplayer.stop(60/(fundamental.bpm*4))
            continue
        # starttime = time.time()
        myplayer.play_sound(result[i],60/(fundamental.bpm*4))
        # endtime = time.time()
        # print("nmsl",endtime - starttime)

if __name__ == '__main__':
    print("nmsl")
    # 创建两个线程
    try:
        print("nmh")
        _thread.start_new_thread(play_control, ())
        _thread.start_new_thread(air_control, (intensity,))
    except:
        print("Error: 无法启动线程")

    while 1:
        pass
