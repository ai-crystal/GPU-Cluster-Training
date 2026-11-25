# -*- coding: utf-8 -*-
"""第 3 章插图：Tensor Core 的数据通路与双缓冲流水。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_mma"]


def fig_mma():
    fig, ax = canvas(16.0, 0.60, xlim=(0, 100), ylim=(0, 94))

    # ---------- 主通路
    box(ax, 1.5, 52, 13, 18, "HBM3\n80 GB", fc=ORANGE_L, ec=ORANGE, fs=7.2)
    box(ax, 19, 52, 12, 18, "L2\n50 MB", fc=GREEN_L, ec=GREEN, fs=7.2)

    box(ax, 35.5, 44, 19, 34, "", fc=PURPLE_L, ec=PURPLE, lw=0.9)
    label(ax, 45, 74.4, "共享内存 228 KB", fs=6.8, color=PURPLE)
    box(ax, 37, 46, 7.6, 23, "buf A\n计算中", fc="white", ec=PURPLE, fs=6.4)
    box(ax, 45.4, 46, 7.6, 23, "buf B\n搬入中", fc="#faf7ff", ec=PURPLE, fs=6.4,
        ls=(0, (3, 2)))

    box(ax, 58.5, 52, 12.5, 18, "寄存器\nldmatrix", fc=BLUE_L, ec=BLUE, fs=6.8)
    box(ax, 75, 52, 11, 18, "Tensor\nCore MMA", fc="white", ec=INK, fs=6.8)
    box(ax, 89.5, 52, 9.5, 18, "FP32\n累加器", fc="white", ec=INK, fs=6.6)

    for x1, x2 in ((14.8, 18.7), (31.3, 35.2), (55.0, 58.2), (71.3, 74.7), (86.3, 89.2)):
        arrow(ax, (x1, 61), (x2, 61), color=INK, lw=0.9, ms=6)

    # TMA 说明
    note(ax, 15.5, 88.5, "TMA 引擎异步把数据从 L2 直接写进共享内存，", fs=6.9, ha="left",
         color=ORANGE)
    note(ax, 15.5, 84.0, "不经过寄存器，也不占用线程的指令发射槽。", fs=6.9, ha="left",
         color=ORANGE)
    arrow(ax, (37.0, 81.0), (40.0, 78.4), color=ORANGE, lw=0.9, ms=5)

    note(ax, 80.5, 43.0, "mma.sync 一条指令完成一次分块矩阵乘加", fs=6.7, ha="center",
         color=MUTED)

    # ---------- 双缓冲时间线
    label(ax, 50, 34.5, "双缓冲：搬下一块的同时，Tensor Core 在算上一块", fs=7.2)
    x0, x1 = 16, 96
    unit = (x1 - x0) / 4
    rows = [(24.0, "TMA 搬入", [("buf A", 0), ("buf B", 1), ("buf A", 2), ("buf B", 3)], BLUE),
            (16.0, "Tensor Core", [("算 A", 0), ("算 B", 1), ("算 A", 2), ("算 B", 3)], GREEN)]

    for y, name, segs, color in rows:
        label(ax, 14.5, y + 3, name, fs=6.8, ha="right")
        for text, k in segs:
            a = x0 + k * unit
            if name == "Tensor Core":
                a += unit * 0.5
                if a + unit > x1 + 0.5:
                    continue
            ax.add_patch(Rectangle((a + 0.6, y), unit - 1.2, 6, fc=color, ec="white",
                                   lw=0.8, zorder=3))
            ax.text(a + unit / 2, y + 3, text, ha="center", va="center", fontsize=6.4,
                    color="white", zorder=4)

    # 一个周期的对齐虚线
    vline(ax, x0 + unit * 0.5, 15.0, 31.5)
    vline(ax, x0 + unit * 1.5, 15.0, 31.5)
    arrow(ax, (x0 - 1.0, 12.0), (x1 + 1.0, 12.0), color=MUTED, lw=0.7, ms=6)
    label(ax, x1 + 2.0, 12.0, "时间", fs=6.8, color=MUTED, ha="left")

    note(ax, 1.5, 5.0,
         "算 A 的时间正好盖住 buf B 的搬入时间。缓冲再深（3～4 级）就能容忍更长的访存抖动。",
         fs=6.9, ha="left")
    save(fig, "fig03-01-mma.png")
