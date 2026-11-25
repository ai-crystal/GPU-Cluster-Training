# -*- coding: utf-8 -*-
"""第 15 章插图：端到端训练流水线。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_pipeline"]


def fig_pipeline():
    fig, ax = canvas(16.0, 0.46, xlim=(0, 100), ylim=(0, 100))

    box(ax, 3, 52, 22, 20, "数据准备\n采集 清洗\n分词 配比", fc=BLUE_L, ec=BLUE, fs=7.4)
    box(ax, 39, 52, 24, 20, "训练循环\n前向 反向\n更新 评估", fc=ORANGE_L, ec=ORANGE, fs=7.4)
    box(ax, 76, 52, 21, 20, "交付\n导出 评测\n发布", fc=PURPLE_L, ec=PURPLE, fs=7.4)

    arrow(ax, (25.4, 62), (38.6, 62), color=INK, ms=8)
    arrow(ax, (63.4, 62), (75.6, 62), color=INK, ms=8)

    box(ax, 39, 18, 24, 18, "保障\n监控 检查点\n故障恢复", fc=GREEN_L, ec=GREEN, fs=7.4)
    ax.annotate("", xy=(51, 51), xytext=(51, 37),
                arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=0.9, ls="--"))

    box(ax, 39, 78, 24, 14, "实验与调参", fc="#f6f7f8", ec=MUTED, fs=7.4)
    ax.annotate("", xy=(51, 73), xytext=(51, 77),
                arrowprops=dict(arrowstyle="<|-|>", color=MUTED, lw=0.9, ls="--"))

    note(ax, 2, 8, "数据、训练、保障三条线同时在动，任何一条断了，整条流水线就停。",
         fs=7.4, ha="left")
    save(fig, "fig15-01-pipeline.png")
