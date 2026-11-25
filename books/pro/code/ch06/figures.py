# -*- coding: utf-8 -*-
"""第 6 章插图：Fat-tree 与 rail-optimized 两种组网。"""
from common import *  # noqa: F401,F403

from matplotlib.patches import Rectangle

FIGURES = ["fig_topo"]


def _fat_tree(ax):
    label(ax, 1.5, 94, "Fat-tree：谁跟谁通信都最多三跳", fs=7.8, ha="left")

    # spine
    for i, x in enumerate((7.0, 25.0)):
        box(ax, x, 76, 15, 9, f"Spine {i + 1}", fc="#f2f4f6", ec=MUTED, fs=7.0)

    # leaf
    lx = [2.5, 14.0, 25.5, 37.0]
    for i, x in enumerate(lx):
        box(ax, x, 56, 9.5, 7, f"Leaf {i + 1}", fc=GREEN_L, ec=GREEN, fs=6.6)

    # 节点
    for i, x in enumerate(lx):
        box(ax, x, 24, 9.5, 15, "", fc="#f8fafb", ec=MUTED, fs=6.6)
        label(ax, x + 4.75, 35.5, f"节点 {i + 1}", fs=6.6)
        for k in range(2):
            ax.add_patch(Rectangle((x + 1.9 + k * 3.2, 26.8), 2.6, 5.0, fc=BLUE_L,
                                   ec=BLUE, lw=0.5, zorder=4))

    # leaf ↔ spine 全互连
    for x in lx:
        for sx in (14.5, 32.5):
            ax.plot([x + 4.75, sx], [63.2, 75.8], color="#aeb6be", lw=0.7, zorder=1)
    # 节点 ↔ leaf
    for x in lx:
        ax.plot([x + 4.75, x + 4.75], [39.2, 55.8], color=MUTED, lw=0.9, zorder=1)

    note(ax, 1.5, 18.0, "每台 leaf：下联 32 口 400 Gb/s，上联 16 口", fs=6.6)
    note(ax, 1.5, 13.6, "→ 收敛比 2:1，跨 leaf 的流量要挤 16 条上联", fs=6.6, color=ORANGE)
    note(ax, 1.5, 9.2, "优点：任意两台机器最多三跳，拓扑对称好扩容", fs=6.6, color=GREEN)
    note(ax, 1.5, 4.8, "缺点：所有并行组挤同一张网，互相干扰", fs=6.6, color=MUTED)


def _rail(ax):
    label(ax, 52.5, 94, "Rail-optimized：第 r 张网卡只接第 r 台 leaf", fs=7.8, ha="left")

    # 节点
    box(ax, 52.5, 26, 14.5, 44, "", fc="#f8fafb", ec=MUTED, lw=0.9)
    label(ax, 54.5, 65.0, "节点", fs=7.0, ha="left")
    label(ax, 54.5, 60.8, "8 × GPU", fs=6.4, color=MUTED, ha="left")

    # 8 个网卡
    for i in range(8):
        y = 55.0 - i * 3.6
        ax.add_patch(Rectangle((63.6, y - 1.1), 3.0, 2.2, fc=BLUE_L, ec=BLUE, lw=0.5,
                               zorder=4))

    # 8 台 leaf
    for i in range(8):
        y = 65.0 - i * 6.0
        hot = i == 0
        box(ax, 74.0, y, 15.0, 4.6, f"Leaf {i}", fc=ORANGE_L if hot else GREEN_L,
            ec=ORANGE if hot else GREEN, fs=6.4)
        ax.plot([66.9, 73.8], [55.0 - i * 3.6, y + 2.3], color=ORANGE if hot else "#aeb6be",
                lw=1.1 if hot else 0.7, zorder=2)

    label(ax, 69.0, 74.0, "8 条 rail", fs=6.6, color=MUTED, ha="center")

    note(ax, 52.5, 20.0, "每节点 8 张 400 Gb/s 网卡，合计 3.2 Tb/s", fs=6.6)
    note(ax, 52.5, 15.6, "同一 rail 内只过一级交换 → 1:1 不收敛", fs=6.6, color=ORANGE)
    note(ax, 52.5, 11.2, "其他机器照抄同一规则，rail 号就是网卡号", fs=6.6, color=MUTED)
    note(ax, 52.5, 6.8, "优点：TP / PP 组被锁在少数 rail 上，干扰可控", fs=6.6, color=GREEN)


def fig_topo():
    fig, ax = canvas(16.0, 0.74, xlim=(0, 100), ylim=(0, 100))
    _fat_tree(ax)
    _rail(ax)
    ax.plot([50, 50], [2, 92], color=FAINT, lw=0.7, ls=(0, (4, 3)))
    save(fig, "fig06-01-topo.png")
