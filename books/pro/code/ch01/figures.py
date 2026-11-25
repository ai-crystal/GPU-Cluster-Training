# -*- coding: utf-8 -*-
"""第 1 章插图：一个 SM 的资源布局。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_sm"]


def fig_sm():
    fig, ax = canvas(16.0, 0.60, xlim=(0, 100), ylim=(0, 100))

    # 外框：一个 SM
    box(ax, 1.5, 6, 61, 80, "", fc="#fbfcfd", ec=INK, lw=1.0)
    label(ax, 3.2, 90, "一个 SM（Streaming Multiprocessor）", fs=8.4, ha="left")

    # 四个处理分区，每个分区各有自己的调度器、寄存器堆、Tensor Core
    px = [4.5, 19.0, 33.5, 48.0]
    for i, x in enumerate(px):
        box(ax, x, 70, 12.4, 9, "warp 调度器", fc=GREEN_L, ec=GREEN, fs=6.6)
        box(ax, x, 50, 12.4, 17, "寄存器堆\n64K × 32 bit", fc=BLUE_L, ec=BLUE, fs=6.6)
        box(ax, x, 36, 12.4, 11, "Tensor Core", fc=ORANGE_L, ec=ORANGE, fs=6.6)
        box(ax, x, 24, 12.4, 9, "CUDA 核心", fc="#f2f4f6", ec=MUTED, fs=6.4)
        if i:
            ax.plot([x - 1.0, x - 1.0], [24, 79], color=FAINT, lw=0.6, ls=(0, (2, 2)),
                    zorder=1)

    # 共享内存
    box(ax, 4.5, 9, 55.9, 12, "共享内存 / L1　228 KB（可按需分割）", fc=PURPLE_L,
        ec=PURPLE, fs=7.2)

    # 右侧三块说明
    box(ax, 66, 56, 33, 24, "", fc="#f8fafb", ec=MUTED, lw=0.9)
    label(ax, 82.5, 76, "每个 SM 同时驻留多个 warp", fs=7.4)
    label(ax, 82.5, 70.6, "最多 64 个，每分区 16 个", fs=6.8, color=MUTED)
    for k in range(4):
        ax.add_patch(Rectangle((70.0 + k * 6.6, 59.0), 5.4, 3.2, fc=GREEN_L,
                               ec=GREEN, lw=0.6, zorder=3))
    arrow(ax, (65.6, 74), (63.4, 74.4), color=GREEN, lw=0.9, ms=6)

    box(ax, 66, 32, 33, 20, "寄存器总量固定\nwarp 越多，每个 warp\n能分到的寄存器越少",
        fc="white", ec=MUTED, lw=0.9, fs=7.0, color=INK)
    arrow(ax, (65.6, 46), (62.9, 59), color=MUTED, lw=0.8, ms=5)

    box(ax, 66, 9, 33, 18, "同一时刻只有一个 warp\n真正在执行，其余都在等",
        fc="white", ec=MUTED, lw=0.9, fs=7.0, color=INK)
    arrow(ax, (65.6, 22), (62.9, 41), color=MUTED, lw=0.8, ms=5)

    note(ax, 1.5, 2.0,
         "访存要几百个周期。一个 warp 发出访存指令后就被挂起，调度器立刻切到另一个就绪的 warp——"
         "这段延迟被别人的执行填满了。",
         fs=7.0, ha="left")
    save(fig, "fig01-01-sm.png")
