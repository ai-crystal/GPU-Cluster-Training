# -*- coding: utf-8 -*-
"""第 4 章插图：几套大模型的实测 MFU。"""
from common import *  # noqa: F401,F403

import numpy as np

FIGURES = ["fig_mfu"]


def fig_mfu():
    fig, ax = chart(15.6, 8.0)

    names = ["PaLM\n540B", "Megatron\n1T", "MegaScale\n175B", "Llama 3\n405B"]
    vals = [46.2, 52.0, 55.2, None]
    lo, hi, mid = 38.0, 43.0, 40.5
    colors = [BLUE, BLUE, GREEN, ORANGE]

    xs = np.arange(4)
    for i in range(3):
        ax.bar(xs[i], vals[i], width=0.56, color=colors[i], edgecolor="none", zorder=3)
        ax.annotate(f"{vals[i]:.1f}%", (xs[i], vals[i]), ha="center", va="bottom",
                    fontsize=7.6, color=INK, xytext=(0, 3), textcoords="offset points")

    # Llama 3 的区间条
    ax.bar(xs[3], hi - lo, bottom=lo, width=0.20, color=ORANGE, edgecolor="none",
           alpha=0.45, zorder=3)
    ax.plot([xs[3]], [mid], marker="o", ms=5, color=ORANGE, zorder=5)
    ax.plot([xs[3] - 0.22, xs[3] + 0.22], [lo, lo], color=ORANGE, lw=1.2, zorder=5)
    ax.plot([xs[3] - 0.22, xs[3] + 0.22], [hi, hi], color=ORANGE, lw=1.2, zorder=5)
    ax.annotate("38%–43%", (xs[3], hi), ha="center", va="bottom", fontsize=7.4,
                color=ORANGE, xytext=(0, 3), textcoords="offset points")

    ax.set_ylim(0, 66)
    ax.set_xlim(-0.62, 3.62)
    ax.set_ylabel("MFU（%）", fontsize=8.2, labelpad=6)
    ax.set_xticks(xs)
    ax.set_xticklabels(names, fontsize=8.0, linespacing=1.4)
    ax.tick_params(axis="x", length=0, pad=4)

    anote(ax, 0.01, -0.19,
          "数据来源：PaLM（2022）、Megatron-LM 1T 训练报告、MegaScale（2024）、Llama 3 技术报告（2024，\n"
          "只给区间 38%–43%；区间条按上下限画，圆点为区间中点）",
          fs=6.6, va="top")
    save(fig, "fig04-01-mfu.png")
