"""05-02「入力を dto/ に分ける」の図。

DTO は、API の外（画面・curl・Try it）から届いた本文を、入力チェックを通したあとの形で
コントローラーに渡すためのもの。応答は Note で返す。
スキーマ: CONTAINER（API）+ SOURCE-PATH-GOAL（受け取り）+ CYCLE（応答）。
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / ".claude/skills/genfig" for p in Path(__file__).resolve().parents
                            if (p / ".claude/skills/genfig").is_dir())))
from genfig import Canvas  # noqa: E402
from genfig.tokens import PALETTE  # noqa: E402

c = Canvas(960, 320)


def box(draw, cx, cy, w, h, label, color):
    """図形を描き、ラベルを図形の上下の中央に置く（2 行でも中央に来るように）。"""
    n = draw(cx - w / 2, cy - h / 2, w, h, color=color)
    lines = label.count("\n")
    c.text(cx, cy + 8 - lines * 14, label, scale="label", fill=PALETTE[color]["text"])
    return n


client = c.node(105, 157, "クライアント\n画面・curl など", emoji_cp="1f310", label_scale="label")  # 🌐

c.sticky(270, 40, 670, 180, color="gray", dash="dashed", weight="thin")
c.text(294, 76, "API", scale="heading", align="left")

check = box(c.hexagon, 400, 140, 170, 80, "入力チェック", "purple")
dto = box(c.sticky, 620, 140, 200, 80, "CreateNoteDto", "yellow")
ctrl = box(c.sticky, 840, 140, 150, 90, "Notes\nController", "blue")

c.link((client.right, 140), check, label="JSON", label_pos="above")
c.link(check, dto)
c.link(dto, ctrl)
c.link(ctrl, client, label="Note（応答）", primary=False, route="elbow",
       start="s", end="s")

c.save("01-dto.svg")
