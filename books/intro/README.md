# 从一张卡到一万张卡（入门篇）

**大规模 GPU 集群训练是怎么跑起来的**

作者：Dr. Dezeming

一个千亿参数的模型，权重、梯度、优化器状态加起来有几千 GB，而一张显卡只有 80 GB。于是训练被拆到上千张卡上，卡与卡之间靠网络连成一台机器。

[开始阅读第 1 章](chapters/ch01.md)　｜　[下载 PDF](../../output/gpu-cluster-intro.pdf ':ignore')（98 页，9.1 MB）

## 目录

### 第一篇　算账

- [第 1 章　一个模型要吃掉多少算力](chapters/ch01.md)
- [第 2 章　一张卡的尺寸](chapters/ch02.md)
- [第 3 章　从一台机器到一座机房](chapters/ch03.md)

### 第二篇　一台机器里的账

- [第 4 章　显卡在算什么](chapters/ch04.md)
- [第 5 章　数字的精度](chapters/ch05.md)
- [第 6 章　训练一步的流水账](chapters/ch06.md)

### 第三篇　把模型摊开

- [第 7 章　把模型切开：张量并行与流水并行](chapters/ch07.md)
- [第 8 章　把数据分开：数据并行与显存分片](chapters/ch08.md)
- [第 9 章　混合并行的一张地图](chapters/ch09.md)
- [第 10 章　卡与卡怎么说话](chapters/ch10.md)

### 第四篇　集群的另一面

- [第 11 章　会坏的东西](chapters/ch11.md)
- [第 12 章　会算错的东西](chapters/ch12.md)
- [第 13 章　会等的东西](chapters/ch13.md)
- [第 14 章　谁来管这些卡](chapters/ch14.md)
- [第 15 章　一条完整的训练流水线](chapters/ch15.md)
