from player import player
import fundamental
import _thread
import time
myplayer=player('COM4','COM5','COM3',90,1)  #par 串口地址（左手、右手、控制阀）、BPM、id标号
myplayer.init()
fundamental.preprocessing()
result=fundamental.sampling()
def air_control():
    f = open("littleStar_air.txt","r")
    line = f.readline()
    while(line):
<<<<<<< HEAD
        print(line)
        a = line.split(" ")
        #time.sleep(float(a[1]))
        myplayer.choose_power(int(a[0]),float(a[1]))
        time.sleep(float(a[1]))
        line = f.readline()

def play_control():
    a=open('result.txt')
    result=[]
    for line in a.readline():
        result.append(line)
    print('end')
    for i in range(0,len(result)):
        if(result[i]=='N'):
            continue
        myplayer.play_sound(result[i],60/(fundamental.bpm*4))

if __name__ == '__main__':
    # 创建两个线程
    try:
        _thread.start_new_thread(play_control, ())
        _thread.start_new_thread(air_control, ())
    except:
        print("Error: 无法启动线程")

    while 1:
        pass

