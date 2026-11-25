# -*- coding: utf-8 -*-
"""第 17 章插图：FlashAttention 的分块与在线 softmax。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_flash"]


def fig_flash():
    fig, ax = canvas(16.0, 0.60, xlim=(0, 100), ylim=(0, 100))

    label(ax, 1.0, 96.0, "（a）Q 块留在 SRAM，K/V 块轮流搬进来", fs=7.8, ha="left")

    # ---------------- HBM
    box(ax, 1.0, 8.0, 12.0, 76.0, "", fc="#f7f8fa", ec=MUTED, lw=0.9, radius=0.8)
    label(ax, 7.0, 80.5, "HBM", fs=7.4, color=MUTED, weight="bold")
    for name, y in (("Q", 66.0), ("K", 49.0), ("V", 32.0), ("O", 15.0)):
        box(ax, 3.0, y, 8.0, 9.0, name, fc="white", ec=MUTED, lw=0.7, fs=7.6,
            radius=0.5)

    # ---------------- SRAM
    box(ax, 20.0, 8.0, 22.0, 76.0, "", fc=BLUE_L, ec=BLUE, lw=1.0, radius=0.8)
    label(ax, 31.0, 80.6, "SRAM 约 228 KB/SM", fs=6.6, color=BLUE)

    box(ax, 21.6, 64.0, 18.8, 10.0, "Q 块  Br×d", fc="white", ec=BLUE, lw=0.7,
        fs=7.0)
    box(ax, 21.6, 48.0, 8.8, 10.0, "K 块" + chr(10) + "Bc×d", fc="white", ec=BLUE,
        lw=0.7, fs=6.6)
    box(ax, 31.6, 48.0, 8.8, 10.0, "V 块" + chr(10) + "Bc×d", fc="white", ec=BLUE,
        lw=0.7, fs=6.6)
    box(ax, 21.6, 27.6, 8.8, 11.4, "O 累加" + chr(10) + "Br×d", fc="white",
        ec=GREEN, lw=0.7, fs=6.4)
    box(ax, 31.6, 27.6, 8.8, 11.4, "m, l 在线" + chr(10) + "softmax",
        fc="white", ec=GREEN, lw=0.7, fs=6.2)

    # ---------------- 搬运箭头
    arrow(ax, (11.2, 70.5), (21.4, 69.0), color=BLUE, lw=0.9, ms=6)
    arrow(ax, (11.2, 53.5), (21.4, 53.0), color=BLUE, lw=0.9, ms=6)
    arrow(ax, (11.2, 36.5), (21.4, 35.0), color=BLUE, lw=0.9, ms=6)
    arrow(ax, (22.4, 27.2), (11.4, 20.0), color=GREEN, lw=0.9, ms=6, rad=-0.12)

    label(ax, 16.0, 63.0, "搬一次", fs=6.2, color=BLUE, ha="center")
    label(ax, 16.2, 45.0, "循环搬", fs=6.2, color=BLUE, ha="center")
    label(ax, 25.4, 23.6, "写回一次", fs=6.2, color=GREEN, ha="center")

    label(ax, 31.0, 44.0, "j 循环：换下一块 K/V", fs=6.2, color=MUTED)

    note(ax, 1.0, 3.2, "整张 s×s 的分数矩阵从不落到 HBM。", fs=6.6, ha="left")

    # ================================================== 右：分块矩阵
    label(ax, 55.0, 96.0, "（b）s×s 的分数矩阵被切成块，每次只算一块", fs=7.8,
          ha="left")

    sx, sy, side, n = 64.0, 33.0, 40.0, 8
    cw, chh = side * 9.6 / 16 / n, side / n          # 让格子看起来是正方形
    mw = cw * n

    for r in range(n):
        for c in range(n):
            ax.add_patch(Rectangle((sx + c * cw, sy + side - (r + 1) * chh), cw,
                                   chh, fc="#f7f8fa", ec="#e2e6ea", lw=0.4,
                                   zorder=2))
    for c in range(n):                                # 第 i 行：Q 块
        ax.add_patch(Rectangle((sx + c * cw, sy + side - chh), cw, chh,
                               fc=BLUE_L, ec="#dfe4e9", lw=0.4, zorder=3))
    ax.add_patch(Rectangle((sx + 5 * cw, sy + side - chh), cw, chh, fc=ORANGE,
                           ec=INK, lw=0.9, zorder=4))
    ax.add_patch(Rectangle((sx, sy + side - chh), mw, chh, fc="none", ec=BLUE,
                           lw=0.9, zorder=5))

    arrow(ax, (sx - 6.0, sy + side - chh / 2), (sx - 1.0, sy + side - chh / 2),
          color=BLUE, lw=0.6, style="<|-|>", ms=4)
    ax.text(sx - 3.5, sy + side + 0.6, "Br", fontsize=6.6, color=BLUE,
            ha="center", va="bottom")
    arrow(ax, (sx + 5.5 * cw, sy - 5.0), (sx + 5.5 * cw, sy - 1.0), color=ORANGE,
          lw=0.6, style="<|-|>", ms=4)
    ax.text(sx + 6.4 * cw, sy - 3.2, "Bc", fontsize=6.6, color=ORANGE, ha="left")

    ax.text(sx + mw / 2, sy + side + 3.2, "K / V 的 token（s 列）", fontsize=6.6,
            color=MUTED, ha="center", va="bottom")
    ax.text(sx - 6.6, sy + side / 2, "Q 的 token（s 行）", fontsize=6.6,
            color=MUTED, ha="center", va="center", rotation=90)

    # 两组数字
    box(ax, 54.5, 11.0, 14.5, 13.0,
        "标准实现" + chr(10) + "8192² × 2 B" + chr(10) + "= 134 MB / 头",
        fc=RED_L, ec=RED, fs=6.3, radius=0.5)
    box(ax, 80.0, 11.0, 17.0, 13.0,
        "FlashAttention" + chr(10) + "128² × 2 B" + chr(10) + "= 32 KB / 块",
        fc=GREEN_L, ec=GREEN, fs=6.3, radius=0.5)
    arrow(ax, (69.4, 17.5), (79.6, 17.5), color=MUTED, lw=0.8, ms=5)
    ax.text(74.5, 19.3, "约 4000 倍", fontsize=5.7, color=MUTED, ha="center",
            va="bottom")

    note(ax, 55.0, 6.0,
         "标准注意力要把整块分数矩阵写回 HBM 再读回来；" + chr(10)
         + "分块之后每算完一块就用在线 softmax 折进累加器，HBM 只碰 Q、K、V、O。",
         fs=6.5, ha="left")
    save(fig, "fig17-01-flash.png")
