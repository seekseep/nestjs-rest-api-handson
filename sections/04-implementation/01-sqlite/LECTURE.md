---
docs: true
title: SQLite を用意する
---

# SQLite を用意する

![04 章 SQLite を用意する](./images/00-thumbnail.svg)

この章では、03 章で書いた `openapi.yaml` のとおりに、メモの API を実装します。メモは **SQLite** のデータベース（`api/notes.db` というファイル）に保存するので、API を再起動しても残ります。

SQLite は、Node.js に入っている `node:sqlite` で使います。ライブラリを足す必要はありません（Node.js 26 では「Release candidate（安定版の直前）」の段階です）。この節では、データベースを開いて、メモのテーブルを作るところまでを行います。

## データベースのファイルを Git に入れない

`notes.db` は手元のデータなので、`.gitignore` の最後に足します。

::diff{file="api/.gitignore"}

## データベースを開く

::diff{file="api/src/database.ts"}

- `new DatabaseSync('notes.db')` … `api/notes.db` を開きます。無ければ作ります
- `CREATE TABLE IF NOT EXISTS` … `notes` テーブルが無ければ作ります。列の名前は、`openapi.yaml` の `Note` の項目名と同じにしています
- `STRICT` … 列の型（`TEXT`）に合わない値を入れようとするとエラーにします

:::notice
Node.js 26 のドキュメントでは、このクラスの名前は `Database` に変わり、`DatabaseSync` は古い名前として残っています。TypeScript の型（`@types/node`）にはまだ `DatabaseSync` しか無いので、このハンズオンでは `DatabaseSync` を使います。
:::

## コントローラーを作る

メモの API を受け付けるコントローラーを作ります。

```bash
npx nest g controller notes
```

```text
CREATE src/notes/notes.controller.ts (99 bytes)
UPDATE src/app.module.ts (335 bytes)
```

`AppModule` に `NotesController` が登録されます。

::diff{file="api/src/app.module.ts" by="command"}

コントローラーが作られたときに、データベースを開くようにします。この章では、データベースの扱いもコントローラーに直接書きます（05 章で整理します）。

::diff{file="api/src/notes/notes.controller.ts" base="generated"}

## 確かめる

`npm run start:dev` で起動すると、`api/notes.db` ができます。Ctrl + C で止めてから、テーブルができたかを確かめます。

```bash
node -e "const { DatabaseSync } = require('node:sqlite'); console.log(new DatabaseSync('notes.db').prepare('SELECT name FROM sqlite_master').all())"
```

```text
[
  [Object: null prototype] { name: 'notes' },
  [Object: null prototype] { name: 'sqlite_autoindex_notes_1' }
]
```

`notes` が出れば大丈夫です（もう 1 つは、`PRIMARY KEY` のために SQLite が作る索引です）。

## 参考にした公式ドキュメント

この節は、次の公式ドキュメントをもとに書いています。

- [Node.js: SQLite](https://nodejs.org/docs/latest-v26.x/api/sqlite.html) … `DatabaseSync`・`exec()`・`prepare()`、安定性（Release candidate）
- [SQLite: STRICT Tables](https://www.sqlite.org/stricttables.html) … `STRICT` の意味
- [NestJS: CLI command reference](https://docs.nestjs.com/cli/usages) … `nest g controller`

## この節を終えたときのディレクトリ

::tree

:::download
[この節を終えた状態をダウンロード](./project.zip)
:::
