"""03-01「CRUD」の図。CRUD の 4 つの言葉と、その中にある形（Read の Get・List、Update の Put・Patch）。

スキーマ: PART-WHOLE（4 つの言葉の下に、それぞれの形がぶら下がる）。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(next(p / ".claude/skills/genfig" for p in Path(__file__).resolve().parents
                            if (p / ".claude/skills/genfig").is_dir())))
from genfig import Canvas  # noqa: E402

c = Canvas(960, 340)

COLS = [
    ("Create\n作る", "green", [("1 件作る", "POST /notes")]),
    ("Read\n読む", "blue", [("Get：1 件", "GET /notes/{id}"), ("List：一覧", "GET /notes")]),
    ("Update\n書き換える", "orange", [("Put：まるごと", "PUT /notes/{id}"), ("Patch：一部だけ", "PATCH /notes/{id}")]),
    ("Delete\n消す", "red", [("1 件消す", "DELETE /notes/{id}")]),
]

for i, (word, color, forms) in enumerate(COLS):
    cx = 130 + i * 233
    # 1 つの言葉のまとまり。中に、その言葉にふくまれる形を並べる
    c.sticky(cx - 114, 16, 228, 308, color=color, weight="thin")
    c.node(cx, 80, word, shape="square", color=color, w=190, h=84, label_scale="heading")
    for j, (name, route) in enumerate(forms):
        c.node(cx, 182 + j * 92, f"{name}\n{route}", shape="square", color="gray",
               w=210, h=78, label_scale="body")

c.save("01-crud.svg")
