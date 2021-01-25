from player import player
import fundamental
import _thread
import time
from removeNoise import start,stand,intensity

myplayer=player('COM9','COM3','COM4','COM10',90,1)  #par 串口地址（左手、右手、控制阀）、BPM、id标号
Sampling_interval_time = 0.1    #表示力度采样的时间间隔
standard_value_num = 700
time_a = 0
time_b = 0
myplayer.init()
fundamental.preprocessing()
result=fundamental.sampling()
start()

def air_control(a):
    for i in range(len(a)):
        if(int(a[i]) == 0):
            max = 1850 - int(a[i])
            myplayer.set_separate(False)
            myplayer.choose_power(max, (Sampling_interval_time) / 2)
            time.sleep(Sampling_interval_time/ 2)
            time_a += Sampling_interval_time
        else:
            myplayer.set_separate(True)
            myplayer.choose_power(1850 - int(a[i]),(Sampling_interval_time)/2)
            time.sleep(Sampling_interval_time/2)
            time_a += Sampling_interval_time

def play_control():
    # a=open('result.txt')
    # result=[]
    # for line in a.readline():
        # result.append(line)
    for i in range(0,len(result)):
        if(result[i]=='N'):
            continue
        myplayer.play_sound(result[i],60/(fundamental.bpm*4))

if __name__ == '__main__':
    # 创建两个线程
    try:
        print("nmh")
        _thread.start_new_thread(play_control, ())
        _thread.start_new_thread(air_control, (intensity,))
    except:
        print("Error: 无法启动线程")

    while 1:
        pass