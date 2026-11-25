# -*- coding: utf-8 -*-
"""本册插图的公共入口：路径与保存。"""
from __future__ import annotations

import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
BOOK = CODE.parent
BUILD = BOOK.parent / "build"
sys.path.insert(0, str(BUILD))

import figlib
from figlib import *  # noqa: F401,F403

CURRENT = BOOK / "images" / "front"


def save(fig, name):
    figlib.CURRENT = CURRENT
    figlib.save(fig, name)
