# 大规模 GPU 集群训练技术

一套讲大规模训练的读本，分两册。入门篇建立完整地图，专业篇把每一步的字节数、微秒数和故障模式算清楚。

在线阅读：<https://ai-crystal.github.io/GPU-Cluster-Training/>

| 册 | 讲什么 | 篇幅 | 在线阅读 | PDF |
|---|---|---|---|---|
| **入门篇**《从一张卡到一万张卡》 | 动机、结构、并行、故障，不推公式 | 98 页 | [开始阅读](books/intro/chapters/ch01.md) ｜ [目录](books/intro/README.md) | [PDF 9.1 MB](output/gpu-cluster-intro.pdf ':ignore') |
| **专业篇**《算力、通信与稳定性》 | 性能模型、通信账、并行细节、踩坑清单 | 236 页 | [开始阅读](books/pro/chapters/ch01.md) ｜ [目录](books/pro/README.md) | [PDF 13.2 MB](output/gpu-cluster-pro.pdf ':ignore') |

建议先读入门篇，再按需要翻专业篇。两册各自完整，只读一本也不影响理解。

## 这套书想讲清楚的一件事

一张 H100 有 80 GB 显存，一个 4050 亿参数的模型光权重就要 810 GB。于是训练被拆到几千张卡上，卡与卡之间靠网络连成一台机器。问题从"怎么写出模型"变成了"怎么让一万张卡像一张卡那样工作"。

显存怎么分，模型怎么切，梯度怎么汇总，网络怎么摆，坏了怎么恢复，慢了怎么定位。这些问题的答案都可以算出来，而不是靠感觉。书里的每一个数字都尽量落到具体的位置：多少字节、多少微秒、多少个百分点。

## 阅读入口

- [入门篇前言](books/intro/front/preface.md)　｜　[入门篇后记](books/intro/front/afterword.md)
- [专业篇前言](books/pro/front/preface.md)　｜　[专业篇后记](books/pro/front/afterword.md)
- [附录 A　术语与缩写](books/pro/appendix/appA.md)　｜　[附录 B　常用公式与估算表](books/pro/appendix/appB.md)

## 作者

Dr. Dezeming
