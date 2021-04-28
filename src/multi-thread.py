from fundamental import *
import threading
import time
import os
import librosa
import math
from numba import jit
from multiprocessing import Process,Manager
from pydub import AudioSegment
from pydub.utils import make_chunks
import shutil

def thread_task(thread_id,source,return_dict):
    return_dict[thread_id]=sampling(source)


@jit
def split():
    source = AudioSegment.from_file('../wav/afterpre.wav')
    unit=math.ceil(librosa.get_duration(filename='../wav/afterpre.wav')/(5/(bpm*4)))    #基频提取单元数目
    min_unit_size=math.ceil(10/(60/(bpm*4)))                                       #每个核最小处理的单元数目
    count=min(math.ceil(unit/min_unit_size),os.cpu_count())                       #需要并行的总核数
    #count=os.cpu_count()
    common_size=int(unit/count)                                                   #平均分配每个核的任务量
    left_size=int(unit%count)
    unit_size = 60/(bpm*4)
    start=float(0)
    for i in range(count):
        if(i<left_size):
            end=start+(common_size+1)*unit_size
            audio_chunk=source[start*1000:end*1000]
        else:
            end = start + common_size* unit_size
            audio_chunk=source[start*1000:end*1000]
        audio_chunk.export('./temp/source {}.wav'.format(i), format="wav")
        start=end
    return count

@jit
def multiprocess(filename):   #多线程解析
    count=split()
    threads = []
    manager=Manager()
    return_dict=manager.dict()
    for i in range(count):
        p = Process(target=thread_task,args=(i,'./temp/source {}.wav'.format(i),return_dict))
        p.start()
        threads.append(p)
    for p in threads:
        p.join()
    result=[]
    for i in range(count):
        result=result+return_dict[i]
    return result

def singleprocess(filename):  #单线程求解
    return sampling(filename)

if __name__=='__main__':
    os.makedirs('./temp')
    t0 = time.clock()
    preprocessing('../wav/强度.wav')
    print(multiprocess('../wav/afterpre.wav'))
    print(singleprocess('../wav/afterpre.wav'))
    print(time.clock() - t0)
    shutil.rmtree('./temp')

