from player import player
import fundamental

myplayer=player('COM4','COM5','COM3',90,1)  #par 串口地址（左手、右手、控制阀）、BPM、id标号
fundamental.preprocessing()
result=fundamental.sampling()
for i in range(0,len(result)):
    if(result[i]=='N'):
        continue
    myplayer.play_sound(result[i],60/(fundamental.bpm*4))
