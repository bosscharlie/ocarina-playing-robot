from player import player
myplayer=player('COM4','COM5','COM3',90,1)  #par 串口地址（左手、右手、控制阀）、BPM、id标号
myplayer.init()

myplayer.play_sound('C',1)  #参数为音名及时长
myplayer.play_sound('D',1)
myplayer.play_sound('E',1)
myplayer.play_sound('F',1)
myplayer.play_sound('G',1)
myplayer.play_sound('A',1)
myplayer.play_sound('B',1)
myplayer.play_sound('HC',1)
myplayer.play_sound('HD',1)
myplayer.init()
