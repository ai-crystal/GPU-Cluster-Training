# -*- coding: utf-8 -*-
"""第 26 章插图：一个训练步的 trace 与三类瓶颈。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_trace"]

X0, X1 = 9.0, 63.0      # 时间轴 0 → 1 的映射区间
W = X1 - X0


def tx(t):
    return X0 + W * t


def fig_trace():
    fig, ax = canvas(16.0, 0.58)

    yc, yh, yd = 76.0, 57.0, 38.0   # 计算 / 通信 / 数据 的底边
    h = 13.0

    # 车道名
    label(ax, 7.4, yc + h / 2, "计算", fs=7.6, color=INK, ha="right")
    label(ax, 7.4, yh + h / 2, "NCCL\n通信", fs=6.8, color=INK, ha="right")
    label(ax, 7.4, yd + h / 2, "数据加载", fs=7.6, color=INK, ha="right")

    # 计算段
    comp = [(0.09, 0.19, "前向"), (0.19, 0.44, "反向"), (0.44, 0.54, "前向"),
            (0.54, 0.79, "反向"), (0.87, 1.00, "优化器")]
    for a, b, text in comp:
        ax.add_patch(Rectangle((tx(a), yc), W * (b - a), h, fc=BLUE_L, ec=BLUE,
                               lw=0.8, zorder=3))
        ax.text(tx((a + b) / 2), yc + h / 2, text, ha="center", va="center",
                fontsize=6.4, color=BLUE, zorder=4)

    # 通信段：前四段与计算重叠，最后一段暴露出来
    nccl = [(0.19, 0.26, False), (0.38, 0.44, False), (0.55, 0.62, False),
            (0.73, 0.79, False), (0.79, 0.90, True)]
    for a, b, exposed in nccl:
        ax.add_patch(Rectangle((tx(a), yh), W * (b - a), h,
                               fc=ORANGE if exposed else ORANGE_L,
                               ec=ORANGE, lw=0.8, zorder=3))
    ax.text(tx(0.855), yh + h / 2, "暴露", ha="center", va="center",
            fontsize=6.5, color="white", zorder=4)

    # 数据段
    for a, b in [(0.00, 0.09), (0.28, 0.42), (0.60, 0.70)]:
        ax.add_patch(Rectangle((tx(a), yd), W * (b - a), h, fc=GREEN_L, ec=GREEN,
                               lw=0.8, zorder=3))

    # 空洞：计算车道上既没算也没等的两段
    for a, b in [(0.00, 0.09), (0.79, 0.87)]:
        ax.add_patch(Rectangle((tx(a), yc), W * (b - a), h, fc="none", ec=RED,
                               lw=0.8, ls=(0, (3, 2)), zorder=3))

    # 时间轴
    ax.annotate("", xy=(X1 + 1.0, 31.0), xytext=(X0, 31.0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8))
    for t, s in [(0.0, "0"), (0.5, "50%"), (1.0, "step 结束")]:
        ax.plot([tx(t), tx(t)], [31.0, 32.4], color=MUTED, lw=0.7)
        ax.text(tx(t), 29.4, s, ha="center", va="top", fontsize=6.4, color=MUTED)

    # 三类瓶颈的数标
    marks = [(tx(0.315), yc + h + 2.4, "1", ORANGE, 1.6),
             (tx(0.845), yh + h + 2.2, "2", ORANGE, 1.6),
             (tx(0.045), yc + h / 2, "3", RED, 1.5)]
    for x, y, s, c, r in marks:
        ax.add_patch(Circle((x, y), r, fc=c, ec="white", lw=0.8, zorder=6))
        ax.text(x, y - 0.15, s, ha="center", va="center", fontsize=6.0,
                color="white", zorder=7)

    # 三类瓶颈的识别方式
    notes = [("① 计算受限", ORANGE,
              "计算车道几乎铺满、没有空洞——步时长由算力决定；去看 kernel 占用率与 HBM 带宽。"),
             ("② 通信受限", ORANGE,
              "NCCL 段没有被计算盖住（暴露出来）——看 all-reduce 的消息量与 TP / PP 切分。"),
             ("③ 空洞", RED,
              "计算与通信同时闲着——在等数据、等最慢的那张卡，或在写检查点。")]
    ny = 23.0
    for title, color, text in notes:
        label(ax, 9.0, ny, title, fs=6.9, color=color, ha="left")
        label(ax, 22.5, ny, text, fs=6.7, color=INK, ha="left")
        ny -= 5.0

    save(fig, "fig26-01-trace.png")
