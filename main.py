from player import player
import _thread
import time
myplayer=player('COM9','COM3','COM4','COM10',90,1)  #par 串口地址（左手、右手、控制阀）、BPM、id标号

# myplayer.play_sound('C',1)  #参数为音名及时长
# myplayer.play_sound('D',1)
# myplayer.play_sound('E',1)
# myplayer.play_sound('F',1)
# myplayer.play_sound('G',1)
# myplayer.play_sound('A',1)
# myplayer.play_sound('B',1)
# myplayer.play_sound('HC',1)
# myplayer.play_sound('HD',1)
# myplayer.init()

def air_control():
    f = open("littleStar_air.txt","r")
    line = f.readline()
    while(line):
        print(line)
        a = line.split(" ")
        #time.sleep(float(a[1]))
        myplayer.choose_power(int(a[0]),float(a[1]))
        time.sleep(float(a[1]))
        line = f.readline()

def play_control():
    f = open("littleStar_melody.txt", "r")
    line = f.readline()
    while (line):
        print(line)
        a = line.split(" ")
        #time.sleep(float(a[1]))
        myplayer.play_sound(a[0], float(a[1]))
        time.sleep(float(a[1]))
        line = f.readline()

if __name__ == '__main__':
    for i in range(1000):
        myplayer.set_separate(True)
        print("true")
        time.sleep(1)
        myplayer.set_separate(False)
        print("false")
        time.sleep(1)
    myplayer.set_separate(True)
    print("true")
    time.sleep(0.01)
    myplayer.set_separate(False)
    print("false")
    time.sleep(0.01)
    # 创建两个线程
    try:
        _thread.start_new_thread(play_control, ())
        myplayer.set_separate(True)
        _thread.start_new_thread(air_control, ())
    except:
        print("Error: 无法启动线程")

    while 1:
        pass