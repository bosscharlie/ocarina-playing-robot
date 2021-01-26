import serial
import time
class player:
    ser_left=''
    ser_valve=''
    ser_right=''
    ser_separate=''
    BPM=''
    hand_id=''
    def __init__(self,left_num,right_num,valve_num,separate_num,BPM,hand_id):
        self.ser_left=serial.Serial(left_num,115200)
        self.ser_valve=serial.Serial(valve_num,921600)
        self.ser_separate=serial.Serial(separate_num,9600)
        self.ser_right=serial.Serial(right_num,115200)
        self.ser_left.isOpen()
        self.ser_valve.isOpen()
        self.ser_right.isOpen()
        self.BPM=BPM
        self.hand_id=hand_id
    # 把数据分成高字节和低字节
    def init(self):
        self.setangle(self.ser_left, 100, 880, 800, 770, 1000, 199)   #init
        self.setangle(self.ser_right, 100, 880, 860, 840, 900, 100)
        self.setspeed(self.ser_left, 1000, 1000, 1000, 1000, 1000, 1000)
        self.setspeed(self.ser_right, 1000, 1000, 1000, 1000, 1000, 1000)
        self.set_valve(1850)
        time.sleep((60/self.BPM)*1)
    def data2bytes(self,data):
        rdata = [0xff] * 2
        if data == -1:
            rdata[0] = 0xff
            rdata[1] = 0xff
        else:
            rdata[0] = data & 0xff
            rdata[1] = (data >> 8) & (0xff)
        return rdata
    # 把十六进制或十进制的数转成bytes
    def num2str(self,num):
        str = hex(num)
        str = str[2:4]
        if (len(str) == 1):
            str = '0' + str
        str = bytes.fromhex(str)
        # print(str)
        return str
    # 求校验和
    def checknum(self,data, leng):
        result = 0
        for i in range(2, leng):
            result += data[i]
        result = result & 0xff
        # print(result)
        return result
    def setangle(self,ser,angle1, angle2, angle3, angle4, angle5, angle6): #(小拇指，无名指，中指，食指，大拇指，大拇指旋转)
        global hand_id
        if angle1 < -1 or angle1 > 1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle2 < -1 or angle2 > 1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle3 < -1 or angle3 > 1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle4 < -1 or angle4 > 1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle5 < -1 or angle5 > 1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle6 < -1 or angle6 > 1000:
            print('数据超出正确范围：-1-1000')
            return
        datanum = 0x0F
        b = [0] * (datanum + 5)
        # 包头
        b[0] = 0xEB
        b[1] = 0x90
        # hand_id号
        b[2] = self.hand_id
        # 数据个数
        b[3] = datanum
        # 写操作
        b[4] = 0x12
        # 地址
        b[5] = 0xCE
        b[6] = 0x05
        # 数据
        b[7] = self.data2bytes(angle1)[0]
        b[8] = self.data2bytes(angle1)[1]
        b[9] = self.data2bytes(angle2)[0]
        b[10] = self.data2bytes(angle2)[1]
        b[11] = self.data2bytes(angle3)[0]
        b[12] = self.data2bytes(angle3)[1]
        b[13] = self.data2bytes(angle4)[0]
        b[14] = self.data2bytes(angle4)[1]
        b[15] = self.data2bytes(angle5)[0]
        b[16] = self.data2bytes(angle5)[1]
        b[17] = self.data2bytes(angle6)[0]
        b[18] = self.data2bytes(angle6)[1]
        # 校验和
        b[19] = self.checknum(b, datanum + 4)
        # 向串口发送数据
        putdata = b''
        for i in range(1, datanum + 6):
            putdata = putdata + self.num2str(b[i - 1])
        ser.write(putdata)
        getdata = ser.read(9)


    def setspeed(self,ser, speed1, speed2, speed3, speed4, speed5, speed6):
        global hand_id
        if speed1 < 0 or speed1 > 1000:
            print('数据超出正确范围：0-1000')
            return
        if speed2 < 0 or speed2 > 1000:
            print('数据超出正确范围：0-1000')
            return
        if speed3 < 0 or speed3 > 1000:
            print('数据超出正确范围：0-1000')
            return
        if speed4 < 0 or speed4 > 1000:
            print('数据超出正确范围：0-1000')
            return
        if speed5 < 0 or speed5 > 1000:
            print('数据超出正确范围：0-1000')
            return
        if speed6 < 0 or speed6 > 1000:
            print('数据超出正确范围：0-1000')
            return
        datanum = 0x0F
        b = [0] * (datanum + 5)
        # 包头
        b[0] = 0xEB
        b[1] = 0x90
        # hand_id号
        b[2] = self.hand_id
        # 数据个数
        b[3] = datanum
        # 写操作
        b[4] = 0x12
        # 地址
        b[5] = 0xF2
        b[6] = 0x05
        # 数据
        b[7] = self.data2bytes(speed1)[0]
        b[8] = self.data2bytes(speed1)[1]
        b[9] = self.data2bytes(speed2)[0]
        b[10] = self.data2bytes(speed2)[1]
        b[11] = self.data2bytes(speed3)[0]
        b[12] = self.data2bytes(speed3)[1]
        b[13] = self.data2bytes(speed4)[0]
        b[14] = self.data2bytes(speed4)[1]
        b[15] = self.data2bytes(speed5)[0]
        b[16] = self.data2bytes(speed5)[1]
        b[17] = self.data2bytes(speed6)[0]
        b[18] = self.data2bytes(speed6)[1]
        # 校验和
        b[19] = self.checknum(b, datanum + 4)
        # 向串口发送数据
        putdata = b''
        for i in range(1, datanum + 6):
            putdata = putdata + self.num2str(b[i - 1])
        ser.write(putdata)
        getdata = ser.read(9)
    def set_valve(self,pos):
        if pos < 0 or pos > 2000:
            return
        datanum = 7
        putdata = b''
        b = [0] * (datanum + 5)
        b[0] = 0x55
        b[1] = 0xAA
        b[2] = 0x04
        b[3] = 0xFF
        b[4] = 0x21
        b[5] = 0x37
        b[6] = self.data2bytes(pos)[0]
        b[7] = self.data2bytes(pos)[1]
        b[8] = self.checknum(b, 8)
        for i in range(1, 10):
            putdata = putdata + self.num2str(b[i - 1])
        self.ser_valve.write(putdata)

    def set_separate(self,separate,t):
        start = time.time()
        putdata = b''
        b = 0x00
        if separate == True:
            b = 0x01
        putdata = putdata + self.num2str(b)
        self.ser_separate.write(putdata)
        end = time.time()
        return (t - (end - start))

    def choosepose(self,l):

        if l == 'C':
            self.setangle(self.ser_left, 100, 880, 650, 650, 730, 120)
            self.setangle(self.ser_right, 100, 880, 650, 630, 730, 60)
            # self.set_valve(1730)
        elif l == 'D':
            self.setangle(self.ser_left, 100, 880, 650, 650, 730, 120)
            self.setangle(self.ser_right, 100, 880, 800, 630, 730, 60)
            # self.set_valve(1705)
        elif l == 'E':
            self.setangle(self.ser_left, 100, 880, 650, 650, 730, 120)
            self.setangle(self.ser_right, 100, 880, 650, 800, 730, 60)
            # self.set_valve(1695)
        elif l == 'F':
            self.setangle(self.ser_left, 100, 880, 650, 650, 730, 120)
            self.setangle(self.ser_right, 100, 880, 800, 800, 730, 60)
            # self.set_valve(1645)
        elif l == 'G':
            self.setangle(self.ser_left, 100, 880, 800, 650, 730, 120)
            self.setangle(self.ser_right, 100, 880, 800, 630, 730, 60)
            # self.set_valve(1675)
        elif l == 'A':
            self.setangle(self.ser_left, 100, 880, 800, 650, 730, 120)
            self.setangle(self.ser_right, 100, 880, 800, 800, 730, 60)
            # self.set_valve(1660)
        elif l == 'B':
            self.setangle(self.ser_left, 100, 880, 800, 800, 730, 120)
            self.setangle(self.ser_right, 100, 880, 650, 800, 730, 60)
            # self.set_valve(1600)
        elif l == 'H':
            self.setangle(self.ser_left, 100, 880, 800, 800, 730, 120)
            self.setangle(self.ser_right, 100, 880, 800, 800, 730, 60)
            # self.set_valve(1500)
        elif l == 'K':
            self.setangle(self.ser_left, 100, 880, 800, 800, 730, 120)
            self.setangle(self.ser_right, 100, 880, 800, 800, 900, 60)
            # self.set_valve(1850)

    def choose_power(self,power,t):
        starttime = time.time()
        self.set_valve(power)
        endtime = time.time()
        time.sleep(t - (endtime - starttime))
            # print(t - (endtime - starttime))
        # self.set_valve(1850)

    def play_sound(self,key,t):
        starttime = time.time()
        self.choosepose(key)
        endtime = time.time()
        # print(t,endtime - starttime)
        time.sleep(t - (endtime - starttime))

    def stop(self,t):
        time.sleep(t)