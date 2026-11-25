# -*- coding: utf-8 -*-
"""第 6 章插图：一个训练步里计算与通信的时间线。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_step"]


def fig_step():
    fig, ax = canvas(16.0, 0.44, xlim=(0, 100), ylim=(0, 76))

    x0, x1 = 12, 97
    label(ax, x0 - 1.5, 58, "计算", fs=8.0, ha="right")
    segs = [("前向", 0.00, 0.30), ("反向", 0.30, 0.72), ("参数更新", 0.75, 0.90)]
    for text, a, b in segs:
        ax.add_patch(Rectangle((x0 + (x1 - x0) * a, 54), (x1 - x0) * (b - a), 11,
                               fc="#e8eff7", ec=BLUE, lw=0.9, zorder=3))
        ax.text(x0 + (x1 - x0) * (a + b) / 2, 59.5, text, ha="center", va="center",
                fontsize=7.8, color=BLUE, zorder=4)

    label(ax, x0 - 1.5, 40, "通信", fs=8.0, ha="right")
    for i in range(6):
        a = 0.30 + i * 0.065
        ax.add_patch(Rectangle((x0 + (x1 - x0) * a, 36), (x1 - x0) * 0.045, 9,
                               fc=ORANGE_L, ec=ORANGE, lw=0.8, zorder=3))
    ax.text(x0 + (x1 - x0) * 0.62, 31.5, "梯度桶逐个 all-reduce，与反向计算重叠",
            ha="center", fontsize=7.4, color=ORANGE)

    ax.annotate("", xy=(x1, 16), xytext=(x0, 16),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8))
    ax.text(x1, 12, "时间", ha="right", fontsize=7.4, color=MUTED)

    bracket(ax, x0, x0 + (x1 - x0) * 0.30, 68, "大部分时间花在前向和反向的矩阵乘上", fs=7.2, up=2.0)

    note(ax, 1, 3, "如果通信不能与计算重叠，一次梯度同步就会把整个训练步拉长。工程上把梯度按参数切成桶，\n"
                   "某一层的反向算完就立刻发这一层的归约，让网络和计算同时忙。",
         fs=7.4, ha="left")
    save(fig, "fig06-01-step.png")
