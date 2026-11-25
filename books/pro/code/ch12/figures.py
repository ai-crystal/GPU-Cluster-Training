# -*- coding: utf-8 -*-
"""第 12 章插图：GPipe、1F1B、交错式 1F1B 的时空图与气泡。"""
from common import *  # noqa: F401,F403

FIGURES = ["fig_schedules"]

S, M = 4, 8          # 4 级流水，8 个微批次
T_MAX = 20.0
X0, X1 = 14.5, 97.5


# ------------------------------------------------------------ 调度计算
def _deps(s, kind, i, n):
    d = []
    if kind == "F" and s > 0:
        d.append((s - 1, "F", i))
    if kind == "B":
        d.append((s, "F", i))
        if s < n - 1:
            d.append((s + 1, "B", i))
    return d


def _sched(orders, dur):
    """列表调度：每个事件占用一个流水级的时间。"""
    n = len(orders)
    pos, times, last_end = [0] * n, {}, [0.0] * n
    while any(pos[s] < len(orders[s]) for s in range(n)):
        best = None
        for s in range(n):
            if pos[s] >= len(orders[s]):
                continue
            kind, i = orders[s][pos[s]]
            dep = _deps(s, kind, i, n)
            if any(x not in times for x in dep):
                continue
            t = max([last_end[s]] + [times[x][1] for x in dep])
            if best is None or t < best[0] - 1e-9:
                best = (t, s)
        t, s = best
        kind, i = orders[s][pos[s]]
        times[(s, kind, i)] = (t, t + dur)
        last_end[s] = t + dur
        pos[s] += 1
    return times


def _gpipe():
    seq = [("F", i) for i in range(M)] + [("B", i) for i in range(M - 1, -1, -1)]
    return _sched([list(seq) for _ in range(S)], 1.0)


def _one_f_one_b():
    out = []
    for s in range(S):
        w = min(S - 1 - s, M)
        if w == 0:
            seq = []
            for i in range(M):
                seq += [("F", i), ("B", i)]
        else:
            seq = [("F", i) for i in range(w)]
            for i in range(M - w):
                seq += [("B", i), ("F", w + i)]
            seq += [("B", i) for i in range(M - w, M)]
        out.append(seq)
    return _sched(out, 1.0)


# ------------------------------------------------------------ 绘图
def _px(t):
    return X0 + (X1 - X0) * t / T_MAX


def _panel(ax, y0, times, pitch, h):
    for s in range(S):
        y = y0 - s * pitch
        label(ax, X0 - 1.6, y + h / 2, f"卡 {s}", fs=7.2, ha="right", color=MUTED)
        busy = sorted([(a, b, k) for (st, k, i), (a, b) in times.items() if st == s])
        gaps, t = [], 0.0
        for (a, b, k) in busy:
            if a - t > 0.45:
                gaps.append((t, a))
            t = max(t, b)
        span = max(b for (a, b, k) in busy)
        if span - t > 0.45:                      # 尾部排空
            gaps.append((t, span + 0.0))
        for (a, b) in gaps:
            ax.add_patch(Rectangle((_px(a), y), _px(b) - _px(a), h, fc="#f4f5f7",
                                   ec=FAINT, lw=0.6, ls=(0, (2, 2)), zorder=1))
        for (a, b, k) in busy:
            ax.add_patch(Rectangle((_px(a) + 0.12, y), _px(b) - _px(a) - 0.24, h,
                                   fc=BLUE if k == "F" else ORANGE, ec="white",
                                   lw=0.5, zorder=3))
        if gaps:
            a, b = max(gaps, key=lambda g: g[1] - g[0])
            if b - a >= 1.0:
                label(ax, (_px(a) + _px(b)) / 2, y + h / 2, "气泡", fs=6.4,
                      color=MUTED, z=5)


def fig_schedules():
    fig, ax = canvas(16.0, 0.80, xlim=(0, 100), ylim=(0, 100))

    # 图例放在右上角空白处
    lx, ly = 55.0, 96.2
    ax.add_patch(Rectangle((lx, ly), 3.2, 2.4, fc=BLUE, ec="white", lw=0.4))
    label(ax, lx + 4.2, ly + 1.2, "前向", fs=6.9, ha="left")
    ax.add_patch(Rectangle((lx + 12, ly), 3.2, 2.4, fc=ORANGE, ec="white", lw=0.4))
    label(ax, lx + 16.2, ly + 1.2, "反向", fs=6.9, ha="left")

    # ---- (a) GPipe
    label(ax, 1.2, 97.4, "（a）GPipe：全部前向走完，再全部反向", fs=7.8, ha="left")
    _panel(ax, 86.0, _gpipe(), 6.0, 4.4)

    # ---- (b) 1F1B
    label(ax, 1.2, 61.0, "（b）1F1B：预热之后一前一后交替，同时在飞的微批次只有一个",
          fs=7.8, ha="left")
    _panel(ax, 53.0, _one_f_one_b(), 6.0, 4.4)

    # ---- (c) 交错式 1F1B
    label(ax, 1.2, 32.5, "（c）交错式 1F1B：每卡两段虚拟阶段，气泡更碎"
                        "（空心＝阶段 0，左侧虚线＝气泡）", fs=7.6, ha="left")

    seq = [("A", "F")] * 3
    cnt = {"AF": 5, "BF": 8, "AB": 8, "BB": 8}
    motif = {"AF": ("A", "F"), "BF": ("B", "F"),
             "AB": ("A", "B"), "BB": ("B", "B")}
    while any(v > 0 for v in cnt.values()):
        for key in ("AF", "BF", "AB", "BB"):
            if cnt[key] > 0:
                seq.append(motif[key])
                cnt[key] -= 1

    unit = (X1 - X0) / T_MAX          # 一个 slot 的宽度
    bw = unit * 0.5                   # 一个虚拟阶段的块宽
    lh, lg = 2.2, 0.4                 # 单条虚拟阶段行高 / 行距
    for d in range(S):
        yb = 24.6 - d * 5.6
        ya = yb + lh + lg
        label(ax, X0 - 1.6, yb + (lh + lg) / 2 + 0.4, f"卡 {d}", fs=7.2,
              ha="right", color=MUTED)
        off = 0.5 * d
        if d > 0:
            ax.add_patch(Rectangle((X0, yb), unit * off, 2 * lh + lg,
                                   fc="#f4f5f7", ec=FAINT, lw=0.6,
                                   ls=(0, (2, 2)), zorder=1))
        for k, (v, kind) in enumerate(seq):
            x = X0 + unit * off + bw * k
            yy = ya if v == "A" else yb
            col = BLUE if kind == "F" else ORANGE
            ax.add_patch(Rectangle((x + 0.1, yy), bw - 0.2, lh,
                                   fc=("white" if v == "A" else col), ec=col,
                                   lw=0.5, zorder=3))
        if d == S - 1:
            pass

    ax.annotate("", xy=(X1 - 2, 3.0), xytext=(X0, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7))
    label(ax, X1, 4.2, "时间（每格一个微批次）", fs=6.8, color=MUTED, ha="right")
    save(fig, "fig12-01-schedules.png")
