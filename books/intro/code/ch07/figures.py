# -*- coding: utf-8 -*-
"""第 7 章插图：张量并行切分、流水线气泡。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_tp", "fig_pp"]


def fig_tp():
    fig, ax = canvas(16.0, 0.5, xlim=(0, 100), ylim=(0, 100))

    box(ax, 2, 42, 10, 16, "X", fc="#f6f7f8", ec=MUTED, fs=9)

    for k, y in ((0, 62), (1, 28)):
        box(ax, 17, y, 9, 14, "A" + str(k + 1), fc=BLUE_L, ec=BLUE, fs=9)
        box(ax, 30, y, 9, 14, "GeLU", fc="#f6f7f8", ec=MUTED, fs=7.6)
        box(ax, 43, y, 9, 14, "B" + str(k + 1), fc=BLUE_L, ec=BLUE, fs=9)
        arrow(ax, (12.3, 50), (16.7, y + 7), color=INK, ms=7)
        arrow(ax, (26.3, y + 7), (29.7, y + 7), color=INK, ms=6)
        arrow(ax, (39.3, y + 7), (42.7, y + 7), color=INK, ms=6)

    box(ax, 58, 38, 13, 24, "按元素相加\nall-reduce", fc=ORANGE_L, ec=ORANGE, fs=7.6)
    arrow(ax, (52.3, 69), (57.7, 55), color=ORANGE, ms=7)
    arrow(ax, (52.3, 35), (57.7, 47), color=ORANGE, ms=7)
    box(ax, 77, 42, 10, 16, "Y", fc="#f6f7f8", ec=MUTED, fs=9)
    arrow(ax, (71.3, 50), (76.7, 50), color=INK, ms=7)

    label(ax, 6, 30, "列并行", fs=7.4, color=BLUE, rotation=90)
    label(ax, 47, 20, "行并行", fs=7.4, color=BLUE, rotation=90)
    note(ax, 2, 8, "每层只在这一处归约，传输量等于激活值的大小。", fs=7.2, ha="left", color=ORANGE)
    save(fig, "fig07-01-tp.png")


def fig_pp():
    fig, ax = canvas(16.0, 0.44, xlim=(0, 100), ylim=(10, 100))
    S, M = 4, 8
    total = 2 * M + S - 1
    x0, x1 = 15, 96
    cw = (x1 - x0) / total
    ch = 10.0
    base = 77

    for s in range(S):
        y = base - s * (ch + 2.0)
        ax.text(x0 - 2, y + ch / 2, f"卡 {s + 1}", ha="right", va="center", fontsize=7.6)
        for m in range(M):
            tf = m + s
            tb = M + s + (M - 1 - m)
            ax.add_patch(Rectangle((x0 + tf * cw + 0.3, y), cw - 0.6, ch,
                                   fc=BLUE_L, ec=BLUE, lw=0.7, zorder=3))
            ax.add_patch(Rectangle((x0 + tb * cw + 0.3, y), cw - 0.6, ch,
                                   fc=ORANGE_L, ec=ORANGE, lw=0.7, zorder=3))
            ax.text(x0 + tf * cw + cw / 2, y + ch / 2, "F", ha="center", va="center",
                    fontsize=6.0, color=BLUE, zorder=4)
            ax.text(x0 + tb * cw + cw / 2, y + ch / 2, "B", ha="center", va="center",
                    fontsize=6.0, color=ORANGE, zorder=4)

    for s in range(S):
        y = base - s * (ch + 2.0)
        end_empty = total - (M + s)
        if s > 0:
            ax.add_patch(Rectangle((x0, y), cw * s, ch, fc="#f4f5f7", ec=FAINT,
                                   lw=0.6, ls="--", zorder=2))
        if end_empty > 0:
            ax.add_patch(Rectangle((x0 + (total - end_empty) * cw, y), cw * end_empty, ch,
                                   fc="#f4f5f7", ec=FAINT, lw=0.6, ls="--", zorder=2))
        if 1 < s < S - 1:
            ax.text(x0 + cw * s / 2, y + ch / 2, "空闲", ha="center", va="center",
                    fontsize=6.4, color=MUTED, zorder=5)

    bracket(ax, x0, x0 + (S - 1) * cw, 92, "预热", fs=7.0, up=1.6)
    bracket(ax, x0 + (total - S + 1) * cw, x1, 92, "排空", fs=7.0, up=1.6)
    ax.annotate("", xy=(x1, 16), xytext=(x0, 16),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8))
    ax.text(x1, 12, "时间（每格一个微批次）", ha="right", fontsize=7.2, color=MUTED)
    save(fig, "fig07-02-pp.png")
