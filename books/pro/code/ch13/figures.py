# -*- coding: utf-8 -*-
"""第 13 章插图：Ring Attention 与 Ulysses 的切分方式。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_cp"]

CARD = [BLUE, ORANGE, GREEN, PURPLE]
CARD_L = [BLUE_L, ORANGE_L, GREEN_L, PURPLE_L]


def fig_cp():
    fig, ax = canvas(16.0, 0.68, xlim=(0, 100), ylim=(0, 100))

    # ================================================== 左：Ring Attention
    label(ax, 1.0, 96.5, "（a）Ring Attention：Q 各留一块，KV 绕环传",
          fs=7.8, ha="left")

    bx = [2.0, 12.6, 23.2, 33.8]
    bw, bh, by = 9.4, 12.0, 72.0
    for i, x in enumerate(bx):
        box(ax, x, by, bw, bh, "", fc=CARD_L[i], ec=CARD[i], lw=0.9, radius=0.8)
        label(ax, x + bw / 2, by + bh - 3.4, f"卡 {i}", fs=7.4, color=CARD[i],
              weight="bold")
        label(ax, x + bw / 2, by + 4.4, f"Q{i} 常驻", fs=7.0, color=INK)

    for i in range(3):
        x1, x2 = bx[i] + bw, bx[i + 1]
        arrow(ax, (x1 + 0.5, by + bh / 2 - 1.4), (x2 - 0.4, by + bh / 2 - 1.4),
              color=MUTED, lw=0.9, ms=6)
    label(ax, (bx[0] + bw + bx[3]) / 2, by + bh + 2.2,
          "每一步把本地的 KV 块交给下一张卡", fs=6.8, color=MUTED)

    arrow(ax, (bx[3] + bw / 2, by - 1.2), (bx[0] + bw / 2, by - 1.2),
          color=MUTED, lw=0.7, ms=5, rad=-0.22, ls=(0, (2, 2)), alpha=0.85)
    label(ax, (bx[0] + bw + bx[3]) / 2, by - 8.6, "转满 4 步回到原处", fs=6.4,
          color=MUTED)

    # KV 轮转表
    gx, gy, cw, ch = 10.0, 14.0, 9.0, 7.0
    top = gy + 4 * ch
    label(ax, 1.0, top + 6.0, "每一步各卡手里的 KV 块", fs=6.8, color=MUTED,
          ha="left")
    for c in range(4):
        label(ax, gx + (c + 0.5) * cw, top + 2.4, f"卡 {c}", fs=6.6, color=CARD[c])
    for r in range(4):
        y = gy + (3 - r) * ch
        label(ax, gx - 2.0, y + ch / 2, f"第 {r + 1} 步", fs=6.6, color=MUTED,
              ha="right")
        for c in range(4):
            k = (c + r) % 4
            box(ax, gx + c * cw + 0.4, y + 0.4, cw - 0.8, ch - 0.8,
                f"KV{k}", fc=CARD_L[k], ec=CARD[k], lw=0.7, fs=6.8, radius=0.4)

    note(ax, 1.0, 7.0,
         "每张卡始终只存本地 Q 和两块 KV（自己的一块 + 正转进来的一块），\n"
         "注意力要在完整序列上做，所以必须转满一圈。", fs=7.0, ha="left")

    ax.plot([49.0, 49.0], [30, 94], color=FAINT, lw=0.7, ls=(0, (3, 3)))

    # ================================================== 右：Ulysses
    label(ax, 51.0, 96.5, "（b）Ulysses：先按序列切，all-to-all 后按头切",
          fs=7.8, ha="left")

    rx = [51.5, 63.0, 74.5, 86.0]
    rw = 10.2
    cell = (rw - 2.6) / 4

    def mini(x, y, kind, me):
        for r in range(4):
            for c in range(4):
                on = (c == me) if kind == "seq" else (r == me)
                xx = x + 1.3 + c * cell
                yy = y + 1.0 + (3 - r) * cell
                ax.add_patch(Rectangle((xx, yy), cell + 0.02, cell,
                                       fc=(CARD[me] if on else "#f6f7f9"),
                                       ec=(CARD[me] if on else "#e3e7ea"),
                                       lw=0.4, zorder=3))

    for i, x in enumerate(rx):
        box(ax, x, 74.0, rw, 15.0, "", fc="white", ec=CARD[i], lw=0.9, radius=0.8)
        mini(x, 75.0, "seq", i)
        label(ax, x + rw / 2, 87.0, f"卡 {i}", fs=6.6, color=CARD[i])

    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            arrow(ax, (rx[i] + rw / 2, 73.7), (rx[j] + rw / 2, 66.6),
                  color=FAINT, lw=0.5, ms=4, z=1)
    label(ax, 73.0, 70.2, "all-to-all", fs=6.9, color=MUTED, ha="center",
          bbox=dict(fc="white", ec="none", pad=1.6))

    for i, x in enumerate(rx):
        box(ax, x, 46.5, rw, 16.5, "", fc="white", ec=CARD[i], lw=0.9, radius=0.8)
        mini(x, 47.4, "head", i)
        label(ax, x + rw / 2, 59.8, f"卡 {i}" + chr(10) + "头 1/4", fs=6.2,
              color=CARD[i])

    box(ax, 51.5, 31.0, 44.7, 9.6,
        "各卡在完整序列上算自己那 1/4 头的注意力" + chr(10) + "计算期间不再通信",
        fc=BLUE_L, ec=BLUE, fs=6.9)
    for x in rx:
        arrow(ax, (x + rw / 2, 46.2), (x + rw / 2, 41.8), color=BLUE, lw=0.7, ms=5)

    note(ax, 51.0, 24.5,
         "算完再用一次反向的 all-to-all 把序列切回来。代价是两次全交换，\n"
         "换来的是注意力本身完全并行。", fs=7.0, ha="left")
    note(ax, 51.0, 15.0,
         "小格：4 行 = 4 组头，4 列 = 4 段序列。\n"
         "左图每卡占一列，右图每卡占一行。", fs=6.8, ha="left", color=MUTED)

    note(ax, 1.0, 1.6,
         "两者都把长序列摊到多卡：Ring Attention 只搬 KV、通信量小但要串行转圈；"
         "Ulysses 一次全交换、通信量大但每卡只算一部分头。", fs=7.0, ha="left")
    save(fig, "fig13-01-cp.png")
