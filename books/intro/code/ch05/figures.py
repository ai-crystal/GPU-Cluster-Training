# -*- coding: utf-8 -*-
"""第 5 章插图：浮点格式的位分配。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_formats"]


def fig_formats():
    fig, ax = canvas(16.0, 0.5, xlim=(0, 100), ylim=(0, 100))
    bit = 2.15
    x0 = 26
    rows = [
        ("FP32", 1, 8, 23, 32, MUTED),
        ("TF32", 1, 8, 10, 32, PURPLE),
        ("BF16", 1, 8, 7, 16, BLUE),
        ("FP16", 1, 5, 10, 16, GREEN),
        ("FP8 E4M3", 1, 4, 3, 8, ORANGE),
        ("FP8 E5M2", 1, 5, 2, 8, RED),
    ]
    top = 88
    gap = 13.2
    for i, (name, s, e, m, total, color) in enumerate(rows):
        y = top - i * gap
        ax.text(x0 - 2.5, y + 3, name, ha="right", va="center", fontsize=8.0, color=INK)
        x = x0
        for (nbit, lab, fc) in ((s, "符", "#e6e9ec"), (e, "指数", color), (m, "尾数", "#f6f7f8")):
            w = nbit * bit
            ax.add_patch(Rectangle((x, y), w, 6.2, fc=fc, ec="white", lw=1.0, zorder=3))
            if nbit >= 4:
                ax.text(x + w / 2, y + 3.1, lab, ha="center", va="center",
                        fontsize=6.8, color="white" if fc == color else INK, zorder=4)
            x += w
        used = (s + e + m)
        ax.text(x + 1.8, y + 3.1, f"{used} 位" + ("（存在 32 位容器里）" if name == "TF32" else ""),
                ha="left", va="center", fontsize=7.0, color=MUTED)

    # 位宽刻度（以 FP32 为基准）
    ax.plot([x0, x0 + 32 * bit], [93.5, 93.5], color=FAINT, lw=0.7)
    for b in range(0, 33, 8):
        ax.plot([x0 + b * bit, x0 + b * bit], [93.5, 94.6], color=FAINT, lw=0.7)
        ax.text(x0 + b * bit, 95.2, str(b), ha="center", fontsize=6.2, color=MUTED)

    note(ax, 1, 6, "符号位管正负，指数位管范围，尾数位管精度。BF16 保留了 FP32 的 8 位指数，所以范围和 FP32 一样，\n"
                   "只是尾数从 23 位砍到 7 位；FP16 的指数只有 5 位，范围小得多，训练时容易溢出。FP8 的两套格式\n"
                   "在范围和精度之间做了不同取舍，E4M3 精度高一点，E5M2 范围大一点。",
         fs=7.4, ha="left")
    save(fig, "fig05-01-formats.png")
