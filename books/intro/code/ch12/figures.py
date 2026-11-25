# -*- coding: utf-8 -*-
"""第 12 章插图：静默数据损坏的传播路径。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_sdc"]


def fig_sdc():
    fig, ax = canvas(16.0, 0.38, xlim=(0, 100), ylim=(20, 100))

    stages = [
        ("显存某一位\n翻转", "一个 0 变成 1\n没有报错", RED, 4),
        ("一次矩阵乘\n结果偏了", "误差很小，\n梯度看不出异常", ORANGE, 22),
        ("参数被污染", "几千步之后\n偏差累积", PURPLE, 40),
        ("损失突然\n发散", "此时已经\n很难回溯", BLUE, 58),
        ("只能回滚\n到旧检查点", "几十小时的\n计算作废", MUTED, 76),
    ]
    for text, sub, color, x in stages:
        box(ax, x, 54, 18, 22, text, fc="white", ec=color, fs=7.6, color=color)
        ax.text(x + 9, 46, sub, ha="center", va="top", fontsize=6.8, color=MUTED,
                linespacing=1.5)
    for x in (22, 40, 58, 76):
        arrow(ax, (x - 0.4, 65), (x + 1.6, 65), color=MUTED, ms=6)

    note(ax, 2, 34, "静默数据损坏不产生异常码，监控上也看不出错误，只能从结果反推。",
         fs=7.4, ha="left")
    save(fig, "fig12-01-sdc.png")
