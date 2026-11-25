# -*- coding: utf-8 -*-
"""第 13 章插图：故障后的时间线、检查点间隔的取舍。"""
from common import *  # noqa: F401,F403

import numpy as np

FIGURES = ["fig_timeline", "fig_ckpt_interval"]


def fig_timeline():
    fig, ax = canvas(16.0, 0.34, xlim=(0, 100), ylim=(26, 100))
    x0, x1 = 8, 96
    y = 55
    ax.add_patch(Rectangle((x0, y), 46, 14, fc=BLUE_L, ec=BLUE, lw=0.9, zorder=3))
    ax.text(x0 + 23, y + 7, "有效训练", ha="center", va="center", fontsize=7.8, color=BLUE)
    ax.add_patch(Rectangle((x0 + 46, y), 4, 14, fc=RED, ec=RED, lw=0.9, zorder=3))
    ax.text(x0 + 48, y + 18, "故障", ha="center", fontsize=7.0, color=RED)
    ax.add_patch(Rectangle((x0 + 50, y), 16, 14, fc="#f1f2f4", ec=MUTED, lw=0.9, zorder=3))
    ax.text(x0 + 58, y + 7, "检测 + 重启", ha="center", va="center", fontsize=7.0, color=MUTED)
    ax.add_patch(Rectangle((x0 + 66, y), 12, 14, fc=ORANGE_L, ec=ORANGE, lw=0.9, zorder=3))
    ax.text(x0 + 72, y + 7, "重算", ha="center", va="center", fontsize=7.0, color=ORANGE)
    ax.add_patch(Rectangle((x0 + 78, y), 10, 14, fc=BLUE_L, ec=BLUE, lw=0.9, zorder=3))

    ax.annotate("", xy=(x1, y - 8), xytext=(x0, y - 8),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8))
    ax.text(x1, y - 13, "时间", ha="right", fontsize=7.2, color=MUTED)

    cp = x0 + 30
    ax.plot([cp, cp], [y + 14, y + 20], color=GREEN, lw=1.2)
    ax.text(cp, y + 22, "上次检查点", ha="center", fontsize=7.0, color=GREEN)
    ax.annotate("", xy=(x0 + 47, y + 18), xytext=(cp, y + 18),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=0.8, ls="--"))

    note(ax, 2, 36, "检测、隔离、重启进程、加载检查点、重建通信组、预热，每一步都要时间。",
         fs=7.4, ha="left")
    save(fig, "fig13-01-timeline.png")


def fig_ckpt_interval():
    fig, ax = chart(15.6, 8.2)
    t_ckpt = 1 / 60       # 小时
    mtbf = 54 * 24 / 419  # 小时
    I = np.linspace(0.05, 3.0, 300)
    waste = t_ckpt / I + I / (2 * mtbf)
    ax.plot(I * 60, waste * 100, color=BLUE, lw=1.8, zorder=3)
    best = np.sqrt(2 * t_ckpt * mtbf)
    ax.plot([best * 60], [(t_ckpt / best + best / (2 * mtbf)) * 100], "o",
            color=ORANGE, ms=6, zorder=5)
    ax.annotate(f"最优间隔约 {best * 60:.0f} 分钟\n浪费约 {(t_ckpt / best + best / (2 * mtbf)) * 100:.1f}%",
                xy=(best * 60, (t_ckpt / best + best / (2 * mtbf)) * 100),
                xytext=(best * 60 + 25, 24), fontsize=7.6, color=ORANGE,
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.8))
    ax.set_xlabel("检查点间隔（分钟）", fontsize=8.2)
    ax.set_ylabel("被浪费的时间占比（%）", fontsize=8.2, labelpad=7)
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 40)
    anote(ax, 0.01, -0.15,
          "按异步检查点每次约 1 分钟、平均故障间隔 3.1 小时（Llama 3 的公开数据）估算：\n"
          "浪费 = 写检查点的时间 / 间隔 + 间隔 / (2 × 平均故障间隔)。",
          fs=7.0, va="top")
    save(fig, "fig13-02-ckpt.png")
