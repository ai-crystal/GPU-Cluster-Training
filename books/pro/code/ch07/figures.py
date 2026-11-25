# -*- coding: utf-8 -*-
"""第 7 章插图：ring 与 tree 两种集合通信算法的时间曲线。"""
from common import *  # noqa: F401,F403

import numpy as np

FIGURES = ["fig_algo"]

N = 64            # 卡数
ALPHA = 10e-6     # 单跳延迟 10 us
BW = 50e9         # 单链路 400 Gb/s = 50 GB/s


def fig_algo():
    fig, ax = chart(15.4, 8.6)

    S = np.logspace(3, 9, 400)                      # 1 KB ~ 1 GB
    t_ring = 2 * (N - 1) * (ALPHA + S / (N * BW))
    t_tree = 2 * np.log2(N) * (ALPHA + S / BW)

    ax.plot(S / 1e6, t_ring * 1e3, color=BLUE, lw=1.8, zorder=3)
    ax.plot(S / 1e6, t_tree * 1e3, color=ORANGE, lw=1.8, zorder=3)

    ax.text(0.004, 1.55, "ring", color=BLUE, fontsize=8.0, ha="left", va="bottom")
    ax.text(0.004, 0.072, "tree", color=ORANGE, fontsize=8.0, ha="left", va="bottom")

    # 交叉点
    denom = (2 * np.log2(N) / BW - 2 * (N - 1) / (N * BW))
    num = 2 * (N - 1) * ALPHA - 2 * np.log2(N) * ALPHA
    xs = num / denom
    ys = 2 * (N - 1) * (ALPHA + xs / (N * BW)) * 1e3
    ax.plot([xs / 1e6], [ys], marker="o", ms=5.5, color=GREEN, zorder=6)
    ax.annotate("交叉点约 5.7 MB\n更小的消息用 tree，更大的用 ring",
                xy=(xs / 1e6, ys), xytext=(0.28, 95),
                fontsize=7.2, color=GREEN, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=0.8,
                                connectionstyle="arc3,rad=-0.2"))
    ax.plot([xs / 1e6] * 2, [0.03, ys], color=GREEN, lw=0.7, ls=":", zorder=2)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.001, 1000)
    ax.set_ylim(0.03, 3e3)
    ax.set_xlabel("消息大小（MB）", fontsize=8.2)
    ax.set_ylabel("一次 64 卡 all-reduce 的耗时（ms）", fontsize=8.2, labelpad=6)

    ax.text(0.0045, 0.30, "小消息：延迟主导\n每跳约 10 μs，ring 要绕 63 跳",
            fontsize=6.8, color=MUTED, ha="left", va="bottom")
    ax.text(60, 700, "大消息：带宽主导\nring 每卡只搬 2S，tree 要搬 12S",
            fontsize=6.8, color=MUTED, ha="right", va="top")

    anote(ax, 0.01, -0.17,
          "按公式估算，非实测：64 卡、单链路 400 Gb/s（50 GB/s）、单跳延迟 10 μs；"
          "ring ≈ 2(n−1)(α+S/nB)，tree ≈ 2log₂n(α+S/B)。",
          fs=6.8, va="top")
    save(fig, "fig07-01-algo.png")
