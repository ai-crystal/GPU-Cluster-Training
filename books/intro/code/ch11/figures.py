# -*- coding: utf-8 -*-
"""第 11 章插图：Llama 3 的故障分类与故障传导。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_failures", "fig_chain"]


def fig_failures():
    fig, ax = chart(15.6, 9.0)
    items = [("GPU 本体", 148), ("GPU 显存 HBM3", 72), ("软件缺陷", 54),
             ("交换机与线缆", 35), ("主机非计划维护", 32), ("GPU 片上 SRAM", 19),
             ("GPU 系统处理器", 17), ("网卡", 7), ("NCCL 看门狗超时", 7),
             ("静默数据损坏", 6), ("GPU 温度传感器", 6), ("其他", 16)]
    labels = [k for k, _ in items][::-1]
    vals = [v for _, v in items][::-1]
    colors = [RED if "GPU" in k else (ORANGE if "网卡" in k or "交换机" in k else MUTED)
              for k in labels]
    hbars(ax, labels, vals, colors=colors, height=0.62, fs=7.4, fmt="{:.0f}", xmax=180)
    ax.set_xlabel("54 天内的中断次数（共 419 次意外中断）", fontsize=8.2)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e3e7ea", lw=0.6)
    ax.grid(axis="y", visible=False)
    anote(ax, 0.01, -0.16, "数据来自 Llama 3 论文的表 5，按根因归类；GPU 相关故障合计占 58.7%。",
          fs=7.0, va="top")
    save(fig, "fig11-01-failures.png")


def fig_chain():
    fig, ax = canvas(16.0, 0.33, xlim=(0, 100), ylim=(20, 100))
    steps = [("一张卡报错\n或掉线", BLUE), ("NCCL 集合通信\n等不到这一份", BLUE),
             ("超时，整个作业\n挂起", ORANGE), ("所有卡重启\n回滚到检查点", RED),
             ("损失几分钟\n到几十分钟", RED)]
    x = 2
    for i, (text, color) in enumerate(steps):
        box(ax, x, 44, 16, 26, text, fc="white", ec=color, fs=7.4, color=color)
        if i < len(steps) - 1:
            arrow(ax, (x + 16.4, 57), (x + 18.6, 57), color=MUTED, ms=7)
        x += 19.4

    note(ax, 2, 34, "任何一张卡出问题，都可能让整步训练无法完成；真正贵的是它引发的停顿与回滚。",
         fs=7.4, ha="left")
    save(fig, "fig11-02-chain.png")
