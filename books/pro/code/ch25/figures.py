# -*- coding: utf-8 -*-
"""第 25 章插图：监控指标的四层分工。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_metrics"]


def fig_metrics():
    fig, ax = canvas(16.0, 0.60)

    bands = [
        ("集群层", "整片集群：还有多少算力在跑", BLUE,
         ["在线卡数", "总功耗", "网络吞吐", "作业队列"]),
        ("节点层", "哪台机器、哪张卡先不对", GREEN,
         ["GPU 利用率", "显存", "温度", "ECC 与 XID"]),
        ("进程层", "这一步慢在算还是通信", ORANGE,
         ["步时长", "通信耗时", "tokens/s", "数据等待"]),
        ("内核层", "哪个 kernel 没打满", PURPLE,
         ["SM 占用率", "HBM 带宽", "实测 FLOPS", "kernel 耗时"]),
    ]
    ys = [74.0, 52.0, 30.0, 8.0]
    h = 16.0

    for (name, sub, color, chips), y in zip(bands, ys):
        ax.add_patch(Rectangle((2.0, y), 96.0, h, fc=color, ec="none",
                               alpha=0.05, zorder=1))
        ax.add_patch(Rectangle((2.0, y), 1.8, h, fc=color, ec="none", zorder=2))
        label(ax, 5.6, y + 10.8, name, fs=8.6, color=color, ha="left")
        label(ax, 5.6, y + 5.4, sub, fs=6.6, color=MUTED, ha="left")
        for i, chip in enumerate(chips):
            box(ax, 30.0 + i * 16.7, y + 3.6, 15.5, 8.8, chip, fc="white",
                ec=color, lw=0.7, fs=6.8, color=INK, radius=0.8)

    for y in (68.0, 46.0, 24.0):
        arrow(ax, (24.0, y + 5.4), (24.0, y + 0.8), color=MUTED, lw=0.8, ms=6)

    label(ax, 2.0, 3.0,
          "上一层只能告诉你“哪里不对”，下一层才回答“为什么”。指标必须跨层对齐同一个时间窗，否则只能各说各话。",
          fs=6.9, color=MUTED, ha="left")

    save(fig, "fig25-01-metrics.png")
