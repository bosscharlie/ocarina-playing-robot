# ocarina-playing-robot
`player.py`中对灵巧手演奏相关的参数配置与函数调用进行了封装，外部调用时只需创建一个对象实例后，通过调用`play_sound(key,time)`即可演奏音符
`main.py`中对player的调用做了简单示例

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
