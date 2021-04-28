from player import player
# from main import myplayer

if __name__ == '__main__':
    myplayer = player('COM9', 'COM3', 'COM4', 'COM10', 90, 1)
    myplayer.set_separate(True)
    myplayer.play_sound('D', 1)
    Sampling_interval_time = 10
    time = 0.5
    now_position = 0
    while(now_position < 1850):
        myplayer.choose_power(1850 - now_position,time)
        print(now_position)
        now_position += Sampling_interval_time