from player import player
import _thread
import time
myplayer=player('COM4','COM5','COM3',90,1)  #par 串口地址（左手、右手、控制阀）、BPM、id标号

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
        # print(line)
        a = line.split(" ")
        # time.sleep(float(a[1]))
        myplayer.choose_power(int(a[0]),float(a[1]))
        line = f.readline()

def play_control():
    f = open("littleStar_melody.txt", "r")
    line = f.readline()
    while (line):
        # print(line)
        a = line.split(" ")
        myplayer.play_sound(int(a[0]), float(a[1]))
        line = f.readline()

if __name__ == '__main__':
    # 创建两个线程
    try:
        _thread.start_new_thread(play_control, ())
        _thread.start_new_thread(air_control, ())
    except:
        print("Error: 无法启动线程")

    while 1:
        pass