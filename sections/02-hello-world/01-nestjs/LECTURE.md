---
docs: true
title: NestJS の Hello World
---

# NestJS の Hello World

![02 章 NestJS の Hello World](./images/00-thumbnail.svg)

この節では、**NestJS** のプロジェクトを作り、「Hello World!」を返す API を動かします。このプロジェクト（`api/`）に、03 章で API の設計（`openapi.yaml`）を書き、04 章でメモを読み書きする REST API を実装します。

NestJS は、Node.js で API を作るためのフレームワークです。URL ごとの処理（コントローラー）と処理の中身（サービス）を分けて書き、それらをモジュールにまとめます。

## NestJS のプロジェクトを作る

作業用のフォルダを作り、その中で Nest CLI の 12 系を使ってプロジェクトを作ります。

```bash
mkdir handson
cd handson
npx @nestjs/cli@12 new api
```

途中で 4 つの質問が出ます。矢印キーで選び、Enter で決めます。

| 質問 | 答え |
|---|---|
| `Which package manager would you ❤️  to use?` | `npm`（このハンズオンは npm で進める） |
| `Would you like to set up @nestjs/observe (...)?` | `n`（監視サービスは使わない） |
| `Which coding agents should get the official NestJS agent skills?` | `none`（いちばん下） |
| `Which module system would you like to use?` | `ESM (ES Modules)`（このハンズオンは ESM のコードで書く） |

答え終わると、`api/` にファイルを作り、ライブラリを入れます。

```text
✔ Which package manager would you ❤️  to use? npm
✔ Would you like to set up @nestjs/observe (distributed tracing, auto-correlated
 logs, metrics and alarms - free for 300k events/month, https://observe.nestjs.c
om)? No
✔ Which coding agents should get the official NestJS agent skills? none
✔ Which module system would you like to use? ESM (ES Modules)         [ with vit
est ]
CREATE api/.gitattributes (19 bytes)
CREATE api/.oxlintrc.json (206 bytes)
（省略）
CREATE api/src/main.ts (237 bytes)
CREATE api/src/app.controller.spec.ts (623 bytes)
CREATE api/test/app.e2e-spec.ts (731 bytes)

▹▹▹▹▹ Installation in progress... ☕

🚀  Successfully created project api
👉  Get started with the following commands:

$ cd api
$ npm run start
```

質問に答える代わりに、オプションで同じ答えを渡すと、1 行で作れます。

```bash
npx @nestjs/cli@12 new api --package-manager npm --no-observe --skip-skills --type esm
```

- `--package-manager npm` … 1 つ目の質問の答え
- `--no-observe` … 2 つ目の質問の答え
- `--skip-skills` … 3 つ目の質問の答え
- `--type esm` … 4 つ目の質問の答え

以降のコマンドは、`api/` の中で実行します。VS Code で `api/` を開いておきます。

```bash
cd api
code .
```

主なファイルは次のとおりです。

| ファイル | 役割 |
|---|---|
| `src/main.ts` | アプリを起動する入り口。ポート番号もここで決める |
| `src/app.module.ts` | モジュール。コントローラーとサービスをまとめる |
| `src/app.controller.ts` | コントローラー。URL とメソッドに応じて処理を呼ぶ |
| `src/app.service.ts` | サービス。実際の処理（ここでは文字列を返すだけ） |
| `package.json`・`package-lock.json` | 使うライブラリとコマンド（`scripts`） |
| `tsconfig.json`・`tsconfig.build.json`・`nest-cli.json` | TypeScript と Nest CLI の設定 |
| `src/app.controller.spec.ts`・`test/app.e2e-spec.ts` | テストのひな形（このハンズオンでは使わない） |

## 動かす

```bash
npm run start:dev
```

```text
[Nest] 53212  - 2026/11/20 11:37:13     LOG [NestFactory] Starting Nest application...
[Nest] 53212  - 2026/11/20 11:37:13     LOG [InstanceLoader] AppModule dependencies initialized +4ms
[Nest] 53212  - 2026/11/20 11:37:13     LOG [RoutesResolver] AppController {/}:
[Nest] 53212  - 2026/11/20 11:37:13     LOG [RouterExplorer] Mapped {/, GET} route
[Nest] 53212  - 2026/11/20 11:37:13     LOG [NestApplication] Nest application successfully started
```

`Mapped {/, GET} route` は「`GET /` を受け付ける」という意味です。ブラウザで <http://localhost:3000> を開くと `Hello World!` と表示されます。

`start:dev` は、ファイルを保存すると自動で再起動します。止めるときは Ctrl + C を押します。ポート番号は `src/main.ts` で決まっています。

:::code{filepath="api/src/main.ts"}
```ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module.js';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT ?? 3000);
}
await bootstrap();
```
:::

`process.env.PORT ?? 3000` は「環境変数 `PORT` があればその値、無ければ 3000」という意味です。

## リクエストが届くまで

`GET /` が届くと、NestJS は `AppModule` の `AppController` から `@Get()` が付いた `getHello()` を呼びます。コントローラーは `AppService` の `getHello()` を呼び、返ってきた文字列がレスポンスの本文になります。

![GET / が AppController の getHello() に届き、AppService の getHello() が返した Hello World! がレスポンスの本文になる](./images/01-request-flow.svg)

:::code{filepath="api/src/app.controller.ts"}
```ts
@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}
```
:::

`constructor(private readonly appService: AppService)` と書くだけで、NestJS が `AppService` のインスタンスを作って渡してくれます。これを **依存性の注入（DI）** と呼びます。

:::notice
NestJS 12 のプロジェクトは ES Modules で書かれています。`import { AppService } from './app.service.js'` のように、TypeScript のファイルでも import の末尾は `.js` にします（ビルド後のファイル名に合わせるため）。
:::

## ビルドする

```bash
npm run build
```

TypeScript をコンパイルして `dist/` に書き出します。このハンズオンでは、節の終わりにビルドが通ることを確かめています。

## 参考にした公式ドキュメント

この節は、次の公式ドキュメントをもとに書いています。

- [NestJS: First steps](https://docs.nestjs.com/first-steps) … `nest new` で作るプロジェクトのファイルと `main.ts`、`npm run start:dev`
- [NestJS: CLI command reference](https://docs.nestjs.com/cli/usages) … `nest new` の質問と、同じ答えを渡す `--package-manager`・`--no-observe`・`--skip-skills`・`--type`
- [NestJS: Controllers](https://docs.nestjs.com/controllers) … `@Controller()`・`@Get()` とルートの決まり方
- [NestJS: Providers](https://docs.nestjs.com/providers) … サービスとコンストラクターでの依存性の注入

## この節を終えたときのディレクトリ

::tree

:::download
[この節を終えた状態をダウンロード](./project.zip)
:::

:::faq

### `npm run start:dev` で `EADDRINUSE: address already in use :::3000` と出る

3000 番ポートを別のプログラムが使っています。前に起動した API が別のターミナルに残っていないか確かめ、Ctrl + C で止めてください。

### ZIP をダウンロードして始めたら動かない

ZIP には `node_modules/` が入っていません。展開した `api/` で `npm install` を実行してから動かしてください。

:::
