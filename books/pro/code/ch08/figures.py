# -*- coding: utf-8 -*-
"""第 8 章插图：incast 汇聚与 PFC 反压扩散。"""
from common import *  # noqa: F401,F403

from matplotlib.patches import Rectangle

FIGURES = ["fig_incast"]


def fig_incast():
    fig, ax = canvas(16.0, 0.64, xlim=(0, 100), ylim=(0, 100))

    # ---------------- 发送方
    sy = [76, 62, 48, 34]
    for i, y in enumerate(sy):
        box(ax, 7, y, 13, 10, f"发送方 {i + 1}", fc=BLUE_L, ec=BLUE, fs=6.8)
        arrow(ax, (20.4, y + 6.2), (29.6, 62 - i * 2.6), color=BLUE, lw=1.0, ms=7)
    label(ax, 13.5, 89, "各 400 Gb/s", fs=6.8, color=BLUE)

    # ---------------- 交换机
    box(ax, 30, 30, 17, 52, "", fc="#fbfcfd", ec=INK, lw=0.9)
    label(ax, 38.5, 79.5, "交换机", fs=6.8)
    # 缓存
    for k in range(9):
        full = k >= 7
        ax.add_patch(Rectangle((33.4, 34 + k * 4.4), 3.8, 3.8,
                               fc=RED_L if not full else RED,
                               ec=RED if full else FAINT, lw=0.6, zorder=3))
    label(ax, 31.7, 56, "缓存", fs=6.2, color=MUTED, rotation=90)
    # 出口
    box(ax, 38.5, 36, 7.0, 40, "", fc="white", ec=FAINT, lw=0.6)
    label(ax, 42.0, 56, "出端口", fs=6.2, color=MUTED, rotation=90)

    arrow(ax, (47.4, 56), (55.6, 56), color=INK, lw=1.0, ms=7)
    label(ax, 51.5, 59.5, "400 G", fs=6.4, color=MUTED)

    # ---------------- 接收方
    box(ax, 56, 44, 13, 24, "接收方\n100 Gb/s", fc=GREEN_L, ec=GREEN, fs=6.8)
    note(ax, 56, 41.0, "4 份流量挤 1 个出口", fs=6.4, color=RED)

    # ---------------- PFC 反压回路
    xs = 3.0
    ax.plot([33.0, 33.0, xs, xs], [30.2, 24.0, 24.0, 81.0], color=RED, lw=0.9,
            ls=(0, (4, 2)), zorder=2)
    for y in sy:
        arrow(ax, (xs, y + 5), (6.6, y + 5), color=RED, lw=0.9, ms=6, ls=(0, (4, 2)))
    label(ax, 26.0, 21.0, "PFC 暂停帧原路反压，四个发送方全被停住", fs=6.6, color=RED,
          ha="center")

    # ---------------- 右侧：连锁扩散
    label(ax, 74.0, 90, "PFC 的连锁反应", fs=7.4, ha="left")
    hops = [(78.0, 74.0, "交换机 A"), (78.0, 58.0, "交换机 B"), (78.0, 42.0, "交换机 C")]
    for x, y, name in hops:
        box(ax, x, y, 18.0, 9.0, name, fc="#fbfcfd", ec=RED, fs=6.6)
    for i in range(2):
        y1 = hops[i][1]
        y2 = hops[i + 1][1] + 9.0
        arrow(ax, (87.0, y1 - 0.4), (87.0, y2 + 0.4), color=RED, lw=0.9, ms=6,
              ls=(0, (4, 2)))
        arrow(ax, (89.4, y2 + 0.4), (89.4, y1 - 0.4), color=RED, lw=0.9, ms=6,
              ls=(0, (4, 2)))
    note(ax, 74.0, 36.0, "暂停帧逐跳往上游传，", fs=6.5, color=RED)
    note(ax, 74.0, 31.6, "被误伤的流量一起停", fs=6.5, color=RED)
    note(ax, 74.0, 24.0, "缓解：限制在途数据量、", fs=6.5, color=MUTED)
    note(ax, 74.0, 19.6, "拥塞隔离，或直接改用", fs=6.5, color=MUTED)
    note(ax, 74.0, 15.2, "无损优先级的调度", fs=6.5, color=MUTED)

    note(ax, 1.5, 6.0,
         "incast 的根因不是带宽不够，而是多个入端口同时冲向同一个出端口——"
         "缓存被瞬时打满，丢包与暂停帧一起出现。",
         fs=6.7, ha="left")
    save(fig, "fig08-01-incast.png")
