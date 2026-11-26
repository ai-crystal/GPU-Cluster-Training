# 大规模 GPU 集群训练技术

> 从一张卡到一万张卡

一套讲大规模训练的读本，分两册。入门篇建立完整地图，专业篇把每一步的字节数、微秒数和故障模式算清楚。

显存怎么分，模型怎么切，梯度怎么汇总，网络怎么摆，坏了怎么恢复，慢了怎么定位。这些问题的答案都可以算出来，而不是靠感觉。

作者：Dr. Dezeming　·　2026

**在线阅读**：[在线阅读站](https://ai-crystal.github.io/GPU-Cluster-Training/)　·　**仓库**：[GitHub 仓库](https://github.com/ai-crystal/GPU-Cluster-Training)

## 分册

| 册 | 书名 | 一句话 | 页数 | 在线阅读 | PDF |
| --- | --- | --- | ---: | --- | --- |
| 01 | [入门篇](books/intro/README.md) | 从一张卡到一万张卡 | 98 页 | [阅读](books/intro/README.md) | <a href="output/v1-intro.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 02 | [专业篇](books/pro/README.md) | 算力、通信与稳定性 | 236 页 | [阅读](books/pro/README.md) | <a href="output/v2-pro.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |

## 怎么读

- 建议先读入门篇，再按需要翻专业篇。两册各自完整，只读一本也不影响理解。
- 只想建立地图：入门篇讲动机、结构、并行与故障，不推公式。
- 要做性能与稳定性：专业篇讲性能模型、通信账、并行细节与踩坑清单。

## 许可

本系列文字与插图采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可发布，转载请注明作者与出处。书中引用的论文、数据集与模型归各自作者所有。

---

作者：Dr. Dezeming　·　2026
