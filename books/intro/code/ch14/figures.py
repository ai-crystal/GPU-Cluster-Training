# -*- coding: utf-8 -*-
"""第 14 章插图：调度流程与成本。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_sched", "fig_cost"]


def fig_sched():
    fig, ax = canvas(16.0, 0.40, xlim=(0, 100), ylim=(20, 100))

    box(ax, 2, 62, 22, 22, "作业队列\n按优先级排队", fc=BLUE_L, ec=BLUE, fs=7.6)
    box(ax, 28, 62, 24, 22, "资源匹配\ngang scheduling", fc=PURPLE_L, ec=PURPLE, fs=7.6)
    box(ax, 56, 62, 22, 22, "拓扑分配\n同一机架优先", fc=GREEN_L, ec=GREEN, fs=7.6)
    box(ax, 82, 62, 16, 22, "启动\n训练", fc=ORANGE_L, ec=ORANGE, fs=7.6)

    for x in (24, 52, 78):
        arrow(ax, (x + 0.4, 73), (x + 3.6, 73), color=INK, ms=8)

    for i in range(6):
        box(ax, 4 + i * 4.6, 40, 3.6, 6, "", fc=BLUE_L, ec=BLUE, lw=0.7, radius=0.4)
    ax.text(16, 33, "排队的作业", ha="center", fontsize=7.0, color=MUTED)

    for i in range(10):
        box(ax, 40 + i * 5.2, 38, 4.2, 10, "", fc="#f2f4f6", ec=MUTED, lw=0.7, radius=0.4)
    ax.text(66, 33, "集群里的空闲资源", ha="center", fontsize=7.0, color=MUTED)

    note(ax, 2, 24, "作业要么一次拿到全部卡，要么继续等；碎片太多时，总数够也拼不出一个完整作业。",
         fs=7.4, ha="left")
    save(fig, "fig14-01-sched.png")


def fig_cost():
    fig, ax = chart(15.4, 7.2)
    names = ["1 千卡", "5 千卡", "1 万卡", "1.6 万卡"]
    cards = [1000, 5000, 10000, 16384]
    cost = [c * 2 * 24 / 1000 for c in cards]  # 千美元/天
    bars(ax, names, cost, colors=[MUTED, BLUE, ORANGE, RED], width=0.5,
         fmt="{:.0f} 千美元/天", fs=8.0)
    ax.set_ylabel("每天的 GPU 租金（千美元）", fontsize=8.2, labelpad=7)
    ax.set_ylim(0, 900)
    ax.grid(axis="x", visible=False)
    anote(ax, 0.01, -0.14, "按每卡每小时 2 美元估算，只算卡时，不含网络、存储、电力和人力。",
          fs=7.0, va="top")
    save(fig, "fig14-02-cost.png")
