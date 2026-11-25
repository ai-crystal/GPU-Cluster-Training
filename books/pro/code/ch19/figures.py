# -*- coding: utf-8 -*-
"""第 19 章插图：训练数据管线的四道关口。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_dataloader"]

STAGES = [
    ("① 存储", "对象存储 / 本地盘" + chr(10) + "小文件、随机读"),
    ("② 预处理", "解码、分词、过滤" + chr(10) + "吃 CPU"),
    ("③ 打包", "拼接成定长序列" + chr(10) + "多次拷贝"),
    ("④ 主机内存", "pinned 缓冲区" + chr(10) + "异步 H2D"),
    ("⑤ GPU", "前向反向计算" + chr(10) + "等着吃数据"),
]

TIPS = [(0, "小文件随机读，IOPS 打满"),
        (1, "解码分词挤在单核上"),
        (2, "拼接与对齐各拷一次"),
        (3, "没有 pinned 就同步阻塞")]


def fig_dataloader():
    fig, ax = canvas(16.0, 0.56, xlim=(0, 100), ylim=(0, 100))

    label(ax, 1.0, 95.0, "（a）数据从存储走到 GPU，中间有四道容易堵的关口", fs=7.8,
          ha="left")

    w, gap, n = 15.0, 4.0, 5
    x0 = (100 - (n * w + (n - 1) * gap)) / 2
    yb, h = 68.0, 17.0
    for i, (title, body) in enumerate(STAGES):
        x = x0 + i * (w + gap)
        fc = GREEN_L if i == n - 1 else "white"
        ec = GREEN if i == n - 1 else MUTED
        box(ax, x, yb, w, h, "", fc=fc, ec=ec, lw=0.9, radius=0.7)
        label(ax, x + w / 2, yb + h - 4.4, title, fs=6.8, weight="bold",
              color=(GREEN if i == n - 1 else INK))
        label(ax, x + w / 2, yb + 5.2, body, fs=6.0, color=MUTED)
        if i < n - 1:
            arrow(ax, (x + w + 0.4, yb + h / 2), (x + w + gap - 0.4, yb + h / 2),
                  color=INK, lw=0.9, ms=6)

    # 关口说明
    for i, (k, txt) in enumerate(TIPS):
        x = x0 + k * (w + gap) + w / 2
        ty = 57.6 if i % 2 == 0 else 51.6
        ax.plot([x, x], [yb - 1.2, ty + 1.8], color=FAINT, lw=0.7, zorder=1)
        label(ax, x, ty, txt, fs=6.2, color=RED, ha="center")

    # ---------------- GPU 时间线
    label(ax, 1.0, 41.0, "（b）任何一道关口供不上，GPU 就空转", fs=7.8, ha="left")
    y0, hh = 22.0, 10.0
    x = 12.0
    gaps = []
    for k in range(7):
        if k in (2, 4):
            ax.add_patch(Rectangle((x, y0), 3.6, hh, fc="#f4f5f7", ec=FAINT,
                                   lw=0.6, ls=(0, (2, 2)), zorder=2))
            gaps.append(x + 1.8)
            x += 3.6
        ax.add_patch(Rectangle((x, y0), 8.0, hh, fc=BLUE, ec="white", lw=0.7,
                               zorder=3))
        x += 8.0
    label(ax, 10.6, y0 + hh / 2, "GPU", fs=6.8, color=MUTED, ha="right")
    for gx in gaps:
        label(ax, gx, y0 + hh / 2, "空转", fs=5.8, color=RED, rotation=90)

    arrow(ax, (gaps[0], y0 - 1.2), (gaps[0] + 2.0, 14.0), color=RED, lw=0.7,
          ms=5, rad=0.25)
    label(ax, gaps[0] + 2.6, 13.2, "数据还没送到，计算单元只能等", fs=6.3,
          color=RED, ha="left", va="center")

    anote(ax, 0.01, 0.04,
          "整条管线的吞吐由最慢的一段决定：存储读得再快，CPU 解不动也会堵；"
          "CPU 再快，同步 H2D 拷贝一样让 GPU 干等。",
          fs=6.8, va="top")
    save(fig, "fig19-01-dataloader.png")
