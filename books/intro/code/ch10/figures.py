# -*- coding: utf-8 -*-
"""第 10 章插图：ring all-reduce 的分块累加、rail-optimized 拓扑。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_ring", "fig_rail"]


def _ring_row(ax, y, greens, title, fs=7.0):
    xs = [8, 30, 52, 74]
    for i, x in enumerate(xs):
        box(ax, x, y, 16, 12, "", fc="#fbfcfd", ec=BLUE, lw=0.9)
        ax.text(x + 8, y + 13.4, f"卡 {i + 1}", ha="center", fontsize=6.6, color=MUTED)
        for c in range(4):
            if greens and (greens[i] == "all" or greens[i] == c):
                color = GREEN
            else:
                color = "#e4e7ea"
            ax.add_patch(Rectangle((x + 1.4 + c * 3.6, y + 3.4), 3.0, 5.2,
                                   fc=color, ec="white", lw=0.6, zorder=4))
    for i in range(3):
        arrow(ax, (xs[i] + 16.4, y + 6), (xs[i + 1] - 0.4, y + 6), color=ORANGE, ms=6, lw=0.8)
    ax.plot([xs[3] + 8, xs[3] + 8, xs[0] + 8, xs[0] + 8],
            [y - 2.0, y - 4.6, y - 4.6, y - 2.0], color=ORANGE, lw=0.8, ls="--")
    arrow(ax, (xs[0] + 8, y - 4.6), (xs[0] + 8, y - 1.6), color=ORANGE, ms=5, lw=0.8)
    ax.text(50, y - 6.2, title, ha="center", va="top", fontsize=fs, color=MUTED)


def fig_ring():
    fig, ax = canvas(16.0, 0.62, xlim=(0, 100), ylim=(0, 100))

    _ring_row(ax, 84, [], "① 每张卡持有全部参数的四个分块，颜色表示来自哪张卡")
    _ring_row(ax, 54, [0, 1, 2, 3], "② reduce-scatter：每张卡把自己的一块发给下一张，逐块累加")
    _ring_row(ax, 24, ["all"] * 4, "③ all-gather：完成的块再传一圈，每张卡都有完整梯度")

    note(ax, 2, 6, "每一步，每张卡同时发出一个块、接收一个块，双向带宽都被用满。",
         fs=7.4, ha="left")
    save(fig, "fig10-01-ring.png")


def fig_rail():
    fig, ax = canvas(16.0, 0.5, xlim=(0, 100), ylim=(0, 100))

    nodes_y = [72, 52, 32]
    for i, y in enumerate(nodes_y):
        box(ax, 2, y, 24, 14, "", fc="#f8fafb", ec=MUTED, lw=0.9)
        ax.text(13, y + 7, f"节点 {i + 1}", ha="center", va="center", fontsize=7.2)
        for r in range(4):
            ax.add_patch(Circle((25.2, y + 2.6 + r * 3.0), 0.9, fc=BLUE, ec="none", zorder=5))

    leaves_y = [78, 64, 50, 36]
    for r, y in enumerate(leaves_y):
        box(ax, 48, y - 4, 20, 8, f"Leaf {r}", fc=GREEN_L, ec=GREEN, fs=7.0)
        for i, ny in enumerate(nodes_y):
            ax.plot([26.1, 47.7], [ny + 2.6 + r * 3.0, y],
                    color=BLUE if i == 0 else FAINT, lw=0.7, zorder=2)

    box(ax, 78, 44, 18, 28, "Spine\n交换机", fc="#f2f4f6", ec=MUTED, fs=7.4)
    for y in leaves_y:
        ax.plot([68.2, 77.8], [y, 58], color=MUTED, lw=0.8)

    note(ax, 2, 24, "每台机器的第 r 张网卡固定接到第 r 台 leaf 交换机，这条路径叫一条 rail。",
         fs=7.4, ha="left")
    note(ax, 2, 15, "同一 rail 上的流量只经过一级交换，不同 rail 之间才需要走 spine。",
         fs=7.4, ha="left", color=GREEN)
    note(ax, 2, 6, "这样排布之后，一个 TP 组或 PP 组的通信可以被约束在少数几条 rail 上，减少拥塞。",
         fs=7.4, ha="left", color=ORANGE)
    save(fig, "fig10-02-rail.png")
