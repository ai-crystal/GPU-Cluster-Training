# -*- coding: utf-8 -*-
"""第 14 章插图：MoE 的两次 all-to-all 与容量因子。"""
from common import *  # noqa: F401,F403

import numpy as np

FIGURES = ["fig_moe"]

EXP = [BLUE, ORANGE, GREEN, PURPLE]
EXP_L = [BLUE_L, ORANGE_L, GREEN_L, PURPLE_L]

# 每张卡的本地 token 分别要送给哪个专家（示意用）
TOKENS = [[0, 1, 2, 0], [1, 2, 3, 3], [0, 2, 1, 3], [2, 0, 3, 1]]


def fig_moe():
    fig, ax = canvas(16.0, 0.62, xlim=(0, 100), ylim=(0, 100))

    xs = [1.2, 11.9, 22.6, 33.3]
    w = 10.0

    label(ax, 1.0, 97.5, "（a）两次 all-to-all 把 token 送去算、再送回来", fs=7.8,
          ha="left")

    def dots(x, colors, y, pitch=2.3, s=1.9):
        for i, c in enumerate(colors):
            ax.add_patch(Circle((x + i * pitch, y), s / 2, fc=c, ec="white",
                                lw=0.4, zorder=4))

    def dot_x(i, k):
        return xs[i] + w / 2 - 3.85 + k * 2.3

    # 第一行：本地 token
    for i, x in enumerate(xs):
        box(ax, x, 82.0, w, 11.0, "", fc="#fbfcfd", ec=MUTED, lw=0.7, radius=0.6)
        label(ax, x + w / 2, 90.2, f"卡 {i}", fs=6.6, color=MUTED)
        dots(x + w / 2 - 3.85, [EXP[k] for k in TOKENS[i]], 85.4)

    # all-to-all ①
    for i in range(4):
        for k, e in enumerate(TOKENS[i]):
            arrow(ax, (dot_x(i, k), 81.5), (xs[e] + w / 2 + 0.4, 71.5),
                  color=EXP[e], lw=0.55, ms=4, alpha=0.6, z=1)
    label(ax, 25.0, 76.8, "all-to-all ①：按 token 要去的专家重新分布",
          fs=6.8, color=INK, bbox=dict(fc="white", ec="none", pad=1.6))

    # 第二行：专家并行计算
    for j, x in enumerate(xs):
        box(ax, x, 53.0, w, 17.6, "", fc=EXP_L[j], ec=EXP[j], lw=0.9, radius=0.8)
        label(ax, x + w / 2, 68.2, f"卡 {j}", fs=6.6, color=EXP[j])
        box(ax, x + 2.0, 55.2, w - 4.0, 8.4,
            "专家 E" + str(j) + chr(10) + "MLP", fc="white", ec=EXP[j],
            lw=0.6, fs=6.2, radius=0.5)
        dots(x + w / 2 - 3.85, [EXP[j]] * 4, 65.0)

    # all-to-all ②
    for i in range(4):
        for j in range(4):
            arrow(ax, (xs[j] + w / 2, 52.5), (xs[i] + w / 2 - 3.5, 40.2),
                  color=FAINT, lw=0.5, ms=3.5, z=1)
    label(ax, 25.0, 46.2, "all-to-all ②：算完按原路送回", fs=6.8, color=INK,
          bbox=dict(fc="white", ec="none", pad=1.6))

    # 第三行：结果回到原卡
    for i, x in enumerate(xs):
        box(ax, x, 28.6, w, 10.6, "", fc="#fbfcfd", ec=MUTED, lw=0.7, radius=0.6)
        label(ax, x + w / 2, 36.6, f"卡 {i}", fs=6.6, color=MUTED)
        dots(x + w / 2 - 3.85, [EXP[k] for k in TOKENS[i]], 32.2)

    note(ax, 1.0, 21.6, "点的颜色＝这个 token 要去的专家。", fs=6.8, ha="left")
    note(ax, 1.0, 17.4, "算完的结果回到原卡，在本卡上加权合并。", fs=6.8, ha="left")
    note(ax, 1.0, 13.0,
         "两次 all-to-all 的流量都等于「token 数 × 隐藏维 × 2 字节」。",
         fs=6.8, ha="left", color=ORANGE)
    note(ax, 1.0, 8.4, "分到超过配额的 token 只能丢掉。", fs=6.8, ha="left")

    # ============================================== 右：容量因子
    ax2 = fig.add_axes([0.560, 0.175, 0.370, 0.655])
    for side in ("top", "right"):
        ax2.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax2.spines[side].set_color(MUTED)
    ax2.tick_params(colors="#4a5560", labelsize=7.2, width=0.7, length=3)
    ax2.grid(axis="y", color="#e3e7ea", lw=0.6, zorder=0)
    ax2.set_axisbelow(True)

    cv = np.linspace(0.02, 1.2, 300)
    grid = np.linspace(1e-4, 60, 8000)

    def drop(frac, cap):
        """对数正态专家负载模型：均值归一为 1，超出容量 C 的 token 被丢弃。"""
        sig = np.sqrt(np.log(1 + frac ** 2))
        mu = -sig ** 2 / 2
        pdf = np.exp(-(np.log(grid) - mu) ** 2 / (2 * sig ** 2))
        pdf /= (grid * sig * np.sqrt(2 * np.pi))
        return np.trapezoid(np.maximum(0, grid - cap) * pdf, grid) * 100

    for cap, color, name in ((1.0, RED, "C = 1.0"),
                             (1.25, ORANGE, "C = 1.25"),
                             (2.0, GREEN, "C = 2.0")):
        y = np.array([drop(f, cap) for f in cv])
        ax2.plot(cv, y, color=color, lw=1.6, zorder=3)
        ax2.text(1.215, y[-1], name, color=color, fontsize=7.1, ha="left",
                 va="center")

    ax2.set_xlim(0, 1.36)
    ax2.set_ylim(0, 40)
    ax2.set_xticks([0, 0.3, 0.6, 0.9, 1.2])
    ax2.set_yticks([0, 10, 20, 30, 40])
    ax2.set_xlabel("专家负载不均衡系数（变异系数 CV）", fontsize=7.4, labelpad=4)
    ax2.set_ylabel("被丢弃的 token 比例（%）", fontsize=7.4, labelpad=5)
    ax2.annotate("容量卡得越紧，" + chr(10) + "负载一抖就丢 token", xy=(0.31, 11.9),
                 xytext=(0.07, 30.0), fontsize=6.8, color=INK, ha="left",
                 arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.6,
                                 connectionstyle="arc3,rad=-0.2"))

    ax2.set_title("（b）容量因子与丢弃率", fontsize=7.8, color=INK, loc="left", pad=7)

    anote(ax2, -0.02, -0.20,
          "按对数正态专家负载模型估算（均值归一到 1；容量 C = 每专家配额 / 平均 token 数）。",
          fs=6.4, va="top")
    save(fig, "fig14-01-moe.png")
