# -*- coding: utf-8 -*-
"""第 15 章插图：并行配置的约束空间。"""
from common import *  # noqa: F401,F403

import numpy as np

FIGURES = ["fig_search"]

TP = [1, 2, 4, 8, 16, 32, 64]
PP = [1, 2, 4, 8, 16, 32]
MIN_CARD = 64          # 405B 参数 + 优化器状态至少需要的卡数（估算）


def fig_search():
    fig, ax = chart(15.6, 8.6)

    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xlim(0.75, 110)
    ax.set_ylim(0.75, 44)
    ax.grid(False)
    for g in (0.6,):
        pass
    for x in TP:
        ax.axvline(x, color="#f0f2f4", lw=0.6, zorder=0)
    for y in PP:
        ax.axhline(y, color="#f0f2f4", lw=0.6, zorder=0)

    # 显存下限：TP×PP 至少要这么多卡
    xs = np.logspace(np.log2(0.75), np.log2(110), 400, base=2)
    ax.fill_between(xs, 0.75, np.minimum(MIN_CARD / xs, 44), color=RED_L,
                    alpha=0.40, lw=0, zorder=1)
    ax.plot(xs, MIN_CARD / xs, color=RED, lw=0.9, ls=(0, (4, 3)), zorder=2,
            label="_")
    ax.text(1.05, 1.05, "装不下：参数 + 优化器状态\n超出 80 GB 单卡容量",
            fontsize=6.8, color=RED, ha="left", va="bottom", zorder=4,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.4, alpha=0.9))

    # 节点边界
    ax.axvline(8, color=ORANGE, lw=0.9, ls=(0, (3, 2)), zorder=2)
    ax.fill_between([8, 110], 0.75, 44, color=ORANGE_L, alpha=0.35, lw=0, zorder=0)
    ax.text(9.4, 38.0, "TP > 8：越过单节点边界，每层 all-reduce 走 IB",
            fontsize=6.8, color=ORANGE, ha="left", va="center", zorder=4)

    # 卡片格子
    for tp in TP:
        for pp in PP:
            ok = tp * pp >= MIN_CARD
            cross = tp > 8
            if ok:
                ax.plot(tp, pp, "o", ms=4.6,
                        mfc=(ORANGE if cross else BLUE), mec="white", mew=0.6,
                        zorder=4)
            else:
                ax.plot(tp, pp, "o", ms=3.4, mfc="white", mec=FAINT, mew=0.8,
                        zorder=3)

    # 405B 的可行点
    ax.plot([8], [16], "o", ms=9.5, mfc="none", mec=GREEN, mew=1.4, zorder=6)
    ax.annotate("405B：TP 8 × PP 16\n= 128 卡（再乘 DP 扩到整集群）",
                xy=(8, 16), xytext=(11.5, 20.5), fontsize=7.2, color=GREEN,
                ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=0.8,
                                connectionstyle="arc3,rad=0.18"))

    # 其他可行点
    for tp, pp in ((8, 8), (4, 32), (16, 16), (32, 8)):
        ax.plot(tp, pp, "o", ms=6.2, mfc="none", mec=MUTED, mew=0.9,
                ls="none", zorder=5)

    ax.set_xticks(TP)
    ax.set_xticklabels([str(t) for t in TP])
    ax.set_yticks(PP)
    ax.set_yticklabels([str(p) for p in PP])
    ax.tick_params(which="minor", length=0)
    ax.set_xlabel("张量并行度 TP", fontsize=8.2)
    ax.set_ylabel("流水线并行度 PP", fontsize=8.2, labelpad=5)

    ax.annotate("PP 再大，气泡就吃掉收益", xy=(8, 32), xytext=(1.05, 26),
                fontsize=6.8, color=MUTED, ha="left", va="center",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.9),
                arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=0.7,
                                connectionstyle="arc3,rad=-0.2"))

    anote(ax, 0.0, -0.14,
          "每个点是一种 (TP, PP) 组合，只能落在 2 的幂上：TP 要整除 128 个头、隐藏维 16384，"
          "PP 要整除 96 层。\n红色虚线下限按 405B 的权重、梯度与 Adam 状态合计约 4.9 TB、"
          "每卡 80 GB 估算，实际还要加上激活，真实下限只会更高。",
          fs=6.9, va="top")
    save(fig, "fig15-01-search.png")
