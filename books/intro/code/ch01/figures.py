# -*- coding: utf-8 -*-
"""第 1 章插图：训练规模的增长、算力估算。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_scale", "fig_estimate"]


def fig_scale():
    fig, ax = chart(15.4, 8.6)
    names = ["BLOOM\n176B · 2022", "OPT\n175B · 2022", "GPT-3\n175B · 2020",
             "PaLM\n540B · 2022", "MegaScale\n175B · 2024", "Llama 3\n405B · 2024"]
    gpus = [384, 992, 1024, 6144, 12288, 16384]
    colors = [MUTED, BLUE, BLUE, PURPLE, ORANGE, ORANGE]
    bars(ax, names, gpus, colors=colors, width=0.58, fmt="{:,.0f}", log=True,
         ylim=(200, 42000), fs=7.6)
    ax.set_ylabel("训练使用的加速卡数量（张，对数刻度）", fontsize=8.2)
    ax.set_yticks([300, 1000, 3000, 10000, 30000])
    ax.set_yticklabels(["300", "1 000", "3 000", "10 000", "30 000"])
    ax.set_ylim(200, 42000)
    ax.grid(axis="x", visible=False)
    anote(ax, 0.01, -0.16, "BLOOM、OPT、GPT-3 的卡数来自各自论文；PaLM 用的是 TPU v4；"
                           "MegaScale 与 Llama 3 为公开的万卡级配置。",
          fs=7.0, va="top")
    save(fig, "fig01-01-cluster-scale.png")


def fig_estimate():
    fig, ax = canvas(15.6, 0.44, xlim=(0, 100), ylim=(0, 62))

    box(ax, 1, 20, 20, 22, "参数量\nN = 4050 亿", fc=BLUE_L, ec=BLUE, fs=9)
    box(ax, 25, 20, 20, 22, "训练 token\nD = 15.6 万亿", fc=BLUE_L, ec=BLUE, fs=9)
    box(ax, 49, 20, 22, 22, "前向加反向\n≈ 6 N D", fc=ORANGE_L, ec=ORANGE, fs=9)
    box(ax, 75, 20, 23, 22, "总计算量\n≈ 3.8×10$^{25}$ FLOPs", fc=GREEN_L, ec=GREEN, fs=9)

    arrow(ax, (21, 31), (25, 31), color=INK, ms=8)
    arrow(ax, (45, 31), (49, 31), color=INK, ms=8)
    arrow(ax, (71, 31), (75, 31), color=INK, ms=8)

    note(ax, 1, 10, "6ND 是最常用的一阶估算，前向 2 次、反向 4 次，注意力部分的长序列开销另算。",
         fs=7.4, ha="left")
    note(ax, 1, 3, "把 4050 亿和 15.6 万亿代进去，得到 3.8×10$^{25}$，与 Llama 3 论文报告的训练总计算量一致。",
         fs=7.4, ha="left", color=GREEN)
    save(fig, "fig01-02-estimate.png")
