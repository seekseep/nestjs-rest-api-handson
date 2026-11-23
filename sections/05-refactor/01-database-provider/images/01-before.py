"""05 章「整理する」の構成図。どの節でも同じ構図で、NotesController から部品が分かれていく。

STAGE だけを節ごとに変える（start / db / dto / entities / service / module）。
その節で分けたものに色を付け、前の節までに分けたものは灰色にする。
スキーマ: CONTAINER（AppModule・NotesModule・DatabaseModule・NotesController）
+ SPLITTING（取り出す）+ LINK（注入）。
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / ".claude/skills/genfig" for p in Path(__file__).resolve().parents
                            if (p / ".claude/skills/genfig").is_dir())))
from genfig import Canvas  # noqa: E402
from genfig.tokens import PALETTE  # noqa: E402

STAGE = "start"

ORDER = ["db", "dto", "entities", "service"]
ROW_LABELS = {
    "db": "データベースを開く",
    "dto": "入力の形とチェック",
    "entities": "Note の形",
    "service": "SQL と処理",
}

if STAGE == "start":
    moved, current = [], None
elif STAGE == "module":
    moved, current = list(ORDER), "module"
else:
    moved, current = ORDER[: ORDER.index(STAGE) + 1], STAGE


def color_of(key, color):
    return color if key == current else "gray"


c = Canvas(960, 540)

# AppModule（いつも全体を包む）
c.sticky(20, 20, 920, 500, color="gray", dash="dashed", weight="thin")
c.text(44, 56, "AppModule", scale="heading", align="left")

# NotesModule（最後の節だけ。DatabaseModule は外に残る）
if STAGE == "module":
    c.sticky(40, 76, 652, 428, color="blue", weight="thick")
    c.text(64, 110, "NotesModule", scale="heading", align="left", fill="#1d4ed8")

# NotesController（いつも同じ位置・大きさ）
ctrl = c.sticky(68, 128, 300, 352, color="teal", weight="thick")
c.text(90, 160, "NotesController", scale="label", align="left", fill="#0f766e")

rows = ["受け取って返す"] + [ROW_LABELS[k] for k in ORDER if k not in moved]
for i, label in enumerate(rows):
    c.node(218, 210 + i * 52, label, shape="square", color="gray",
           w=264, h=42, label_scale="label")

# 分けたもの（いつも同じ位置）
nodes = {}


def box(cx, cy, label, **kw):
    """2 行のラベルを図形の上下の中央に置く（node() は 1 行目を中央に置くため）。"""
    w, h, color = kw["w"], kw["h"], kw["color"]
    draw = c.hexagon if kw["shape"] == "hexagon" else c.sticky
    n = draw(cx - w / 2, cy - h / 2, w, h, color=color)
    c.text(cx, cy - 4, label, scale="label", fill=PALETTE[kw["color"]]["text"])
    return n


if "db" in moved:
    db_color = color_of("db", "green")
    c.sticky(702, 96, 228, 200, color=db_color, weight="thick")
    c.text(716, 128, "DatabaseModule", scale="label", align="left")
    nodes["db"] = c.node(816, 210, "DatabaseSync", shape="cylinder",
                         color=db_color, w=196, h=116, label_scale="label")
if "service" in moved:
    nodes["service"] = box(540, 210, "NotesService\nSQL と処理", shape="hexagon",
                           color=color_of("service", "purple"), w=250, h=110)
if "dto" in moved:
    nodes["dto"] = box(540, 342, "dto/\n入力の形とチェック", shape="square",
                       color=color_of("dto", "yellow"), w=270, h=92)
if "entities" in moved:
    nodes["entities"] = box(540, 448, "entities/\nNote の形", shape="square",
                            color=color_of("entities", "orange"), w=270, h=92)

# 注入（データベース → 使う側、サービス → コントローラー）
if "db" in nodes:
    if "service" in nodes:
        c.link(nodes["db"], nodes["service"], label="注入", start="w", label_pos="above")
    else:
        c.link(nodes["db"], (ctrl.right, 210), label="注入", start="w")
if "service" in nodes:
    c.link(nodes["service"], (ctrl.right, 210), label="注入", start="w", label_pos="above")

c.save(os.path.splitext(os.path.basename(__file__))[0] + ".svg")
