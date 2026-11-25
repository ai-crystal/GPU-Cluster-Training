# -*- coding: utf-8 -*-
"""第 20 章插图：同步检查点与异步检查点。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_ckpt"]

X0 = 12.0
STEP = 10.0
PAUSE = 26.0
COPY = 5.0


def fig_ckpt():
    fig, ax = canvas(16.0, 0.50, xlim=(0, 100), ylim=(0, 100))

    label(ax, 1.0, 94.0, "（a）同步检查点：所有卡停下来等写盘", fs=7.8, ha="left")
    label(ax, 1.0, 44.0, "（b）异步检查点：先抄一份，写盘挪到后台", fs=7.8, ha="left")

    # ---------------- (a)
    y, h = 74.0, 9.0
    label(ax, X0 - 1.4, y + h / 2, "GPU", fs=6.8, color=MUTED, ha="right")
    for k in range(4):
        x = X0 + k * STEP
        ax.add_patch(Rectangle((x, y), STEP - 0.3, h, fc=BLUE, ec="white", lw=0.7,
                               zorder=3))
        label(ax, x + STEP / 2, y + h / 2, f"第 {k + 1} 步", fs=6.4, color="white")
    xp = X0 + 4 * STEP
    ax.add_patch(Rectangle((xp, y), PAUSE, h, fc=RED, ec="white", lw=0.7, zorder=3))
    label(ax, xp + PAUSE / 2, y + h / 2, "全体暂停：写盘", fs=6.6, color="white")
    for k in range(4, 6):
        x = xp + PAUSE + (k - 4) * STEP
        ax.add_patch(Rectangle((x, y), STEP - 0.3, h, fc=BLUE, ec="white", lw=0.7,
                               zorder=3))
        label(ax, x + STEP / 2, y + h / 2, f"第 {k + 1} 步", fs=6.4, color="white")

    bracket(ax, xp, xp + PAUSE, y - 2.0, "这段时间集群什么也没算", fs=6.3,
            color=RED, up=-1.6)

    # ---------------- (b)
    yb, hb = 24.0, 9.0
    label(ax, X0 - 1.4, yb + hb / 2, "GPU", fs=6.8, color=MUTED, ha="right")
    xc = X0 + 4 * STEP
    for k in range(4):
        x = X0 + k * STEP
        ax.add_patch(Rectangle((x, yb), STEP - 0.3, hb, fc=BLUE, ec="white",
                               lw=0.7, zorder=3))
        label(ax, x + STEP / 2, yb + hb / 2, f"第 {k + 1} 步", fs=6.4, color="white")
    ax.add_patch(Rectangle((xc, yb), COPY, hb, fc=RED, ec="white", lw=0.7, zorder=3))
    label(ax, xc + COPY / 2, yb + hb / 2, "抄", fs=6.4, color="white")
    for k in range(4, 7):
        x = xc + COPY + (k - 4) * STEP
        ax.add_patch(Rectangle((x, yb), STEP - 0.3, hb, fc=BLUE, ec="white",
                               lw=0.7, zorder=3))
        label(ax, x + STEP / 2, yb + hb / 2, f"第 {k + 1} 步", fs=6.4, color="white")

    # 后台写盘
    yd, hd = 12.0, 6.0
    label(ax, X0 - 1.4, yd + hd / 2, "写盘", fs=6.8, color=MUTED, ha="right")
    ax.add_patch(Rectangle((xc + COPY, yd), PAUSE, hd, fc=ORANGE_L, ec=ORANGE,
                           lw=0.8, ls=(0, (3, 2)), zorder=3))
    label(ax, xc + COPY + PAUSE / 2, yd + hd / 2, "后台写盘，不占 GPU",
          fs=6.3, color=ORANGE)

    label(ax, xc - 1.8, yd + 4.4, "停顿只剩这一次拷贝", fs=6.1, color=RED,
          ha="right", va="center")

    anote(ax, 0.01, -0.04,
          "同步检查点的停顿随模型规模线性增长，几千张卡时一次能停几十分钟；"
          "异步检查点把「写」挪到后台，代价是需要一块额外的显存/内存副本。",
          fs=6.8, va="top")
    save(fig, "fig20-01-ckpt.png")
