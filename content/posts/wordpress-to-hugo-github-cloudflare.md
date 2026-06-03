---
title: "WordPress のサイトを Hugo/GitHub/Cloudflare Pages に移管した"
date: 2026-06-03T09:00:04+09:00
slug: "wordpress-to-hugo-github-cloudflare"
categories: ["コンピューター"]
tags: ["WordPress", "Hugo", "GitHub", "Cloudflare"]
summary: "長年 WordPress で動かしていた自社サイトを、Hugo で静的サイト化し、GitHub で管理して Cloudflare Pages から公開する構成に移管しました。記事の取り込み、URL 維持、Cloudflare Pages の設定、移管後の運用についてまとめます。"
---

長年 WordPress で動かしていた自社サイトを、Hugo + GitHub + Cloudflare Pages の構成に移管しました。

WordPress は便利ですが、会社案内や古いブログ記事が中心のサイトでは、ログイン画面、プラグイン、データベース、PHP の更新、バックアップなど、動的 CMS として維持するための作業が少し重くなってきます。更新頻度が高くないサイトなら、静的サイトにしてしまった方が運用が単純になります。

今回の移管では、次の構成にしました。

- 静的サイトジェネレーター: Hugo
- テーマ: Ananke
- ソース管理: GitHub
- 公開先: Cloudflare Pages
- URL: 旧 WordPress 時代の `/<slug>.html` 形式をなるべく維持

## WordPress から記事を取り込む

WordPress の記事は、WordPress REST API から取得しました。

`/wp-json/wp/v2/posts` で記事一覧を取得し、カテゴリとタグも API から取得します。本文 HTML は `pandoc` で Markdown に変換し、Hugo の `content/posts/` 以下に出力しました。

変換用に `scripts/import-wp.sh` を用意しました。

```sh
./scripts/import-wp.sh
```

必要なコマンドは `curl`, `jq`, `pandoc` です。

スクリプトの流れは次の通りです。

1. WordPress REST API から投稿一覧を取得する
2. カテゴリとタグを取得する
3. 投稿本文の HTML を Markdown に変換する
4. Hugo 用の front matter を付けて `content/posts/<slug>.md` に保存する

移行後の記事は、例えば次のような front matter になります。

```yaml
---
title: "記事タイトル"
date: 2025-06-25T09:43:25
slug: "awssummit2025"
categories: ["コンピューター"]
tags: []
---
```

完全な変換を目指すと大変なので、まずは本文、カテゴリ、タグ、日付、slug をきちんと移すことを優先しました。WordPress 由来の `alignnone` や `wp-image-xxxx` のような class は残っていますが、表示に大きな問題がなければ後から整理できます。

## Hugo の URL を WordPress 時代に寄せる

移管で一番気をつけたのは URL です。

WordPress 時代の記事 URL は `/<slug>.html` 形式でした。検索エンジンや外部リンクからのアクセスを考えると、ここを変えない方が安全です。

Hugo 側では `hugo.toml` に次の設定を入れました。

```toml
[permalinks]
  posts = '/:slug'

[uglyURLs]
  posts = true
```

これで `content/posts/example.md` のような記事が、`/example.html` として出力されます。

固定ページは Hugo の通常の構成に合わせて、会社情報、事業内容、実績、お問い合わせを `content/about/`, `content/services/`, `content/actual_list/`, `content/contact/` に置きました。

## ローカルで確認する

ローカルでは Hugo の開発サーバーで確認します。

```sh
hugo server -D
```

本番ビルドと同じ条件で確認したい場合は、次のコマンドで静的ファイルを生成します。

```sh
hugo --minify
```

出力先は `public/` です。Cloudflare Pages でもこの `public/` を公開ディレクトリとして使います。

## GitHub に置く

Hugo のプロジェクト一式を GitHub リポジトリで管理します。

今回の構成では、Hugo のテーマ `ananke` は `themes/ananke/` に置いています。クローン直後はテーマも取得する必要があります。

```sh
git submodule update --init --recursive
```

記事を追加・修正したら GitHub に push します。以後は GitHub の `main` ブランチが公開の起点になります。

## Cloudflare Pages で公開する

Cloudflare Pages では、GitHub リポジトリを接続して自動デプロイするようにしました。

設定は次の通りです。

- Framework preset: Hugo
- Build command: `hugo --minify`
- Build output directory: `public`
- Production branch: `main`
- Environment variable: `HUGO_VERSION=0.162.0`

GitHub の `main` ブランチに push すると、Cloudflare Pages が Hugo をビルドして公開します。

Cloudflare Pages の GitHub 連携が切れていると、自動デプロイが失敗することがあります。Cloudflare の画面で「Git アカウントから切断されています」という警告が出ている場合は、GitHub 連携を再認可します。

## カスタムドメインを切り替える

Cloudflare Pages のデプロイが成功したら、カスタムドメインに `www.showway.biz` を追加します。

DNS も Cloudflare で管理している場合は、Pages 側の案内に従って DNS レコードを切り替えます。表示確認ができたら、旧 WordPress が動いていたサーバーは停止できます。

移管直後は次の点を確認しました。

- トップページが表示されるか
- 主要な固定ページが表示されるか
- 旧記事の `/<slug>.html` URL が表示されるか
- 画像のパスが切れていないか
- sitemap.xml と robots.txt が生成されているか

## 移管してよかった点

一番大きいのは、運用が単純になったことです。

WordPress のために PHP、データベース、プラグイン、管理画面を維持する必要がなくなりました。記事やページは Markdown ファイルとして GitHub に残るので、変更履歴も追いやすくなります。

また、Cloudflare Pages で配信するため、通常の会社サイトとしては十分に速く、サーバー管理の手間もかなり減ります。

もちろん、WordPress の管理画面で記事を書くような使い勝手はなくなります。そのかわり、更新頻度が低く、構成が大きく変わらないサイトでは、静的サイトの方が素直に運用できます。

## 今後の作業

移管は完了しましたが、細かい改善は残っています。

- WordPress 由来の古い class の整理
- アイキャッチ画像の設定
- OGP 画像や description の調整
- Google Search Console の確認
- 旧カテゴリ・タグ・年月アーカイブ URL の扱い確認

まずはサイトを静的化して、GitHub に置き、Cloudflare Pages から公開するところまでできました。今後は WordPress の保守ではなく、Hugo 側のコンテンツ整理に時間を使えます。
