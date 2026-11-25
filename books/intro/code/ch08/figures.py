# -*- coding: utf-8 -*-
"""第 8 章插图：数据并行、ZeRO 三阶段的显存占用。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_dp", "fig_zero"]


def fig_dp():
    fig, ax = canvas(16.0, 0.42, xlim=(0, 100), ylim=(0, 100))

    xs = [6 + i * 23 for i in range(4)]
    for i, x in enumerate(xs):
        box(ax, x, 46, 16, 20, f"模型副本\n第 {i + 1} 张卡", fc=BLUE_L, ec=BLUE, fs=7.4)
        box(ax, x, 14, 16, 12, f"数据分片 {i + 1}", fc="#f6f7f8", ec=MUTED, fs=7.2)
        arrow(ax, (x + 8, 27), (x + 8, 45), color=MUTED, lw=0.8, ms=6)

    # 梯度归约
    y = 76
    ax.plot([xs[0] + 8, xs[-1] + 8], [y, y], color=ORANGE, lw=1.1, zorder=3)
    for x in xs:
        ax.plot([x + 8, x + 8], [66, y], color=ORANGE, lw=1.1, zorder=3)
    box(ax, 34, 79, 32, 10, "all-reduce 汇总梯度", fc=ORANGE_L, ec=ORANGE, fs=7.6)

    note(ax, 2, 4, "每张卡保存一份完整模型，读不同的数据，算各自的梯度，然后把梯度加起来。",
         fs=7.6, ha="left")
    save(fig, "fig08-01-dp.png")


def fig_zero():
    fig, ax = chart(15.6, 7.8)
    nd = 8
    stages = ["普通数据并行", "ZeRO-1\n只切优化器状态", "ZeRO-2\n再切梯度", "ZeRO-3\n再切参数"]
    params = [2, 2, 2, 2 / nd]
    grads = [2, 2, 2 / nd, 2 / nd]
    opts = [12, 12 / nd, 12 / nd, 12 / nd]

    xs = range(4)
    ax.bar(xs, params, width=0.52, color=BLUE, label="参数", zorder=3)
    ax.bar(xs, grads, bottom=params, width=0.52, color=GREEN, label="梯度", zorder=3)
    bottom2 = [p + g for p, g in zip(params, grads)]
    ax.bar(xs, opts, bottom=bottom2, width=0.52, color=ORANGE,
           label="优化器状态", zorder=3)

    totals = [p + g + o for p, g, o in zip(params, grads, opts)]
    for x, t in zip(xs, totals):
        ax.text(x, t + 0.5, f"{t:g}", ha="center", va="bottom", fontsize=8.0)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(stages, fontsize=7.8)
    ax.set_ylabel("每卡字节 / 每参数", fontsize=8.2, labelpad=7)
    ax.set_ylim(0, 19.5)
    ax.legend(frameon=False, fontsize=7.6, loc="upper right", ncol=3,
              bbox_to_anchor=(1.0, 1.07))
    ax.grid(axis="x", visible=False)
    anote(ax, 0.01, -0.19, "按 8 路数据并行、混合精度训练估算：参数与梯度各 2 字节，Adam 的一阶矩与二阶矩各 4 字节。\n"
                           "前两个阶段减少的是每卡占用，第三个阶段把占用压到与并行度成反比。",
          fs=7.0, va="top")
    save(fig, "fig08-02-zero.png")
