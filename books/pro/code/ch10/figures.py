# -*- coding: utf-8 -*-
"""第 10 章插图：FSDP 一次前向与反向的参数搬运与释放。"""
from common import *  # noqa: F401,F403

from matplotlib.patches import Rectangle

FIGURES = ["fig_fsdp"]

T_MAX = 96.0


def fig_fsdp():
    fig, ax = canvas(16.0, 0.66, xlim=(0, 100), ylim=(0, 100))

    def X(t):
        return 14.0 + t * (82.0 / T_MAX)

    def seg(t0, t1, y, h, color, text="", tcol="white", fs=6.2):
        ax.add_patch(Rectangle((X(t0), y), X(t1) - X(t0), h, fc=color, ec="white",
                               lw=0.8, zorder=3))
        if text:
            ax.text((X(t0) + X(t1)) / 2, y + h / 2, text, ha="center", va="center",
                    fontsize=fs, color=tcol, zorder=4)

    Y_AG, Y_C, Y_RS, H = 78.0, 62.0, 46.0, 10.0

    label(ax, 12.5, Y_AG + H / 2, "参数 all-gather", fs=7.0, ha="right")
    label(ax, 12.5, Y_C + H / 2, "计算", fs=7.0, ha="right")
    label(ax, 12.5, Y_RS + H / 2, "梯度 reduce-scatter", fs=7.0, ha="right")

    # 前向
    seg(0, 6, Y_AG, H, BLUE)
    seg(6, 20, Y_C, H, GREEN_L, "层 1 前向", GREEN)
    seg(20, 26, Y_AG, H, BLUE)
    seg(26, 40, Y_C, H, GREEN_L, "层 2 前向", GREEN)

    # 反向
    seg(40, 46, Y_AG, H, BLUE)
    seg(46, 60, Y_C, H, "#e6edf5", "层 2 反传", BLUE)
    seg(60, 68, Y_RS, H, ORANGE, "RS", "white")
    seg(68, 74, Y_AG, H, BLUE)
    seg(74, 88, Y_C, H, "#e6edf5", "层 1 反传", BLUE)
    seg(88, 96, Y_RS, H, ORANGE, "RS", "white")

    # 显存占用
    Y_M0, Y_M1 = 26.0, 38.0
    xs, ys = [], []
    for t0, t1 in ((0, 20), (20, 40), (40, 60), (68, 88)):
        xs += [X(t0), X(t0), X(t1), X(t1)]
        ys += [Y_M0, Y_M1, Y_M1, Y_M0]
    ax.plot(xs, ys, color=PURPLE, lw=1.1, zorder=4)
    ax.fill_between(xs, Y_M0, ys, color=PURPLE_L, zorder=2)
    ax.plot([X(0), X(96)], [Y_M0, Y_M0], color=FAINT, lw=0.7, ls=(0, (2, 2)), zorder=1)

    label(ax, 12.5, (Y_M0 + Y_M1) / 2, "显存里的参数", fs=7.0, ha="right")
    label(ax, X(33), Y_M1 + 1.6, "该层全量（临时）", fs=6.2, color=PURPLE, va="bottom")

    # 释放标注
    label(ax, X(64), 22.0, "层算完就释放，只剩 1/N 分片", fs=6.2, color=PURPLE, ha="center")
    arrow(ax, (X(64), 23.6), (X(64), 25.6), color=PURPLE, lw=0.7, ms=4.5)

    # 分隔：前向 / 反向
    ax.plot([X(40), X(40)], [44.0, 92.0], color=MUTED, lw=0.7, ls=(0, (4, 3)))
    label(ax, X(40) - 1.0, 92.0, "前向", fs=6.8, color=MUTED, ha="right", va="bottom")
    label(ax, X(40) + 1.0, 92.0, "反向", fs=6.8, color=MUTED, ha="left", va="bottom")

    # 说明
    arrow(ax, (X(3), 92.6), (X(3), 88.6), color=BLUE, lw=0.7, ms=4.5)
    label(ax, X(3), 93.4, "只临时收这一层", fs=6.2, color=BLUE, va="bottom")

    label(ax, X(64), 43.4, "梯度切片发出去", fs=6.2, color=ORANGE, ha="center")
    arrow(ax, (X(64), 44.2), (X(64), 45.6), color=ORANGE, lw=0.7, ms=4.5)

    note(ax, 1.5, 13.0,
         "前向：收一层完整参数 → 算这一层 → 立刻放掉，显存里始终只有一层是全量的。",
         fs=6.8, ha="left")
    note(ax, 1.5, 7.5,
         "反向：把这一层再收一遍，算完梯度直接 reduce-scatter 发走，所以反向比前向多一次 all-gather。",
         fs=6.8, ha="left")
    save(fig, "fig10-01-fsdp.png")
