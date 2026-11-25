# -*- coding: utf-8 -*-
"""第 27 章插图：几个大模型训练作业的横向对比。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_compare"]


def _panel(fig, rect, axis="y"):
    ax = fig.add_axes(rect)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors="#4a5560", labelsize=7.2, width=0.7, length=3)
    ax.grid(axis=axis, color="#e3e7ea", lw=0.6)
    ax.set_axisbelow(True)
    return ax


def fig_compare():
    fig = plt.figure(figsize=(15.6 / 2.54, 9.0 / 2.54))

    axA = _panel(fig, [0.135, 0.315, 0.235, 0.575], axis="x")
    axB = _panel(fig, [0.480, 0.315, 0.165, 0.575])
    axC = _panel(fig, [0.745, 0.315, 0.165, 0.575])

    # ---------------- ① 集群规模（对数横轴，横向柱）
    names = ["BLOOM-176B", "OPT-175B", "DeepSeek-V3", "MegaScale", "Llama 3 405B"]
    cards = [384, 992, 2048, 12288, 16384]
    cols = [BLUE, BLUE, PURPLE, GREEN, ORANGE]
    ys = np.arange(len(names))[::-1]
    axA.barh(ys, cards, height=0.52, color=cols, edgecolor="none", zorder=3)
    for y, v in zip(ys, cards):
        axA.annotate(f"{v:,}".replace(",", " "), (v, y), va="center", ha="left",
                     fontsize=6.8, color=INK, xytext=(3, 0),
                     textcoords="offset points", zorder=4)
    axA.set_xscale("log")
    axA.set_xlim(100, 60000)
    axA.set_xticks([1000, 10000])
    axA.set_xticklabels(["1 000", "10 000"])
    axA.set_yticks(ys)
    axA.set_yticklabels(names, fontsize=6.9)
    axA.set_ylim(-0.6, len(names) - 0.4)
    axA.set_xlabel("GPU 卡数（log 尺度）", fontsize=7.4, labelpad=5)
    axA.set_title("① 规模", fontsize=8.4, color=INK, pad=5, loc="left")
    axA.tick_params(axis="y", length=0)

    # ---------------- ② 连续训练时长
    nb = ["BLOOM\n176B", "Llama 3\n405B"]
    days = [105, 54]
    xb = np.arange(len(nb))
    axB.bar(xb, days, width=0.46, color=[BLUE, ORANGE], edgecolor="none", zorder=3)
    for xi, v, tag in zip(xb, days, ["约 3.5 个月", "54 天"]):
        axB.annotate(tag, (xi, v), ha="center", va="bottom", fontsize=6.9,
                     color=INK, xytext=(0, 3), textcoords="offset points", zorder=4)
    axB.set_xticks(xb)
    axB.set_xticklabels(nb, fontsize=6.9, linespacing=1.3)
    axB.set_xlim(-0.68, 1.68)
    axB.set_ylim(0, 135)
    axB.set_ylabel("连续训练时长（天）", fontsize=7.4, labelpad=5)
    axB.set_title("② 时长", fontsize=8.4, color=INK, pad=5, loc="left")

    # ---------------- ③ 效率
    axC.bar([0], [55.2], width=0.5, color=GREEN, edgecolor="none", zorder=3)
    axC.annotate("55.2%", (0, 55.2), ha="center", va="bottom", fontsize=8.2,
                 color=GREEN, xytext=(0, 3), textcoords="offset points", zorder=4)
    axC.set_xticks([0])
    axC.set_xticklabels(["MegaScale\n12 288 卡"], fontsize=6.9, linespacing=1.3)
    axC.set_xlim(-0.68, 0.68)
    axC.set_ylim(0, 100)
    axC.set_ylabel("MFU（%）", fontsize=7.4, labelpad=5)
    axC.set_title("③ 效率", fontsize=8.4, color=INK, pad=5, loc="left")
    axC.text(0.02, 0.99, "只有这一个作业\n公布了 MFU", transform=axC.transAxes,
             fontsize=6.5, color=MUTED, ha="left", va="top", linespacing=1.5)

    fig.text(0.012, 0.130,
             "OPT-175B：992 卡，训练中发生 35 次人工重启；BLOOM-176B：384 卡，约 3.5 个月；",
             fontsize=6.7, color=MUTED, ha="left")
    fig.text(0.012, 0.086,
             "Llama 3 405B：16 384 卡、54 天、419 次意外中断；DeepSeek-V3：2 048 卡、2.788M 卡时。",
             fontsize=6.7, color=MUTED, ha="left")
    fig.text(0.012, 0.030,
             "几个数字的单位各不相同——卡数比规模、天数比稳定、MFU 比效率，不能放进同一根柱子。",
             fontsize=6.7, color=ORANGE, ha="left")

    save(fig, "fig27-01-compare.png")
