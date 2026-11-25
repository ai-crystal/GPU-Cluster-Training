# -*- coding: utf-8 -*-
"""第 24 章插图：弹性训练——缩容后重新划分并行度。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_elastic"]


def draw_blocks(ax, x0, y0, cols, rows, bw, bh, gx, gy, prefix, color):
    i = 0
    for r in range(rows):
        for c in range(cols):
            x = x0 + c * (bw + gx)
            y = y0 + (rows - 1 - r) * (bh + gy)
            ax.add_patch(Rectangle((x, y), bw, bh, fc=color, ec="none", alpha=0.13, zorder=2))
            ax.add_patch(Rectangle((x, y), bw, bh, fc="none", ec=color, lw=0.7, zorder=3))
            ax.text(x + bw / 2, y + bh / 2, f"{prefix}{i}", ha="center", va="center",
                    fontsize=6.4, color=color, zorder=4)
            i += 1
    return i


def fig_elastic():
    fig, ax = canvas(16.0, 0.64)

    # ---------------- 左：1024 卡
    label(ax, 1.5, 96.0, "缩容前　1 024 卡", fs=8.4, color=INK, ha="left")
    label(ax, 1.5, 91.6, "TP = 8　PP = 8　DP = 16", fs=7.2, color=BLUE, ha="left")
    draw_blocks(ax, 1.5, 48.0, 4, 4, 6.9, 8.4, 1.0, 2.6, "DP", BLUE)
    label(ax, 1.5, 43.6, "每块 = 64 卡（8 TP × 8 PP）", fs=6.3, color=MUTED, ha="left")

    # ---------------- 中：检查点
    label(ax, 40.0, 96.0, "检查点", fs=8.4, color=INK, ha="left")
    label(ax, 40.0, 91.6, "全量分片写到存储", fs=6.4, color=MUTED, ha="left")
    ck = [("参数分片", BLUE), ("优化器状态", GREEN), ("数据位置 / step / RNG", ORANGE)]
    cy = 74.0
    for text, color in ck:
        box(ax, 37.0, cy, 23.0, 11.0, text, fc="white", ec=color, fs=6.6, color=color)
        cy -= 14.0

    # ---------------- 右：768 卡
    label(ax, 66.0, 96.0, "缩容后　768 卡", fs=8.4, color=INK, ha="left")
    label(ax, 66.0, 91.6, "TP = 8　PP = 8　DP = 12", fs=7.2, color=ORANGE, ha="left")
    draw_blocks(ax, 66.0, 48.0, 3, 4, 9.0, 8.4, 1.2, 2.6, "DP", ORANGE)
    label(ax, 66.0, 43.6, "每块 = 64 卡（8 TP × 8 PP）", fs=6.3, color=MUTED, ha="left")

    # ---------------- 箭头
    arrow(ax, (32.4, 68.0), (36.6, 68.0), color=GREEN, lw=1.0, ms=8)
    label(ax, 34.6, 64.2, "① 存", fs=6.5, color=GREEN)
    arrow(ax, (60.4, 68.0), (65.6, 68.0), color=ORANGE, lw=1.0, ms=8)
    label(ax, 63.0, 64.2, "② 取", fs=6.5, color=ORANGE)
    label(ax, 1.5, 36.0,
          "TP / PP 组不变，层内的切分和通信模式都不用动；变的是 DP 组：16 组 → 12 组。",
          fs=6.8, color=INK, ha="left")
    label(ax, 1.5, 31.4,
          "优化器状态与梯度分片按新的 DP 组重新切分（每卡分到更多），全局 batch 相应变小，学习率与步数要跟着调整。",
          fs=6.8, color=MUTED, ha="left")

    # ---------------- 底：流程
    steps = [("掉卡 / 缩容信号", "检测到不可恢复的节点", MUTED),
             ("回滚到检查点", "取最近一次完整快照", GREEN),
             ("重算并行度", "DP 16 → 12，重切分片", ORANGE),
             ("重建通信组续训", "按新拓扑建 NCCL 组", BLUE)]
    x = 1.5
    for i, (title, sub, color) in enumerate(steps):
        box(ax, x, 8.0, 21.4, 17.0, fc="white", ec=color, lw=0.9, radius=1.2)
        label(ax, x + 10.7, 19.4, title, fs=7.4, color=color)
        label(ax, x + 10.7, 13.4, sub, fs=6.3, color=MUTED)
        if i < len(steps) - 1:
            arrow(ax, (x + 21.6, 16.5), (x + 24.4, 16.5), color=MUTED, lw=0.8, ms=6)
        x += 24.6

    save(fig, "fig24-01-elastic.png")
