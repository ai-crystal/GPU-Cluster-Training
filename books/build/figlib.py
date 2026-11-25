# -*- coding: utf-8 -*-
"""两册书共用的插图库。

坐标系默认 100×100，所有示意图都用它，保证字号和线宽一致。
数据图用 chart() 建立真实坐标，避免手工换算。
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import (Arc, Circle, FancyArrowPatch, FancyBboxPatch,
                               Polygon, Rectangle, Wedge)
from matplotlib.lines import Line2D

# ---------------------------------------------------------------- 调色
INK = "#1f2933"
MUTED = "#7b8794"
FAINT = "#c7ced6"
LIGHT = "#eef1f4"
BLUE = "#3d6b9e"
BLUE_L = "#e8eff7"
ORANGE = "#c0603c"
ORANGE_L = "#fbf0ea"
GREEN = "#3f7d63"
GREEN_L = "#e9f2ee"
PURPLE = "#6b5b95"
PURPLE_L = "#f0edf6"
RED = "#a63d40"
RED_L = "#f9ecec"
GOLD = "#a9822c"

plt.rcParams.update({
    "font.family": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "font.size": 9,
    "axes.unicode_minus": False,
    "mathtext.fontset": "stix",
    "figure.dpi": 100,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.linewidth": 0.8,
})

CURRENT = Path(".")


def canvas(w=16.0, ratio=0.55, xlim=(0, 100), ylim=(0, 100)):
    fig, ax = plt.subplots(figsize=(w / 2.54, w * ratio / 2.54))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def chart(w=16.0, h=8.0):
    fig, ax = plt.subplots(figsize=(w / 2.54, h / 2.54))
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors="#4a5560", labelsize=8, width=0.7, length=3)
    ax.grid(axis="y", color="#e3e7ea", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    return fig, ax


def save(fig, name):
    path = CURRENT / Path(name).with_suffix(".png").name
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="png", dpi=230, facecolor="white")
    plt.close(fig)
    print("  ->", path)


def box(ax, x, y, w, h, text="", fc="white", ec=INK, lw=0.9, fs=8.2,
        color=INK, radius=1.0, style="round", weight="normal", z=2,
        alpha=1.0, ls="-", linespacing=1.4):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"{style},pad=0,rounding_size={radius}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z,
                       alpha=alpha, linestyle=ls)
    ax.add_patch(p)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, color=color, zorder=z + 1, weight=weight,
                linespacing=linespacing)
    return p


def arrow(ax, p1, p2, color=INK, lw=0.9, style="-|>", ls="-", rad=0.0,
          shrinkA=1, shrinkB=1, z=3, ms=6, alpha=1.0):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms,
                        linewidth=lw, color=color, linestyle=ls,
                        shrinkA=shrinkA, shrinkB=shrinkB,
                        connectionstyle=f"arc3,rad={rad}", zorder=z, alpha=alpha)
    ax.add_patch(a)
    return a


def label(ax, x, y, text, fs=8, color=INK, ha="center", va="center",
          weight="normal", z=5, rotation=0, bbox=None, alpha=1.0):
    return ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va,
                   weight=weight, zorder=z, rotation=rotation, bbox=bbox,
                   linespacing=1.4, alpha=alpha)


def note(ax, x, y, text, fs=7.2, color=MUTED, ha="left", va="center", weight="normal"):
    return ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va,
                   weight=weight, linespacing=1.4, zorder=6)


def bracket(ax, x1, x2, y, text, fs=7.2, color=MUTED, up=1.6):
    ax.plot([x1, x1, x2, x2], [y + up * 0.45, y + up, y + up, y + up * 0.45],
            color=color, lw=0.7, zorder=4)
    ax.text((x1 + x2) / 2, y + up * 1.35, text, ha="center", va="bottom",
            fontsize=fs, color=color, zorder=5)


def vline(ax, x, y1, y2, color=FAINT, lw=0.7, ls="--", z=1):
    ax.plot([x, x], [y1, y2], color=color, lw=lw, ls=ls, zorder=z)


def grid(ax, x, y, w, h, rows, cols, fc="white", ec=MUTED, lw=0.6, gap=0.0, z=2):
    cw, ch = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            ax.add_patch(Rectangle((x + c * cw + gap, y + (rows - 1 - r) * ch + gap),
                                   cw - 2 * gap, ch - 2 * gap, fc=fc, ec=ec,
                                   lw=lw, zorder=z))


def cell_text(ax, x, y, w, h, rows, cols, texts, fs=6.5, color=INK):
    cw, ch = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            if i < len(texts) and texts[i]:
                ax.text(x + (c + 0.5) * cw, y + (rows - 0.5 - r) * ch, texts[i],
                        ha="center", va="center", fontsize=fs, color=color, zorder=4)


def heatmap(ax, x, y, w, h, mat, cmap="Blues", vmin=None, vmax=None, ec="none", lw=0.4):
    m = np.asarray(mat, dtype=float)
    rows, cols = m.shape
    vmin = m.min() if vmin is None else vmin
    vmax = m.max() if vmax is None else vmax
    cm = plt.get_cmap(cmap)
    for r in range(rows):
        for c in range(cols):
            v = 0.0 if vmax == vmin else (m[r, c] - vmin) / (vmax - vmin)
            ax.add_patch(Rectangle((x + c * w / cols, y + (rows - 1 - r) * h / rows),
                                   w / cols, h / rows, fc=cm(0.08 + 0.84 * v),
                                   ec=ec, lw=lw, zorder=2))
    return rows, cols


def bars(ax, labels, values, colors=None, width=0.62, fs=8, fmt="{:.0f}",
         text_color=INK, text_fs=7.5, log=False, ylim=None, rotation=0):
    n = len(values)
    xs = np.arange(n)
    colors = colors or [BLUE] * n
    if isinstance(colors, str):
        colors = [colors] * n
    rects = ax.bar(xs, values, width=width, color=colors, edgecolor="none", zorder=3)
    if log:
        ax.set_yscale("log")
    if ylim:
        ax.set_ylim(*ylim)
    for r, v in zip(rects, values):
        h = r.get_height()
        ax.annotate(fmt.format(v), (r.get_x() + r.get_width() / 2, h),
                    ha="center", va="bottom", fontsize=text_fs, color=text_color,
                    xytext=(0, 3), textcoords="offset points", zorder=4)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=fs, rotation=rotation,
                       ha="right" if rotation else "center")
    ax.set_xlim(-0.6, n - 0.4)
    return rects


def hbars(ax, labels, values, colors=None, height=0.6, fs=7.8, fmt="{:.0f}",
          text_fs=7.4, xmax=None):
    n = len(values)
    ys = np.arange(n)[::-1]
    colors = colors or [BLUE] * n
    if isinstance(colors, str):
        colors = [colors] * n
    ax.barh(ys, values, height=height, color=colors, edgecolor="none", zorder=3)
    for y, v in zip(ys, values):
        ax.annotate(fmt.format(v), (v, y), va="center", ha="left",
                    fontsize=text_fs, color=INK, xytext=(3, 0),
                    textcoords="offset points", zorder=4)
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=fs)
    if xmax:
        ax.set_xlim(0, xmax)
    return ys


def timeline(ax, rows, tmax, height=0.55, fs=7.6, row_gap=1.0):
    """rows: [(名称, [(起, 止, 颜色, 文本)])]，返回行 y 位置。"""
    ys = []
    for i, (name, segs) in enumerate(rows):
        y = (len(rows) - 1 - i) * row_gap
        ys.append(y)
        ax.text(-1.2, y + height / 2, name, ha="right", va="center", fontsize=fs)
        for (a, b, color, text) in segs:
            ax.add_patch(Rectangle((a, y), b - a, height, fc=color, ec="white",
                                   lw=0.8, zorder=3))
            if text and (b - a) / tmax > 0.045:
                ax.text((a + b) / 2, y + height / 2, text, ha="center", va="center",
                        fontsize=fs - 1.0, color="white", zorder=4)
    ax.set_xlim(0, tmax)
    ax.set_ylim(-0.9, len(rows) * row_gap - 0.1)
    ax.axis("off")
    return ys


def seq(ax, lanes, events, x0=8, x1=96, y0=6, y1=90, fs=7.6, ms=6):
    """时序图。lanes: 名称列表；events: [(起点lane, 终点lane, 文本, 颜色, 虚线?)]"""
    n = len(lanes)
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)] if n > 1 else [x0]
    for x, name in zip(xs, lanes):
        ax.add_patch(Rectangle((x - 4.2, y1 - 6), 8.4, 6, fc="#f2f4f6",
                               ec=MUTED, lw=0.7, zorder=2))
        ax.text(x, y1 - 3, name, ha="center", va="center", fontsize=fs, zorder=3)
        ax.plot([x, x], [y0, y1 - 6], color=FAINT, lw=0.8, ls=(0, (3, 2)), zorder=1)
    for (a, b, text, color, *rest) in events:
        dashed = rest[0] if rest else False
        y = y0 + (y1 - y0 - 8) * (1 - (events.index((a, b, text, color, *rest)) + 0.6) / (len(events) + 0.4))
        arrow(ax, (xs[a], y), (xs[b], y), color=color, lw=0.9, ms=ms,
              ls="--" if dashed else "-")
        ax.text((xs[a] + xs[b]) / 2, y + 1.6, text, ha="center", va="bottom",
                fontsize=fs - 0.6, color=color, zorder=4)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")


def brace_label(ax, x, y, w, text, color=MUTED, fs=7.0):
    ax.annotate(text, xy=(x + w / 2, y), xytext=(x + w / 2, y - 4),
                ha="center", va="top", fontsize=fs, color=color,
                arrowprops=dict(arrowstyle="-", color=color, lw=0.6,
                                shrinkA=0, shrinkB=1))


def anote(ax, x, y, text, fs=7.0, color=MUTED, ha="left", va="top"):
    """按坐标轴比例写注释，不会把画布撑大。"""
    return ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, color=color,
                   ha=ha, va=va, linespacing=1.5, zorder=7)


def clean_axes(ax, xlabel="", ylabel="", title=""):
    ax.set_xlabel(xlabel, fontsize=8.2, color="#3a4650")
    ax.set_ylabel(ylabel, fontsize=8.2, color="#3a4650")
    if title:
        ax.set_title(title, fontsize=9, color=INK, pad=6)
