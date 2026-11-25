# -*- coding: utf-8 -*-
"""第 9 章插图：三维并行网格与通信组划分。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_grid", "fig_groups"]


def fig_grid():
    fig, ax = canvas(16.0, 0.5, xlim=(0, 100), ylim=(0, 100))

    # 叠放的三层平面表示 DP 副本
    for k in (2, 1):
        ax.add_patch(Rectangle((16 + k * 5, 16 + k * 4), 46, 46, fc="#fdfefe",
                               ec=FAINT, lw=0.8, zorder=1))
    ax.add_patch(Rectangle((16, 16), 46, 46, fc="white", ec=INK, lw=1.0, zorder=2))

    cols, rows = 16, 8
    cw, chh = 46 / cols, 46 / rows
    for r in range(rows):
        for c in range(cols):
            ax.add_patch(Rectangle((16 + c * cw, 16 + (rows - 1 - r) * chh),
                                   cw * 0.9, chh * 0.9, fc=BLUE, alpha=0.16,
                                   ec="none", zorder=3))

    ax.annotate("", xy=(64, 10), xytext=(16, 10),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.9))
    ax.text(40, 6, "TP = 8（张量并行）", ha="center", fontsize=8.0, color=BLUE)

    ax.annotate("", xy=(11, 64), xytext=(11, 16),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=0.9))
    ax.text(7.5, 40, "PP = 16", ha="center", va="center", rotation=90,
            fontsize=8.0, color=GREEN)

    ax.annotate("", xy=(74, 71), xytext=(62, 62),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.0))
    ax.text(77, 73, "DP = 128\n同一张网格叠 128 份", ha="left", va="center",
            fontsize=7.8, color=ORANGE, linespacing=1.5)

    note(ax, 2, 88, "8 × 16 × 128 = 16384 张卡", fs=9.2, ha="left", color=INK)
    save(fig, "fig09-01-grid.png")


def fig_groups():
    fig, ax = canvas(16.0, 0.5, xlim=(0, 100), ylim=(0, 100))

    for n in range(3):
        x = 6 + n * 31
        box(ax, x, 52, 26, 30, "", fc="#f8fafb", ec=MUTED, lw=0.9)
        for i in range(4):
            box(ax, x + 2 + i * 5.6, 70, 4.6, 9, "G", fc=BLUE_L, ec=BLUE, fs=5.8, radius=0.4)
            box(ax, x + 2 + i * 5.6, 56, 4.6, 9, "G", fc=BLUE_L, ec=BLUE, fs=5.8, radius=0.4)
        ax.text(x + 13, 50, f"节点 {n + 1}", ha="center", va="top", fontsize=7.2, color=MUTED)

    ax.add_patch(Rectangle((7.2, 54.8), 23.6, 25.4, fc="none", ec=ORANGE, lw=1.2, ls="--", zorder=5))
    ax.text(2, 93, "TP 组：节点内 8 卡，走 NVLink", fontsize=7.6, color=ORANGE, ha="left")

    ax.annotate("", xy=(38, 67), xytext=(33, 67),
                arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=1.2))
    ax.annotate("", xy=(69, 67), xytext=(64, 67),
                arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=1.2))
    ax.text(47, 93, "PP 组：相邻节点之间，走网卡", ha="left", fontsize=7.6, color=GREEN)

    ax.annotate("", xy=(6, 40), xytext=(94, 40),
                arrowprops=dict(arrowstyle="<|-|>", color=BLUE, lw=1.2))
    ax.text(50, 35, "DP 组：128 份副本之间，跨机架同步梯度", ha="center",
            fontsize=7.6, color=BLUE)

    note(ax, 2, 22, "同一个编号的卡属于同一个 TP 组；不同节点上相同位置的卡属于同一个 PP 组；\n"
                    "所有副本里编号相同的卡组成一个 DP 组。摆放顺序决定了哪类流量走哪张网。",
         fs=7.4, ha="left")
    note(ax, 2, 8, "把 TP 放在节点内，是因为它的通信最频繁、对延迟最敏感；DP 的流量大但频率低，可以跨机架。",
         fs=7.4, ha="left", color=ORANGE)
    save(fig, "fig09-02-groups.png")
