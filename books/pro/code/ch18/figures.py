# -*- coding: utf-8 -*-
"""第 18 章插图：计算与通信的重叠。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_overlap"]

X0 = 13.0
COMP, COMM = 20.0, 5.6
STEP_S = COMP + COMM
STEP_O = COMP
NP = 3


def fig_overlap():
    fig, ax = canvas(16.0, 0.50, xlim=(0, 100), ylim=(0, 100))

    label(ax, 1.0, 95.0, "（a）无重叠：算完再通信，每一步都多出一段", fs=7.8, ha="left")
    label(ax, 1.0, 47.5, "（b）有重叠：通信塞进计算时间里", fs=7.8, ha="left")

    # 图例
    lx, ly = 66.0, 88.0
    ax.add_patch(Rectangle((lx, ly), 3.4, 3.4, fc=BLUE, ec="none"))
    label(ax, lx + 4.4, ly + 1.7, "计算", fs=6.8, ha="left")
    ax.add_patch(Rectangle((lx + 12, ly), 3.4, 3.4, fc=ORANGE, ec="none"))
    label(ax, lx + 16.4, ly + 1.7, "集合通信", fs=6.8, ha="left")

    # ---------------- (a) 串行
    y = 76.0
    label(ax, X0 - 1.4, y + 4.6, "GPU", fs=6.8, color=MUTED, ha="right")
    for k in range(NP):
        x = X0 + k * STEP_S
        ax.add_patch(Rectangle((x, y), COMP, 9.2, fc=BLUE, ec="white", lw=0.8,
                               zorder=3))
        label(ax, x + COMP / 2, y + 4.6, f"第 {k + 1} 步计算", fs=6.4, color="white")
        ax.add_patch(Rectangle((x + COMP, y), COMM, 9.2, fc=ORANGE, ec="white",
                               lw=0.8, zorder=3))
    label(ax, X0 + COMP + COMM / 2, y + 11.2, "all-reduce", fs=6.2, color=ORANGE)

    bracket(ax, X0, X0 + STEP_S, 71.0, "步时 = 计算 + 通信", fs=6.6, up=-1.3)
    ax.annotate("", xy=(X0 + 3 * STEP_S, 60.0), xytext=(X0, 60.0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7))
    label(ax, X0 + 3 * STEP_S, 56.6, "总时长 3 × (计算 + 通信)", fs=6.6, color=MUTED,
          ha="right")

    # ---------------- (b) 重叠
    yb, yc = 26.0, 34.0
    label(ax, X0 - 1.4, yc + 4.6, "计算", fs=6.8, color=MUTED, ha="right")
    label(ax, X0 - 1.4, yb + 3.0, "通信", fs=6.8, color=MUTED, ha="right")
    for k in range(NP):
        x = X0 + k * STEP_O
        ax.add_patch(Rectangle((x, yc), COMP - 0.3, 9.2, fc=BLUE, ec="white",
                               lw=0.8, zorder=3))
        label(ax, x + COMP / 2, yc + 4.6, f"第 {k + 1} 步", fs=6.4, color="white")
        ax.add_patch(Rectangle((x + 1.0, yb), COMM, 6.0, fc=ORANGE, ec="white",
                               lw=0.8, zorder=3))

    # 通信块与计算的对应关系
    for k in range(2):
        x = X0 + k * STEP_O
        ax.plot([x + 1.0 + COMM / 2, x + 1.0 + COMM / 2], [yb + 6.2, yc - 0.4],
                color=FAINT, lw=0.7, ls=(0, (2, 2)), zorder=1)

    bracket(ax, X0, X0 + STEP_O, 21.0, "步时 = 计算（通信在后台）", fs=6.6, up=-1.3)
    ax.annotate("", xy=(X0 + 3 * STEP_O, 12.0), xytext=(X0, 12.0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7))
    label(ax, X0 + 3 * STEP_O, 8.6, "总时长 3 × 计算", fs=6.6, color=MUTED,
          ha="right")

    # 差值标记
    xr = X0 + 3 * STEP_O
    ax.annotate("", xy=(X0 + 3 * STEP_S, 66.5), xytext=(xr, 66.5),
                arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=0.8))
    label(ax, (xr + X0 + 3 * STEP_S) / 2, 68.2, "多花 3 段通信", fs=6.3,
          color=GREEN, ha="center", va="bottom")

    anote(ax, 0.01, -0.02,
          "示意图中通信约占步时的 22%，实际比例取决于张量并行度、消息大小与互连带宽。",
          fs=6.8, va="top")
    save(fig, "fig18-01-overlap.png")
