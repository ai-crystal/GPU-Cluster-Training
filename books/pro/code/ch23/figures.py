# -*- coding: utf-8 -*-
"""第 23 章插图：训练异常的排查顺序。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_triage"]


def fig_triage():
    fig, ax = canvas(16.0, 0.68)

    stages = [
        ("① 先看 loss 形态", "发散 / 尖峰 / 长时间不降", BLUE,
         "冻结现场：存下最近 100 步的 loss 与 lr 记录，标出第一个异常 step。\n"
         "能复现就缩到单机复现；不能复现就比对环境与配置差异。"),
        ("② 再查数据", "长度 / padding / 重复样本", BLUE,
         "抽样出问题的那几个批次：看长度突变、重复率、tokenizer 边界。\n"
         "修好数据管道，回滚到该 step 重跑。"),
        ("③ 查数值", "梯度范数 / 激活量级", PURPLE,
         "梯度范数尖峰 → 降 lr、收紧裁剪；\n"
         "激活溢出 → 调 loss scale 与 bf16 策略；必要时在该层加日志。"),
        ("④ 最后查硬件", "ECC / XID / SDC 重算", RED,
         "同一 rank 反复报错 → 下线换卡；XID、ECC 交运维换件。\n"
         "怀疑静默数据损坏（SDC）时，就用重算同一批数据校验。"),
    ]
    ys = [78.0, 56.0, 34.0, 12.0]
    h = 16.0

    for i, ((title, sub, color, act), y) in enumerate(zip(stages, ys)):
        box(ax, 2.0, y, 34.0, h, fc="white", ec=color, lw=1.0, radius=1.2)
        label(ax, 4.0, y + 10.4, title, fs=8.6, color=color, ha="left")
        label(ax, 4.0, y + 4.8, sub, fs=6.7, color=MUTED, ha="left")

        # 正常向下，异常向右
        if i < len(stages) - 1:
            arrow(ax, (19.0, y - 0.4), (19.0, y - 5.6), color=GREEN, lw=0.8, ms=6)
            label(ax, 20.4, y - 3.0, "正常", fs=6.4, color=GREEN, ha="left")

        arrow(ax, (36.4, y + h / 2), (40.8, y + h / 2), color=color, lw=0.9, ms=7)
        label(ax, 38.6, y + h / 2 + 1.8, "异常", fs=6.4, color=color)

        box(ax, 41.0, y, 57.0, h, fc="white", ec=FAINT, lw=0.7, radius=1.0)
        box(ax, 41.0, y, 1.6, h, fc=color, ec="none", radius=0.0)
        label(ax, 43.6, y + h / 2, act, fs=6.7, color=INK, ha="left", va="center")

    label(ax, 2.0, 4.0,
          "顺序的道理：越便宜的检查越先做。先排除自己刚改过的代码和数据，再花几个小时去怀疑一张可能坏了的卡。",
          fs=6.9, color=MUTED, ha="left")

    save(fig, "fig23-01-triage.png")
