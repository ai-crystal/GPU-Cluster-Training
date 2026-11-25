# -*- coding: utf-8 -*-
"""第 9 章插图：梯度分桶与通信/计算重叠。"""
from common import *  # noqa: F401,F403

from matplotlib.patches import Rectangle

FIGURES = ["fig_buckets"]


def _row(ax, y, name, segs, h=9.0, fs=6.6):
    label(ax, 9.0, y + h / 2, name, fs=7.0, ha="right")
    for a, b, color, text, tcol in segs:
        ax.add_patch(Rectangle((a, y), b - a, h, fc=color, ec="white", lw=0.8, zorder=3))
        if text:
            ax.text((a + b) / 2, y + h / 2, text, ha="center", va="center",
                    fontsize=fs, color=tcol, zorder=4)


def fig_buckets():
    fig, ax = canvas(16.0, 0.62, xlim=(0, 100), ylim=(0, 100))

    t0, step, arw = 12.0, 17.5, 12.0
    b = [t0 + i * step for i in range(4)]

    # 前向
    fwd = [(b[i], b[i] + step, "#f2f4f6", f"层 {i + 1}", MUTED) for i in range(4)]
    _row(ax, 80, "前向计算", fwd)

    # 反向（层 4 → 层 1）
    bwd = [(b[i], b[i] + step, BLUE_L, f"层 {4 - i} 反传", BLUE) for i in range(4)]
    _row(ax, 65, "反向计算", bwd)

    # 梯度桶
    buckets = [(b[i], b[i] + step, "#f7f1e2", f"桶 {i + 1}", GOLD) for i in range(4)]
    _row(ax, 50, "梯度桶", buckets)

    # all-reduce
    ar = [(b[i] + step, b[i] + step + arw, ORANGE, f"AR{i + 1}", "white") for i in range(4)]
    _row(ax, 35, "all-reduce", ar)

    # 对齐虚线
    for i in range(1, 4):
        vline(ax, b[i], 33.0, 78.0)
    vline(ax, b[3] + step, 33.0, 78.0)

    # 时间轴
    arrow(ax, (t0, 28.0), (98.0, 28.0), color=MUTED, lw=0.7, ms=6)
    label(ax, 98.6, 28.0, "时间", fs=6.6, color=MUTED, ha="left")

    # 重叠说明
    label(ax, b[0] + step + 0.5, 31.5, "AR1 与上方的层 3 反传同时进行，通信被计算盖住",
          fs=6.6, color=GREEN, ha="left")

    # 总耗时
    ax.annotate("", xy=(b[3] + step, 92.5), xytext=(t0, 92.5),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.7))
    label(ax, (t0 + b[3] + step) / 2, 94.5, "总耗时 ≈ 反传总时间 + 最后一次 all-reduce",
          fs=6.8, color=MUTED)

    note(ax, 1.5, 20.0, "桶满就发：某层梯度攒够一个桶，立刻发起 all-reduce，不等整个反传结束。",
         fs=6.8, ha="left")
    note(ax, 1.5, 14.5, "桶太大 → 要等很久才发第一包，尾巴露在计算外面；桶太小 → 每次启动开销占比高。",
         fs=6.8, ha="left")
    note(ax, 1.5, 9.0, "常见做法是 25 MB 一桶，并按反向顺序倒着分桶，保证第一个桶最早填满。",
         fs=6.8, ha="left")
    save(fig, "fig09-01-buckets.png")
