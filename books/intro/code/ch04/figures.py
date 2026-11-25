# -*- coding: utf-8 -*-
"""第 4 章插图：GPU 内部结构与 roofline。"""
from common import *  # noqa: F401,F403

import numpy as np

FIGURES = ["fig_gpu", "fig_roofline"]


def fig_gpu():
    fig, ax = canvas(16.0, 0.52, xlim=(0, 100), ylim=(0, 100))

    box(ax, 1, 6, 72, 88, "", fc="#fbfcfd", ec=INK, lw=1.0)
    label(ax, 3.5, 90, "一张 H100", fs=8.6, ha="left")

    for r in range(6):
        for c in range(9):
            box(ax, 4.5 + c * 7.2, 30 + r * 9.2, 6.0, 7.4, "", fc=BLUE_L,
                ec=BLUE, lw=0.7, radius=0.5)
    label(ax, 37, 26, "132 个 SM，每个 SM 有 4 个 Tensor Core", fs=7.6, color=BLUE)

    box(ax, 4.5, 17, 64, 6.2, "L2 缓存　50 MB", fc=PURPLE_L, ec=PURPLE, fs=7.4)
    box(ax, 4.5, 8.2, 64, 6.2, "HBM3　80 GB　3.35 TB/s", fc=ORANGE_L, ec=ORANGE, fs=7.4)

    box(ax, 76, 72, 22, 13, "算力\n989 TFLOPS", fc=GREEN_L, ec=GREEN, fs=7.6)
    box(ax, 76, 54, 22, 13, "NVLink\n900 GB/s", fc=GREEN_L, ec=GREEN, fs=7.6)
    box(ax, 76, 36, 22, 13, "PCIe 5.0\n64 GB/s", fc="#f2f4f6", ec=MUTED, fs=7.6)
    box(ax, 76, 18, 22, 13, "功耗\n700 W", fc=RED_L, ec=RED, fs=7.6)

    for y in (78.5, 60.5, 42.5, 24.5):
        arrow(ax, (73.3, y), (75.7, y), color=FAINT, lw=0.9, ms=5)

    note(ax, 1, 1.5, "数据从 HBM 经 L2 进入 SM，算完再写回。越靠近计算单元，容量越小、带宽越高。",
         fs=7.4, ha="left")
    save(fig, "fig04-01-gpu.png")


def fig_roofline():
    NL = chr(10)
    fig, ax = chart(15.4, 8.4)
    ai = np.logspace(-0.5, 3.4, 300)
    bw = 3.35e12
    peak = 989e12
    perf = np.minimum(ai * bw, peak)
    ax.plot(ai, perf / 1e12, color=BLUE, lw=1.8, zorder=3)

    ridge = peak / bw
    ax.axvline(ridge, color=MUTED, lw=0.8, ls=":", zorder=2)
    ax.plot([ridge], [peak / 1e12], "o", color=ORANGE, ms=5, zorder=5)
    ax.annotate(NL.join(["拐点约 295 FLOP/字节",
                         "989 TFLOPS 与 3.35 TB/s",
                         "在这里正好匹配"]),
                xy=(ridge, peak / 1e12), xytext=(430, 70),
                fontsize=7.4, color=ORANGE, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.8,
                                connectionstyle="arc3,rad=0.18"))

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.3, 2500)
    ax.set_ylim(0.85, 2600)
    ax.set_xlabel("算术强度（FLOP / 字节）", fontsize=8.2)
    ax.set_ylabel("可达到的算力（TFLOPS）", fontsize=8.2, labelpad=6)
    ax.text(0.45, 1700, "算力受限：再提高算术强度也不会更快", fontsize=7.6,
            color=MUTED, ha="left", va="center")
    ax.text(0.45, 1.02, "带宽受限：算力随算术强度线性增长", fontsize=7.6,
            color=MUTED, ha="left", va="bottom")
    anote(ax, 0.01, -0.15, "按 H100 SXM 的 BF16 峰值 989 TFLOPS 与 HBM3 带宽 3.35 TB/s 绘制，斜线为带宽上限。",
          fs=7.0, va="top")
    save(fig, "fig04-02-roofline.png")
