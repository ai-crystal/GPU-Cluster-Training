# -*- coding: utf-8 -*-
"""第 21 章插图：存储层级与带宽预算。"""
from common import *  # noqa: F401,F403

import math

FIGURES = ["fig_storage"]


def fig_storage():
    fig, ax = canvas(16.0, 0.62)

    # 名称, 典型带宽文本, 容量文本, 带宽数值(GB/s), 颜色
    layers = [
        ("GPU 显存 HBM3", "3 350 GB/s", "80 GB / 卡", 3350, BLUE),
        ("主机内存 DDR5", "400 GB/s", "1–2 TB / 节点", 400, BLUE),
        ("本地 NVMe（RAID 0）", "56 GB/s", "数十 TB / 节点", 56, GREEN),
        ("并行文件系统", "10 GB/s", "PB 级、多租户", 10, ORANGE),
        ("对象存储", "2 GB/s", "近乎无限、冷数据", 2, MUTED),
    ]
    # 每块的高度与底部 y
    h = 11.0
    ys = [82.0, 64.0, 46.0, 28.0, 10.0]

    # 表头
    label(ax, 4.0, 96.6, "层级", fs=7.2, color=MUTED, ha="left")
    label(ax, 36.0, 96.6, "典型带宽（log 尺度，1 GB/s 起）", fs=7.2, color=MUTED, ha="left")


    x0, wmax = 36.0, 38.0
    ref = math.log10(4000.0)
    for (name, bw, cap, val, color), y in zip(layers, ys):
        label(ax, 4.0, y + 7.0, name, fs=8.2, color=INK, ha="left")
        label(ax, 4.0, y + 3.0, bw, fs=7.4, color=color, ha="left", weight="bold")
        label(ax, 18.5, y + 3.0, cap, fs=6.7, color=MUTED, ha="left")
        w = wmax * math.log10(val) / ref
        ax.add_patch(Rectangle((x0, y + 2.4), w, 6.0, fc=color, ec="none",
                               alpha=0.85, zorder=3))
        # 带宽数量级的对照刻度
        ax.plot([x0, x0], [y + 1.6, y + 9.4], color=MUTED, lw=0.8, zorder=2)

    # 层间互连：向上为读取路径
    links = [
        (9.5, "经网络与缓存层  ≈ 10 GB/s"),
        (27.5, "客户端挂载 / 网络  ≈ 10 GB/s"),
        (45.5, "PCIe Gen5 ×16  ≈ 64 GB/s"),
        (63.5, "NVLink-C2C 或 PCIe  ≈ 64–900 GB/s"),
    ]
    for y, text in links:
        arrow(ax, (28.0, y - 2.6), (28.0, y + 2.6), color=MUTED, lw=0.8, ms=6)
        label(ax, 30.0, y, text, fs=6.5, color=MUTED, ha="left")

    # 读多写少
    box(ax, 79.0, 58.0, 20.0, 30.0, fc=ORANGE_L, ec=ORANGE, lw=0.9, radius=1.2)
    label(ax, 89.0, 82.0, "读多写少", fs=9.2, color=ORANGE, weight="bold")
    label(ax, 89.0, 70.0,
          "训练 IO 以对数据集的\n顺序大块读为主；\n写只发生在周期性的\n检查点与日志上。",
          fs=6.6, color=ORANGE)

    label(ax, 79.0, 48.0,
          "分层的理由不是技术炫耀，\n而是每一级的单价差两个数量级；\n"
          "把热数据放在贵的地方，\n把冷数据放在便宜的地方。",
          fs=6.6, color=MUTED, ha="left", va="top")

    label(ax, 4.0, 4.4,
          "越靠上越靠近计算：容量小、带宽高、单价贵；越靠下容量越大、带宽越低，可被整个集群共享。",
          fs=6.8, color=MUTED, ha="left")

    save(fig, "fig21-01-storage.png")
