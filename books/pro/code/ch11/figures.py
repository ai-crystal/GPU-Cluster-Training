# -*- coding: utf-8 -*-
"""第 11 章插图：张量并行的通信量随并行度与序列长度的变化。"""
from common import *  # noqa: F401,F403

import numpy as np

FIGURES = ["fig_tp_comm"]


def fig_tp_comm():
    b, h = 1, 8192
    fig, ax = chart(15.6, 8.2)

    tp = np.array([1, 2, 4, 8, 16, 32, 64], float)
    curves = ((2048, BLUE, "s = 2048", 1.55),
              (8192, GREEN, "s = 8192", 3.1),
              (32768, ORANGE, "s = 32768", 6.1))

    for s, color, name, ty in curves:
        # 每层 all-reduce：收发合计 2·b·s·h 个元素，bf16 每元素 2 字节，
        # 每卡实际搬运量按环状 all-reduce 的 (TP-1)/TP 折算。
        mb = 2 * b * s * h * 2 * (tp - 1) / tp / 1e6
        ax.plot(tp, mb, color=color, lw=1.7, marker="o", ms=3.6, zorder=3,
                clip_on=False)
        ax.text(70, mb[-1], name, color=color, fontsize=7.8,
                ha="left", va="center")

    ax.set_xscale("log", base=2)
    ax.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax.set_xticklabels(["1", "2", "4", "8", "16", "32", "64"])
    ax.set_xlim(0.9, 150)
    ax.set_ylim(0, 1160)
    ax.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax.set_xlabel("张量并行度 TP", fontsize=8.2)
    ax.set_ylabel("每层每卡 all-reduce 搬运量（MB，bf16）", fontsize=8.2, labelpad=5)

    # 渐近线：TP 很大时的上限 2·b·s·h·2 字节
    for s, color, _, _ in curves:
        ceil = 2 * b * s * h * 2 / 1e6
        ax.plot([20, 48], [ceil, ceil], color=color, lw=0.7, ls=(0, (2, 3)),
                alpha=0.75, zorder=2)

    ax.annotate("TP=8 时已到上限的 87.5%，\n再加大 TP 几乎不再增加，\n但也绝不会下降",
                xy=(8, 2 * b * 8192 * h * 2 * 7 / 8 / 1e6), xytext=(12.5, 480),
                fontsize=7.4, color=INK, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7,
                                connectionstyle="arc3,rad=-0.2"))

    anote(ax, 0.015, -0.155,
          "按公式估算：每层 all-reduce 收发合计 2·b·s·h 个元素，bf16 每元素 2 字节，"
          "每卡搬运量再乘 (TP−1)/TP；取 b=1、h=8192。虚线为该 TP 下的上限。",
          fs=7.0, va="top")
    save(fig, "fig11-01-tpcomm.png")
