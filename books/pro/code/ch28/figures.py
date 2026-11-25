# -*- coding: utf-8 -*-
"""第 28 章插图：从一台机器到正式训练的启动顺序。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_launch"]


def fig_launch():
    fig, ax = canvas(16.0, 0.62)

    stages = [
        ("① 单机自检", "1 台 / 8 卡", MUTED,
         ["驱动版本一致", "8 卡全部识别", "NVLink 达标", "显存压测通过"]),
        ("② 单节点跑通", "1 节点 / 8 卡", BLUE,
         ["单机跑通前反向", "all-reduce 达标", "loss 与单卡对齐", "显存留有余量"]),
        ("③ 双节点", "2 节点 / 16 卡", GREEN,
         ["跨机 NCCL 建链", "IB 带宽与时延", "16 卡收敛一致", "拔线触发告警"]),
        ("④ 全规模短跑", "目标卡数 / 百步", ORANGE,
         ["扩到目标卡数", "步时长按预期", "检查点读写验证", "监控告警打通"]),
        ("⑤ 正式训练", "全规模 / 长跑", RED,
         ["锁定镜像版本", "检查点策略定稿", "值班交接完成", "记录基线 MFU"]),
    ]

    bx, bw, gap = 2.0, 16.6, 3.2
    by = [58.0, 65.5, 73.0, 80.5, 88.0]
    bh = 7.6

    for i, ((title, scale, color, items), y) in enumerate(zip(stages, by)):
        x = bx + i * (bw + gap)
        box(ax, x, y, bw, bh, fc="white", ec=color, lw=1.0, radius=1.0)
        label(ax, x + bw / 2, y + 4.9, title, fs=7.6, color=color)
        label(ax, x + bw / 2, y + 1.9, scale, fs=6.4, color=MUTED)

        # 阶梯之间
        if i < len(stages) - 1:
            arrow(ax, (x + bw + 0.3, y + bh / 2), (x + bw + gap - 0.3, y + bh / 2 + 7.5),
                  color=MUTED, lw=0.7, ms=5)

        # 连到验收清单
        ax.plot([x + bw / 2, x + bw / 2], [y, 50.0], color=color, lw=0.6,
                ls=(0, (2, 2)), zorder=1)

        # 清单
        box(ax, x, 8.0, bw, 42.0, fc="#f8f9fa", ec=FAINT, lw=0.6, radius=1.0)
        label(ax, x + bw / 2, 46.4, "验收项", fs=6.4, color=MUTED)
        iy = 40.0
        for it in items:
            ax.add_patch(Rectangle((x + 1.3, iy - 0.6), 1.3, 1.3, fc="white",
                                   ec=color, lw=0.6, zorder=3))
            label(ax, x + 3.0, iy, it, fs=6.4, color=INK, ha="left")
            iy -= 8.4

    label(ax, 2.0, 3.4,
          "每一级只在前一级全部通过后才放行；全规模短跑是唯一能在几分钟内暴露跨机问题的地方。",
          fs=6.9, color=MUTED, ha="left")

    save(fig, "fig28-01-launch.png")
