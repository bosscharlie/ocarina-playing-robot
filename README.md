# ocarina-playing-robot
## 一、文件结构
- `player.py` 音符与动作的映射。对灵巧手演奏相关的参数配置与函数调用进行了封装，外部调用时只需创建一个对象实例后，通过调用`play_sound(key,time)`即可演奏音符
- `main.py` 主程序
- `audioTransiton.py` 提取视频素材中的音频
- `fundamental.py` 音频信号基频提取

## 二、系统运行流程

![b8bde9f3b7487a26229a81106b8e025](C:\Users\87857\Desktop\b8bde9f3b7487a26229a81106b8e025.png)

## 音符动作映射
由陶笛复杂度较低，所以将音符与灵巧手手势做一一映射，在`player.py`中预设好不同音符对应的灵巧手参数，输入音符保持时长，完成对灵巧手姿势及保持的映射。

## 基频提取流程
  - 设置音频信号速度bpm及YIN算法阈值s

  - 将音频信号进行等长切分采样，将每个采样段分为四份，取第二段（极品特征最明显的一段）进行YIN算法

  - 用差值版本的自相关函数对音频序列进行自相关运算 `func difference()`
    
  - $$
    d_t(\tau)=\sum_{j=1}^W(x_j-x_{j+\tau})^2
    $$
    
  - 将自相关运算的结果通过累计均值归一化差函数进行归一化 `func CMNDF()`

  - $$
    d_t^{'}(\tau)=
    \begin{cases}
    1, & \text{if }\tau=0, \\
    \frac{d_t(\tau)}{[(\frac{1}{\tau}\sum_{j=1}^\tau d_\tau(j)]}, & \text{otherwise.}
    \end{cases}
    $$

  - 对归一化后的结果进行特征提取，选取阈值下的第一个波谷对应的抽样点位置作为该段音频的基频周期 `func getperiod()`

  - 与提前解析好的单音高基频周期进行比对，得出当前音频段对应的具体音高 `func getkey()`
