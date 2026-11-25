# -*- coding: utf-8 -*-
"""第 16 章插图：激活显存随序列长度的增长（按 Megatron 每层公式估算）。"""
from common import *  # noqa: F401,F403

import numpy as np

FIGURES = ["fig_activation"]

H = 8192        # 隐藏维
A = 64          # 注意力头数（head_dim = 128）
L = 80          # 层数


def act_gb(s, b):
    """每层激活 ≈ s·b·h·(34 + 5·s·a/h) 字节，整模型乘层数。"""
    per_layer = s * b * H * (34 + 5 * s * A / H)
    return per_layer * L / 1e9


def fig_activation():
    fig, ax = chart(15.6, 8.4)

    s = np.logspace(np.log2(1024), np.log2(16384), 200, base=2)
    for b, color in ((1, BLUE), (4, GREEN), (8, ORANGE)):
        y = act_gb(s, b)
        ax.plot(s, y, color=color, lw=1.7, zorder=3)
        yy = act_gb(16384, b)
        ax.text(16900, yy, f"b = {b}", color=color, fontsize=7.6, ha="left",
                va="center")
        ax.plot([16384], [yy], "o", color=color, ms=4, zorder=4, clip_on=False)

    ax.axhline(80, color=RED, lw=0.9, ls=(0, (4, 3)), zorder=2)
    ax.text(2150, 86, "单卡 80 GB", fontsize=7.0, color=RED, ha="left",
            va="bottom")

    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks([1024, 2048, 4096, 8192, 16384])
    ax.set_xticklabels(["1K", "2K", "4K", "8K", "16K"])
    ax.tick_params(which="minor", length=0)
    ax.set_xlim(900, 20500)
    ax.set_ylim(10, 1.2e5)
    ax.set_yticks([10, 100, 1000, 1e4, 1e5])
    ax.set_yticklabels(["10", "100", "1 TB", "10 TB", "100 TB"])
    ax.set_xlabel("序列长度 s（token）", fontsize=8.2)
    ax.set_ylabel("单卡激活显存（GB，bf16）", fontsize=8.2, labelpad=5)

    ax.text(1000, 22000,
            "双对数下斜率≈2：" + chr(10) + "序列翻倍，激活约变四倍",
            fontsize=6.9, color=MUTED, ha="left", va="center")

    ax.annotate("b=1 在 s≈1.1K 就撞到 80 GB，" + chr(10) + "s=2048 时已要 153 GB",
                xy=(1180, 88), xytext=(1250, 20), fontsize=6.9, color=BLUE,
                ha="left", va="bottom",
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.7,
                                connectionstyle="arc3,rad=0.2"))

    anote(ax, 0.0, -0.145,
          "按 Megatron 论文的每层公式估算：每层 s·b·h·(34 + 5·s·a/h) 字节，共 80 层；"
          "取 h=8192、a=64、bf16，"
          "假设不做重算、不做序列并行——三种省显存手段能砍掉的就是这一大块。",
          fs=6.9, va="top")
    save(fig, "fig16-01-activation.png")
