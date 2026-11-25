# -*- coding: utf-8 -*-
"""第 22 章插图：故障率随集群规模的变化。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_failure_rate"]

# Llama 3 公开数据：54 天、16384 卡、419 次意外中断
RATE = 419 / (16384 * 54 * 24)     # 单卡故障率，次/小时
MTBF_1 = 1 / RATE                  # 单卡 MTBF，小时


def fig_failure_rate():
    fig, ax = chart(15.0, 7.6)

    labels = ["1 000 卡", "4 000 卡", "8 000 卡", "16 384 卡"]
    n = [1000, 4000, 8000, 16384]
    vals = [MTBF_1 / k for k in n]
    colors = [BLUE, BLUE, BLUE, ORANGE]

    rects = bars(ax, labels, vals, colors=colors, width=0.46, fs=8.4,
                 fmt="{:.1f}", text_fs=8.0, ylim=(0, 58))
    for r, v in zip(rects, vals):
        cx = r.get_x() + r.get_width() / 2
        if v >= 12:
            ax.text(cx, v * 0.45, f"约 {24 / v:.1f} 次\n中断 / 天", ha="center",
                    va="center", fontsize=6.9, color="white", linespacing=1.5, zorder=5)
        else:
            ax.text(cx, v + 4.6, f"{24 / v:.1f} 次中断 / 天", ha="center", va="bottom",
                    fontsize=6.6, color=MUTED, zorder=5)

    ax.axhline(24, color=GREEN, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.text(3.42, 25.2, "一天（24 小时）", ha="right", va="bottom",
            fontsize=7.0, color=GREEN, zorder=5)

    ax.set_ylabel("平均无故障时间 MTBF（小时）", fontsize=8.2, labelpad=6)
    ax.set_xlabel("集群规模（GPU 卡数）", fontsize=8.2, labelpad=4)
    ax.set_ylim(0, 58)
    ax.tick_params(axis="x", length=0)

    anote(ax, 0.012, -0.175,
          "按 Llama 3 公开数据线性外推：54 天、16 384 卡、419 次意外中断\n"
          "→ 单卡故障率约 $2.0\\times10^{-5}$ /小时（单卡 MTBF 约 5.1 万小时），"
          "N 卡集群的 MTBF = 5.1 万 / N 小时。",
          fs=6.9, va="top")
    anote(ax, 0.012, -0.30,
          "规模扩大 16 倍，平均无故障时间缩短 16 倍：这不是运维水平下降，而是概率的算术。",
          fs=6.9, va="top", color=ORANGE)

    save(fig, "fig22-01-failure-rate.png")
