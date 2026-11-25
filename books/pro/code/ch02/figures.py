# -*- coding: utf-8 -*-
"""第 2 章插图：存储层级金字塔与共享内存 bank 冲突。"""
from common import *  # noqa: F401,F403

from matplotlib.patches import Polygon, Rectangle

FIGURES = ["fig_hierarchy", "fig_bank"]


# ---------------------------------------------------------------- 层级金字塔
def _layer(ax, y0, y1, wb, wt, text, fc, ec, fs=7.6):
    cx = 30.0
    ax.add_patch(Polygon([(cx - wb, y0), (cx + wb, y0), (cx + wt, y1), (cx - wt, y1)],
                         closed=True, fc=fc, ec=ec, lw=0.9, zorder=2))
    label(ax, cx, (y0 + y1) / 2, text, fs=fs, z=4)


def fig_hierarchy():
    fig, ax = canvas(16.0, 0.58, xlim=(0, 100), ylim=(0, 72))

    rows = [
        # (y0, y1, 下宽, 上宽, 层内文字, 颜色, 说明行1, 说明行2)
        (50, 64, 11.0, 6.0, "寄存器", BLUE_L, BLUE, "每个线程 255 个 32 位寄存器", "整 SM 约 256 KB，约 20 个周期"),
        (36, 50, 16.0, 11.0, "共享内存", PURPLE_L, PURPLE, "228 KB / SM，软件显式管理", "约 30 个周期"),
        (22, 36, 20.5, 16.0, "L2 缓存", GREEN_L, GREEN, "50 MB，全卡共享", "约 200 个周期 · 芯片内"),
        (6, 22, 26.0, 20.5, "HBM3 显存", ORANGE_L, ORANGE, "80 GB，3.35 TB/s", "约 500 个周期 · 芯片外"),
    ]
    for y0, y1, wb, wt, txt, fc, ec, t1, t2 in rows:
        _layer(ax, y0, y1, wb, wt, txt, fc, ec)

    # 右侧说明：容量 / 带宽 / 延迟
    right_edge = [8.0, 11.0, 16.0, 20.5]
    for (y0, y1, wb, wt, txt, fc, ec, t1, t2), re in zip(rows, right_edge):
        ym = (y0 + y1) / 2
        ax.plot([30 + wt, 62], [ym, ym], color=FAINT, lw=0.6, ls=(0, (2, 2)), zorder=1)
        label(ax, 63.5, ym + 2.0, t1, fs=7.2, ha="left")
        note(ax, 63.5, ym - 2.4, t2, fs=6.9, ha="left")

    # 左侧：容量与带宽方向
    arrow(ax, (3.5, 66), (3.5, 4), color=MUTED, lw=0.9, ms=7)
    label(ax, 2.0, 35, "容量变大", fs=7.0, color=MUTED, rotation=90, ha="center")
    arrow(ax, (98.0, 4), (98.0, 66), color=MUTED, lw=0.9, ms=7)
    label(ax, 94.0, 35, "带宽与延迟", fs=7.0, color=MUTED, rotation=90, ha="center")

    # 芯片内外分割线
    ax.plot([3, 99], [22, 22], color=RED, lw=0.7, ls=(0, (5, 3)), zorder=3)

    note(ax, 3.0, 1.4,
         "每往下一层，容量大约涨一个数量级，带宽降一档，延迟涨几倍——存储层级就是用容量换速度。",
         fs=6.9, ha="left")
    save(fig, "fig02-01-hierarchy.png")


# ---------------------------------------------------------------- bank 冲突
def _banks(ax, x0, w, n=32, y=20, h=12, conflict=0):
    """画 n 个 bank 单元，前 conflict 个标为被访问。"""
    cw = w / n
    for i in range(n):
        hot = i < conflict
        ax.add_patch(Rectangle((x0 + i * cw, y), cw - 0.12, h,
                               fc=ORANGE_L if hot else "#f4f5f7",
                               ec=ORANGE if hot else FAINT, lw=0.6, zorder=2))
    for i in (0, 8, 16, 24, 31):
        label(ax, x0 + (i + 0.5) * cw, y - 2.4, str(i), fs=6.5, color=MUTED)
    return cw


def fig_bank():
    fig, ax = canvas(16.0, 0.62, xlim=(0, 100), ylim=(0, 100))

    # ---- 左：无冲突
    box(ax, 1.5, 4, 45, 88, "", fc="white", ec=FAINT, lw=0.8)
    label(ax, 24, 84, "无冲突：32 个线程落在 32 个 bank", fs=7.4)
    cw = _banks(ax, 4, 40, y=20, h=13, conflict=0)
    for i in range(32):
        cx = 4 + (i + 0.5) * cw
        ax.add_patch(Rectangle((cx - 0.52, 58), 1.04, 1.04, fc=BLUE, ec="none", zorder=4))
        arrow(ax, (cx, 56.5), (cx, 34.0), color=BLUE, lw=0.5, ms=3.2)
    label(ax, 24, 64.0, "线程 0 … 线程 31", fs=6.8, color=MUTED)
    label(ax, 24, 10.5, "一轮并发完成，1 个周期", fs=7.2, color=GREEN)
    label(ax, 24, 5.8, "bank i 恰好服务线程 i", fs=6.8, color=MUTED)

    # ---- 右：4 路冲突
    box(ax, 52.5, 4, 45, 88, "", fc="white", ec=FAINT, lw=0.8)
    label(ax, 75, 84, "4 路冲突：4 个线程挤在同一个 bank", fs=7.4)
    cw = _banks(ax, 55, 40, y=20, h=13, conflict=8)
    for i in range(8):
        cx = 55 + (i + 0.5) * cw
        for r in range(4):
            ax.add_patch(Rectangle((cx - 0.5, 44 + r * 4.4), 1.0, 1.0,
                                   fc=ORANGE, ec="none", zorder=4))
        arrow(ax, (cx, 43.0), (cx, 34.0), color=ORANGE, lw=0.6, ms=3.6)
    label(ax, 70, 64.0, "每个 bank 上排了 4 个线程", fs=6.8, color=ORANGE)
    label(ax, 84, 38.5, "其余 24 个 bank 空闲", fs=6.8, color=MUTED)
    label(ax, 75, 10.5, "被拆成 4 次，4 个周期", fs=7.2, color=RED)
    label(ax, 75, 5.8, "32 个线程只用到 8 个 bank", fs=6.8, color=MUTED)

    note(ax, 1.5, 1.0,
         "步长取成 bank 数的整数倍（如按列访问二维数组）就会出现这种冲突；把数组每行补一个 padding 就能打散。",
         fs=6.8, ha="left")
    save(fig, "fig02-02-bank.png")
