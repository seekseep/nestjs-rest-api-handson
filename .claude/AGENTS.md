# AGENTS.md - プロジェクト方針

## プロジェクト概要

メモの REST API を、OpenAPI で設計してから NestJS で実装し、NestJS の形に整理するハンズオン教材（シリーズの A。
B「Cognito で認証と認可」は seekseep/nestjs-cognito-auth-handson、C「テスト」は seekseep/nestjs-testing-handson。
どれも他を前提にしない）。
handson-builder スキルの骨格（`sections/` ＋ Starlight の `site/` ＋ GitHub Pages）を使っている。
全体の計画と方針の正本は GitHub のイシュー #1。

## 用語：章（セクション）と節（レクチャー）

| 用語 | 指すもの | 例 |
|---|---|---|
| **章** | `sections/<NN-section>/`。章立ては固定（イシュー #1） | `03-design/` |
| **節** | `sections/<NN-section>/<NN-lecture>/`。増減してよい | `03-design/03-create/` |

- 節のディレクトリは **その節を終えた時点のプロジェクト** を丸ごと持つ（`api/` だけ）
- 次の節は、前の節のディレクトリをコピーして差分を足して作る
- 本文は `LECTURE.md`（`docs: true`）。節の直下の `README.md` は ZIP を展開した人向けの起動方法
- 説明図は `images/` に SVG で置く（`00-thumbnail.svg` を先頭サムネに）
- 章の直下には README を置かない
- 環境構築の節のようにプロジェクトを持たない節もある（本文だけ）

## プロジェクトの形

```text
sections/<sec>/<lec>/
├── README.md         起動方法（ZIP に入る。::tree には出さない）
├── LECTURE.md        教材本文（ZIP に入らない）
├── images/           説明図（ZIP に入らない）
└── api/              NestJS（nest new で作ったもの。.gitignore を持つ）
    ├── openapi.yaml  03 章から。API の設計（OpenAPI 3.0.3）
    └── notes.db      04 章から。SQLite のデータ（.gitignore 済み）
```

- 章立て: 01 準備 / 02 Hello World / 03 設計する（CRUD の説明（本文だけ）、空の `openapi.yaml` を作り、1 節 1 操作で書き足し、最後に `components` にまとめる）/
  04 実装する（`node:sqlite` の `DatabaseSync`。@hey-api/openapi-ts で型を作る節のあと、1 節 1 操作でコントローラーに直接書き、最後の節で Zod の入力チェックを足す）/ 05 整理する（1 節で 1 つだけ分け、動きは変えない）
- 動作確認は、42Crunch の OpenAPI (Swagger) Editor の **Try it**（`openapi.yaml` の各操作の下に出る）で行う。
  Try it は拡張機能の中（Node.js）から送るので CORS は要らない。Try it は OpenAPI 2.0 / 3.0.x だけに出るので、`openapi: 3.0.3` で書く
- 04 章の動作確認では、Try it に加えて curl のコマンドも載せる（`curl -i` の 1 行で、OS で分けない）。Postman・Redocly CLI などは使わない

- 言語は **TypeScript**（handson-builder 既定の「JS のみ」から外している。NestJS と OpenAPI からの型生成を扱うため）
- Podman・compose・コンテナ・Next.js は使わない。Node.js と VS Code だけで進める
- パッケージマネージャはレクチャー側が **npm**（`api/package-lock.json`）、サイトが pnpm
- `api/` は、`nest new --package-manager npm --skip-tests --type esm --no-observe --skip-skills` が作ったものを使う。
  テストの仕組み（Vitest の設定 2 つ・`vite`・`vitest`・`@vitest/coverage-v8`・`supertest`・`@types/supertest`・`@nestjs/testing`・`test` の 5 つのスクリプト・`tsconfig.json` の `vitest/globals`・`format` と `lint` の `test/`）だけは 02-01 で消す（テストは C で扱う）。
  ほか（`AGENTS.md`・`README.md`・oxlint・Prettier）はそのまま。`@nestjs/testing` が無いので、`nest g` は spec を作らない（`--no-spec` は要らない）。教材で足すのは `src/` の中身と、03 章から `openapi.yaml`、04 章から型の生成と zod
- ポート: `nest new` の既定の 3000
- 秘密の実値は絶対にコミットしない

## 本文の書き方（センチネル）

- コードの変更は `::diff{file="api/src/main.ts"}` で示す。前の節の同じファイルとの差分を実ファイルから生成する
  （`site/scripts/libs/project-diff.mjs`）。新規ファイルは全行 `+`。本文にコードを手で二重に書かない
  - `::diff[どこを書き換えるか]{file="..."}` で説明を付けられる
  - `::diff` は先頭に「`api/src/main.ts` を変更する」の見出しを自動で付ける（前の節に無ければ「作成する」、
    この節で消したなら「削除する」。漢字で書く）。見出しの深さは直前の見出しより 1 つ深い。
    本文に「`...` を作ります」のような、見出しと重なる文は書かない
  - 比べる相手を変えるときは `from="<sec>/<lec>"`、前の節でのファイル名が違うときは `fromFile="..."`
  - 本文のコマンド（`nest g` など）が作った・書き換えたファイルに手で書き足すときは、コマンドの直後のファイルを
    節の `generated/<file>` に置き、`base="generated"` で比べる（`generated/` は ZIP・`::tree` に入らない）
  - コマンドが作った・書き換えた結果を見せるだけの差分には `by="command"` を付ける。見出しが「`...` が作られる／が変わる／が消える」になり、
    手で書く手順（「作成する／変更する／削除する」）と見分けられる
- ページの最後は「この節を終えたときのディレクトリ」見出し → `::tree` → `:::download` ＋ `[...](./project.zip)`
  - `::tree` は、その節のプロジェクト全体をエディタ（左にツリー、右にコード）で見せる。前の節から追加・変更したファイルに「作成」「変更」の印、変更したファイルの足した行に色を付ける。`package-lock.json` と画像は中身を省く（エディタは Cognito + Entra ID のハンズオンから移したもの）
- コマンドの実行例は普通のコードブロックで書く
- 節ごとに「参考にした公式ドキュメント」の見出しを、「この節を終えたときのディレクトリ」（無ければ `:::faq`）の前に置き、`- [名前](URL) … 何を参考にしたか` の形で並べる。リンクは開けることと、書いた中身が本当にそのページにあることを確かめてから載せる
- よくある質問は `:::faq`、注意は `:::warning` / `:::danger` / `:::notice`
- 手順が OS で分かれるところは `:::::platform` で囲み、中を `::::macos` / `::::windows` / `::::linux`（`::::macos-linux` のように `-` でつなぐと両方に出す）に分ける
  - Windows は PowerShell 7 の手順を書く（WSL は使わない）。bash のコマンドで PowerShell では動かないもの（`\` の改行・`/dev/null`・`export`・`rm -rf`・`VAR=値 コマンド` など）は、`::::macos-linux` と `::::windows` に分ける
  - 選んだ OS は localStorage（キー `handson-os`）に残り、ナビゲーションバーの選択欄と `::platform-choice`（01-01 に置いている）で変える
  - パネルの中に見出し（`##`・`###`）は書かない（目次に残って、隠れた所を指してしまう）
  - 実装は site/src/plugins/remark-platform.mjs・site/src/scripts/platform-client.js・site/src/styles/platform.css・site/src/components/ThemeSelect.astro（Cognito + Entra ID のハンズオンから移したもの）
- 「次へ」の見出しやリンクは書かない（Starlight の前へ／次へと重複するため）

## 本文の分量

- 目標は、できるだけ少ない分量で重要な要素だけを理解させること。「あったら良い」説明は書かない
- 手順は 1 通りに絞る。別のやり方・任意の道具・「〜でもかまいません」・豆知識・コラム・背景の長い説明・言い直しは書かない
- `::diff` の下の箇条書きは、そのコードを読むのに欠かせない点だけにする
- `:::faq` は、手順どおりに進めても本当につまずく問題だけにする
- 「参考にした公式ドキュメント」は、本文に書いた話題のリンクだけにする

## 図（genfig）

- 図は genfig スキルで作る。genfig は `seekseep/genfig-skill` を **サブモジュール** として `.claude/skills/genfig` に入れている。clone は `git clone --recurse-submodules`、clone 済みなら `git submodule update --init` で取ってくる
- 各節の `images/NN-xxx.py` は、ファイルの場所から上へたどって `.claude/skills/genfig` を読み込む。`images/` の中で `python3 NN-xxx.py` を実行すると、同じ名前の `.svg` を書き出す
- genfig を直すときは genfig-skill のリポジトリに PR を出し、マージしてからサブモジュールを更新して図を描き直す
- SVG は `xmllint --noout` を通し、描き出して目で確かめる

## サイト（site/）の開発

パッケージマネージャは **pnpm**（`site/package.json` の `packageManager` で固定）。

```sh
cd site
pnpm install
pnpm run dev      # http://localhost:4321（predev で previews / sync / downloads が走る）
pnpm run build    # 本番ビルド
```

- ZIP・`::tree`・`::diff` は `git ls-files --cached --others --exclude-standard` の結果を使う。
  `.gitignore` 済みのもの（`node_modules/`・`dist/`・`.env`）は入らない
- 依存を上げ直すときに踏みやすい点（esbuild の allowBuilds、archiver 8 の `ZipArchive`、Astro 7 の
  `@astrojs/markdown-remark`）は handson-builder スキルの `references/conventions.md` を参照

## サイトへの公開ルール

- frontmatter に `docs: true` を持つマークダウンだけが `site/scripts/sync-lectures.mjs` に拾われる
- 文章は必ず `sections/` 側に書く。`site/src/content/docs/` は自動生成なので直接編集しない
- 相対リンクは sync スクリプトが自動変換する（他の節 → サイト内 URL、ソースコード → GitHub blob、
  画像 → GitHub raw、`./project.zip` → その節の ZIP、`./start.zip` → 前の節の ZIP）

## 進め方（このリポジトリ）

- 章ごとにブランチを切って PR を作る。ビルドが通ることを確かめてからマージしてよい
- 方針が変わったらイシュー #1 の本文を更新する
