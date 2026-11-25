#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成站点导航与首页。

从 structure.json 与各章一级标题生成：
    books/<册>/_sidebar.md
    books/<册>/README.md
    _sidebar.md
    README.md
页数与体积读 books/build/out/manifest.json。
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BOOKS = ROOT / "books"
MANIFEST = HERE / "out" / "manifest.json"

INTRO = (
    "一个千亿参数的模型，权重、梯度、优化器状态加起来有几千 GB，而一张显卡只有 80 GB。"
    "于是训练被拆到上千张卡上，卡与卡之间靠网络连成一台机器。"
)
PRO = (
    "同一件事，在单卡上是写代码，在千卡上就变成了系统工程。"
    "计算、显存、网络、存储、供电，任何一处算错，都会以训练变慢、挂起或者悄悄算错的形式表现出来。"
)


def title_of(path: Path) -> str:
    m = re.search(r"^#\s+(.+)$", path.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else path.stem


def load(key: str) -> dict:
    book = BOOKS / key
    meta = json.loads((book / "book.json").read_text(encoding="utf-8"))
    struct = json.loads((book / "structure.json").read_text(encoding="utf-8"))
    return {"key": key, "dir": book, "meta": meta, "struct": struct}


def pages_of(pdf_name: str) -> tuple[int, float]:
    if not MANIFEST.exists():
        return 0, 0.0
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for v in data.values():
        if v.get("pdf") == pdf_name:
            return int(v.get("pages", 0)), float(v.get("mb", 0))
    return 0, 0.0


def book_sidebar(b: dict) -> str:
    lines = ["- [系列首页](/README.md)", "", f"- [本册首页](/books/{b['key']}/README.md)"]
    for part in b["struct"]["parts"]:
        ptitle = title_of(b["dir"] / "front" / part["file"])
        lines.append("")
        lines.append(f"- **{ptitle}**")
        for ch in part["chapters"]:
            t = title_of(b["dir"] / "chapters" / ch)
            lines.append(f"  - [{t}](/books/{b['key']}/chapters/{ch})")
    app = b["struct"].get("appendix")
    if app:
        lines.append("")
        lines.append(f"- **{app.get('title', '附录')}**")
        for ch in app["chapters"]:
            t = title_of(b["dir"] / "appendix" / ch)
            lines.append(f"  - [{t}](/books/{b['key']}/appendix/{ch})")
    if b["struct"].get("back"):
        lines.append("")
        lines.append(f"- [后记](/books/{b['key']}/front/{b['struct']['back'][0]})")
    return chr(10).join(lines) + chr(10)


def book_readme(b: dict) -> str:
    meta = b["meta"]
    pages, mb = pages_of(meta["pdf"])
    out = [f"# {meta['title']}（{meta['edition']}）", "",
           f"**{meta['subtitle']}**", "", "作者：Dr. Dezeming", ""]
    out.append(INTRO if b["key"] == "intro" else PRO)
    out.append("")
    out.append(f"[开始阅读第 1 章](chapters/ch01.md)　｜　"
               f"[下载 PDF](../../output/{meta['pdf']} ':ignore')"
               + (f"（{pages} 页，{mb:.1f} MB）" if pages else ""))
    out.append("")
    out.append("## 目录")
    out.append("")
    for part in b["struct"]["parts"]:
        ptitle = title_of(b["dir"] / "front" / part["file"])
        out.append(f"### {ptitle}")
        out.append("")
        for ch in part["chapters"]:
            t = title_of(b["dir"] / "chapters" / ch)
            out.append(f"- [{t}](chapters/{ch})")
        out.append("")
    app = b["struct"].get("appendix")
    if app:
        out.append(f"### {app.get('title', '附录')}")
        out.append("")
        for ch in app["chapters"]:
            t = title_of(b["dir"] / "appendix" / ch)
            out.append(f"- [{t}](appendix/{ch})")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def root_sidebar(books: list[dict]) -> str:
    lines = ["- [系列首页](README.md)"]
    for b in books:
        m = b["meta"]
        lines.append("")
        lines.append(f"- **{m['edition']} · {m['title']}**")
        lines.append(f"  - [本册首页与目录](books/{b['key']}/README.md)")
        lines.append(f"  - [从第 1 章开始读](books/{b['key']}/chapters/ch01.md)")
    return "\n".join(lines) + "\n"


def root_readme(books: list[dict]) -> str:
    rows = []
    blurb = {"intro": "动机、结构、并行、故障，不推公式",
             "pro": "性能模型、通信账、并行细节、踩坑清单"}
    for b in books:
        m = b["meta"]
        pages, mb = pages_of(m["pdf"])
        rows.append(
            f"| **{m['edition']}**《{m['title']}》 | {blurb.get(b['key'], '')} | "
            f"{pages or '—'} 页 | [开始阅读](books/{b['key']}/chapters/ch01.md) ｜ "
            f"[目录](books/{b['key']}/README.md) | "
            f"[PDF {mb:.1f} MB](output/{m['pdf']} ':ignore') |")
    return f"""# 大规模 GPU 集群训练技术

一套讲大规模训练的读本，分两册。入门篇建立完整地图，专业篇把每一步的字节数、微秒数和故障模式算清楚。

| 册 | 讲什么 | 篇幅 | 在线阅读 | PDF |
|---|---|---|---|---|
{chr(10).join(rows)}

建议先读入门篇，再按需要翻专业篇。两册各自完整，只读一本也不影响理解。

## 这套书想讲清楚的一件事

一张 H100 有 80 GB 显存，一个 4050 亿参数的模型光权重就要 810 GB。于是训练被拆到几千张卡上，卡与卡之间靠网络连成一台机器。问题从"怎么写出模型"变成了"怎么让一万张卡像一张卡那样工作"。

显存怎么分，模型怎么切，梯度怎么汇总，网络怎么摆，坏了怎么恢复，慢了怎么定位。这些问题的答案都可以算出来，而不是靠感觉。书里的每一个数字都尽量落到具体的位置：多少字节、多少微秒、多少个百分点。

## 阅读入口

- [入门篇前言](books/intro/front/preface.md)　｜　[入门篇后记](books/intro/front/afterword.md)
- [专业篇前言](books/pro/front/preface.md)　｜　[专业篇后记](books/pro/front/afterword.md)
- [附录 A　术语与缩写](books/pro/appendix/appA.md)　｜　[附录 B　常用公式与估算表](books/pro/appendix/appB.md)

## 作者

Dr. Dezeming
"""


def main() -> None:
    keys = [p.name for p in sorted(BOOKS.iterdir())
            if p.is_dir() and (p / "book.json").exists()]
    order = [k for k in ("intro", "pro") if k in keys] + [k for k in keys if k not in ("intro", "pro")]
    books = [load(k) for k in order]
    for b in books:
        (b["dir"] / "_sidebar.md").write_text(book_sidebar(b), encoding="utf-8")
        (b["dir"] / "README.md").write_text(book_readme(b), encoding="utf-8")
    (ROOT / "_sidebar.md").write_text(root_sidebar(books), encoding="utf-8")
    (ROOT / "README.md").write_text(root_readme(books), encoding="utf-8")
    print("site files written:", ", ".join(order))


if __name__ == "__main__":
    main()
