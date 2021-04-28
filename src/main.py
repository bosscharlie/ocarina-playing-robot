from player import player
import fundamental
import _thread
import threading
import time
from removeNoise import start,stand,intensity
from transcribe import audio_record

# audio_record('sound4.wav',5)
myplayer=player('COM9','COM3','COM4','COM10',90,1)  #par 串口地址（左手、右手、控制阀）、BPM、id标号
t = myplayer.set_separate(False,1)
Sampling_interval_time = 0.1   #表示力度采样的时间间隔
standard_value_num = 700
myplayer.init()
start()
# fundamental.preprocessing()
# result=fundamental.sampling()
time_a = 0
time_b = 0
print(intensity)
def air_control(a):
    # myplayer.choose_power(1700, 100)
    starttime = time.time()
    totaltime = 0.
    for i in range(len(a)):
        if(int(a[i]) == 0):
            max = 1850 - int(a[i])
            # starttime = time.time()
            t = myplayer.set_separate(False,Sampling_interval_time)
            #myplayer.choose_power(max,t)
            time.sleep(t)
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
    t = myplayer.set_separate(False,1)
    print(totaltime)
    return 0

def play_control(result):
    # myplayer.play_sound("C", 1)
    # myplayer.play_sound("D", 1)
    # myplayer.play_sound("E", 1)
    # myplayer.play_sound("F", 1)
    # myplayer.play_sound("G", 1)
    # myplayer.play_sound("A", 1)
    # myplayer.play_sound("B", 1)

    for i in range(0,len(result)):
        if(result[i]=='N'):
            myplayer.stop(60/(fundamental.bpm*4))
            continue
        # starttime = time.time()
        myplayer.play_sound(result[i],60/(fundamental.bpm*4))
        # endtime = time.time()
        # print("nmsl",endtime - starttime)
    return 0

if __name__ == '__main__':
    # t = myplayer.set_separate(True,1)

    a = open('../result.txt')
    result = []
    for line in a.readline():
        result.append(line)
    index=0
    while(result[index]=='N'):
        index=index+1
    myplayer.play_sound(result[index],1)
    print(result)

    t1 = threading.Thread(target = play_control,args=(result,))
    t2 = threading.Thread(target = air_control,args = (intensity,))
    t1.start()
    time.sleep(0.1)

    t2.start()
    t1.join()
    t2.join()