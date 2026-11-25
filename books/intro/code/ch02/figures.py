# -*- coding: utf-8 -*-
"""第 2 章插图：显存账本与精度带来的容量变化。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_ledger", "fig_precision"]


def fig_ledger():
    fig, ax = canvas(16.0, 0.44, xlim=(0, 100), ylim=(4, 60))
    total = 2800.0
    x0, x1 = 4, 96
    scale = (x1 - x0) / total
    segs = [("权重\n350 GB", 350, BLUE),
            ("梯度\n350 GB", 350, GREEN),
            ("Adam 一阶矩\n700 GB", 700, ORANGE),
            ("Adam 二阶矩\n700 GB", 700, PURPLE),
            ("FP32 主权重\n700 GB", 700, MUTED)]

    x = x0
    for name, val, color in segs:
        w = val * scale
        ax.add_patch(Rectangle((x, 22), w, 20, fc=color, ec="white", lw=1.4, zorder=3))
        ax.text(x + w / 2, 32, name, ha="center", va="center", fontsize=7.4,
                color="white", linespacing=1.5, zorder=4)
        x += w

    bracket(ax, x0, x1, 46, "总计约 2800 GB，按 1750 亿参数、每参数 16 字节估算", fs=7.6, up=2.2)
    note(ax, x0, 15, "权重和梯度用 2 字节，Adam 的两份状态和 FP32 主权重各用 4 字节。\n"
                     "这笔账还没算激活值，也没算反向传播需要的临时缓冲区。",
         fs=7.4, ha="left")
    save(fig, "fig02-01-memory-ledger.png")


def fig_precision():
    fig, ax = chart(15.4, 7.6)
    names = ["FP32 权重\n4 字节/参数", "BF16 权重\n2 字节/参数", "FP8 权重\n1 字节/参数"]
    gb = [700, 350, 175]
    bars(ax, names, gb, colors=[MUTED, BLUE, ORANGE], width=0.5,
         fmt="{:,.0f} GB", fs=8.0, ylim=(0, 820))
    ax.axhline(80, color=RED, lw=1.0, ls="--", zorder=4)
    ax.text(-0.42, 98, "单张 H100 的 80 GB", ha="left", va="bottom",
            fontsize=7.6, color=RED)
    ax.set_ylabel("仅权重所需显存（GB）", fontsize=8.2, labelpad=8)
    ax.grid(axis="x", visible=False)
    anote(ax, 0.01, -0.16, "以 1750 亿参数为例。精度降低只改变存储宽度，不改变参数量。\n"
                           "权重从 FP32 换成 BF16，容量需求直接减半，再换成 FP8 又减半，但数值范围和精度也随之收紧。",
          fs=7.0, va="top")
    save(fig, "fig02-02-precision.png")
