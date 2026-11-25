# -*- coding: utf-8 -*-
"""第 5 章插图：FP8 训练的量化流程与回退分支。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_fp8"]


def fig_fp8():
    fig, ax = canvas(16.0, 0.66, xlim=(0, 100), ylim=(0, 100))

    w, gap = 20.5, 4.6
    xs = [2.0, 2.0 + w + gap, 2.0 + 2 * (w + gap), 2.0 + 3 * (w + gap)]
    y1, h = 68, 16

    box(ax, xs[0], y1, w, h, "① 张量（BF16）", fc=BLUE_L, ec=BLUE, fs=7.0)
    box(ax, xs[1], y1, w, h, "② 统计 amax", fc=BLUE_L, ec=BLUE, fs=7.0)
    box(ax, xs[2], y1, w, h, "③ 缩放因子\ns = 448 / amax", fc=BLUE_L, ec=BLUE, fs=7.0)
    box(ax, xs[3], y1, w, h, "④ 量化到 FP8\nE4M3（±448）", fc=ORANGE_L, ec=ORANGE, fs=7.0)

    for i in range(3):
        arrow(ax, (xs[i] + w + 0.4, y1 + h / 2), (xs[i + 1] - 0.4, y1 + h / 2), ms=7)

    # 第二行（右 → 左）
    y2 = 42
    box(ax, xs[3], y2, w, h, "⑤ FP8 矩阵乘", fc=ORANGE_L, ec=ORANGE, fs=7.0)
    box(ax, xs[2], y2, w, h, "⑥ 反量化\n乘回 1/s", fc=GREEN_L, ec=GREEN, fs=7.0)
    box(ax, xs[1], y2, w, h, "⑦ FP32 累加", fc=GREEN_L, ec=GREEN, fs=7.0)
    box(ax, xs[0], y2, w, h, "⑧ 更新参数\n（BF16 主权重）", fc=GREEN_L, ec=GREEN, fs=7.0)

    # ④ → ⑤ 的折线
    xm = xs[3] + w / 2
    ax.plot([xm, xm], [y1 - 0.3, y2 + h + 3.2], color=INK, lw=0.9, zorder=2)
    ax.plot([xm, xs[3] + w / 2], [y2 + h + 3.2, y2 + h + 3.2], color=INK, lw=0.9, zorder=2)
    ax.plot([xs[3] + w / 2, xs[3] + w / 2], [y2 + h + 3.2, y2 + h + 3.2], color=INK, lw=0.9)
    arrow(ax, (xm, y2 + h + 3.2), (xm, y2 + h + 0.4), ms=7)

    for i in range(3):
        arrow(ax, (xs[3 - i] - 0.4, y2 + h / 2), (xs[2 - i] + w + 0.4, y2 + h / 2), ms=7)

    # 回退分支
    arrow(ax, (88.0, y2 - 0.4), (88.0, 23.4), color=RED, lw=0.9, ms=6, ls=(0, (4, 2)))
    label(ax, 90.0, 33.0, "溢出", fs=6.6, color=RED, ha="left")

    box(ax, 56, 9, 42, 14, "amax 溢出或出现 NaN / Inf\n整层回退 BF16 计算（慢，但不错）",
        fc=RED_L, ec=RED, fs=6.8, color=RED)

    # 回退后直接进累加
    ax.plot([55.6, 47.5], [16.0, 16.0], color=RED, lw=0.9, ls=(0, (4, 2)), zorder=2)
    arrow(ax, (47.5, 16.0), (37.0, y2 - 0.4), color=RED, lw=0.9, ms=6,
          ls=(0, (4, 2)), rad=-0.3)

    # 左侧说明
    note(ax, 1.8, 31.0, "FP8 只用在矩阵乘的输入上，", fs=6.9, ha="left")
    note(ax, 1.8, 26.5, "累加、权重更新始终是", fs=6.9, ha="left")
    note(ax, 1.8, 22.0, "BF16 / FP32，所以精度", fs=6.9, ha="left")
    note(ax, 1.8, 17.5, "损失主要来自量化误差。", fs=6.9, ha="left")

    note(ax, 1.8, 3.0,
         "E4M3 只有 3 位尾数，单次量化的相对误差约 2⁻⁴；靠每张量（或每 128 元素一块）独立算 s 把动态范围摊开。",
         fs=6.8, ha="left")
    save(fig, "fig05-01-fp8.png")
