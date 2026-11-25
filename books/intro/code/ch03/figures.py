# -*- coding: utf-8 -*-
"""第 3 章插图：机器层级与节点内的三种连接方式。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_hierarchy", "fig_nvlink"]


def fig_hierarchy():
    fig, ax = canvas(16.0, 0.5, xlim=(0, 100), ylim=(0, 100))

    # 单卡
    box(ax, 2, 40, 16, 26, "一张 GPU\n80 GB 显存\n700 W", fc=BLUE_L, ec=BLUE, fs=8.4)

    # 节点（8 卡）
    box(ax, 23, 26, 20, 50, "", fc="#f8fafb", ec=MUTED, lw=0.9)
    for i in range(4):
        box(ax, 25 + i * 4.3, 52, 3.3, 18, "G", fc=BLUE_L, ec=BLUE, fs=6.2, radius=0.5)
        box(ax, 25 + i * 4.3, 30, 3.3, 18, "G", fc=BLUE_L, ec=BLUE, fs=6.2, radius=0.5)

    # 机架（32 节点）
    box(ax, 48, 20, 20, 56, "", fc="#f8fafb", ec=MUTED, lw=0.9)
    for r in range(4):
        for c in range(4):
            box(ax, 50 + c * 4.4, 22 + r * 13.2, 3.4, 11.4, "", fc=BLUE_L,
                ec=BLUE, lw=0.7, radius=0.4)

    # 集群（128 机架）
    box(ax, 73, 10, 24, 66, "", fc="#f8fafb", ec=MUTED, lw=0.9)
    for r in range(4):
        for c in range(4):
            box(ax, 75.5 + c * 5.2, 12 + r * 15.2, 4.2, 13.0, "", fc=BLUE_L,
                ec=BLUE, lw=0.7, radius=0.4)

    arrow(ax, (18.3, 53), (22.7, 53), color=INK, ms=9)
    arrow(ax, (43.3, 53), (47.7, 53), color=INK, ms=9)
    arrow(ax, (68.3, 53), (72.7, 53), color=INK, ms=9)

    label(ax, 11, 74, "单卡", fs=8.6, color=MUTED)
    label(ax, 33, 80, "一台服务器 · 8 卡", fs=8.4, color=INK)
    label(ax, 58, 80, "一个机架 · 32 台", fs=8.4, color=INK)
    label(ax, 85, 80, "一个集群 · 128 柜", fs=8.4, color=INK)

    note(ax, 2, 4, "格数只是示意。卡数每往上一层乘一次：8 卡一台，32 台一柜，128 柜一群。\n"
                   "万卡集群大致是 1250 台服务器、40 个机架；Llama 3 训练用的 16384 张卡约合两千台服务器。",
         fs=7.4, ha="left")
    save(fig, "fig03-01-hierarchy.png")


def fig_nvlink():
    fig, axes = plt.subplots(1, 3, figsize=(16.0 / 2.54, 5.2 / 2.54))
    for ax in axes:
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")
    titles = ["PCIe 连接", "NVLink 加 PCIe", "NVSwitch 全互联"]
    for ax, t in zip(axes, titles):
        ax.text(50, 92, t, ha="center", fontsize=8.4, color=INK)
        for i in range(4):
            box(ax, 6 + i * 23, 58, 16, 15, "GPU", fc=BLUE_L, ec=BLUE, fs=7.0, radius=0.8)
            box(ax, 6 + i * 23, 20, 16, 13, "CPU", fc="#f2f4f6", ec=MUTED, fs=6.4, radius=0.8)

    ax = axes[0]
    for i in range(4):
        ax.plot([14 + i * 23, 14 + i * 23], [58, 33], color=MUTED, lw=1.0)
    ax.text(50, 8, "跨卡流量都要绕经 CPU 与 PCIe 交换机", ha="center", fontsize=6.6, color=MUTED)

    ax = axes[1]
    for i in range(4):
        ax.plot([14 + i * 23, 14 + i * 23], [58, 33], color=MUTED, lw=1.0)
    for i in range(3):
        x1, x2 = 14 + i * 23, 14 + (i + 1) * 23
        ax.plot([x1, x1], [73, 80], color=GREEN, lw=1.2)
        ax.plot([x2, x2], [73, 80], color=GREEN, lw=1.2)
        ax.plot([x1, x2], [80, 80], color=GREEN, lw=1.2)
    ax.text(50, 8, "相邻卡直连，跨组仍要走 PCIe", ha="center", fontsize=6.6, color=MUTED)

    ax = axes[2]
    box(ax, 30, 39, 40, 8, "NVSwitch", fc=GREEN_L, ec=GREEN, fs=6.8, radius=0.8)
    for i in range(4):
        x = 14 + i * 23
        ax.plot([x, 36 + i * 9.3], [58, 47], color=GREEN, lw=1.0)
    ax.text(50, 8, "任意两张卡之间都是全带宽", ha="center", fontsize=6.6, color=MUTED)

    save(fig, "fig03-02-links.png")
