# TODO

このファイルは積み残し作業のメモ。終わったものは消すか取り消し線にする。

## ユーザー側で必要な操作

- [ ] Cloudflare Pages でリポジトリ連携
  - Workers & Pages → Create application → Pages → Connect to Git
  - Repo: `kusanaginoturugi/www`
  - Framework preset: **Hugo**
  - Build command: `hugo --minify`
  - Build output: `public`
  - Env var: `HUGO_VERSION=0.162.0`
- [ ] カスタムドメイン `www.showway.biz` を Pages プロジェクトに追加
- [ ] DNS を Pages 向けに切替 (Cloudflare DNS なら案内に従う)
- [ ] 動作確認後、EC2 上の旧 WordPress を停止

## WP 固定ページの残り

- [ ] `about` (タイトル「紹介」, `https://www.showway.biz/about`)
  - 自前の `content/about/_index.md` (会社情報) と被るので、内容を取り込むか / 差し替えるか / 無視するか判断
- [ ] `test` (`https://www.showway.biz/test`)
  - 中身がテスト用なら無視で OK
- [ ] 取り込む方針が決まったら `scripts/import-wp.sh` を pages 対応に拡張する案もあり

## デザイン・UI

- [ ] ヒーロー画像を設定
  - `static/images/hero.jpg` を置いて `hugo.toml` の `params.intro_image = '/images/hero.jpg'`
- [ ] ファビコン (`params.favicon`)、サイトロゴ (`params.site_logo`) 設定
- [ ] page-header の中央寄せ (`tc-l`) も外したい場合は `layouts/_partials/page-header.html` を上書き
- [ ] 配色・タイポの最終調整 (Tachyons / `assets/ananke/css/custom.css`)

## コンテンツ

- [ ] 各記事のアイキャッチ (`featured_image`) は未設定。必要なら front matter に追加
- [ ] 取得不能だった画像 (`/uploads/2015/10/3.png`, `cc.png`) は img タグだけ削除済み。代替画像を入れるなら別途
- [ ] 記事内に古い WP 由来クラス (`alignnone`, `wp-image-xxxx` 等) が残っている。気になれば一括除去
- [ ] 旧サイトのカテゴリ/タグ ページのデザインを確認 (Ananke のデフォルトでよいか)

## URL / リダイレクト

- [ ] `/actual_list` (末尾スラなし) と `/actual_list/` のリダイレクト挙動を Cloudflare Pages 上で確認
  - 不足なら `static/_redirects` に手動で書く
- [ ] 旧 WordPress 独自の URL (タグ・カテゴリ・年月アーカイブ) が外部リンクされていたら個別対応

## スクリプト改善案

- [ ] `scripts/import-wp.sh`
  - 固定ページ (`/pages` API) 対応
  - アイキャッチ画像も `static/uploads/` に自動取得
  - 本文中の画像も自動ダウンロード
  - 古い WP クラスの除去オプション

## SEO / 運用

- [ ] sitemap.xml (Hugo が自動生成) の中身確認
- [ ] `robots.txt` の中身確認 (`enableRobotsTXT = true` で生成)
- [ ] OGP 画像・description のデフォルト設定
- [ ] Google Search Console の所有権確認 (新ドメイン扱いになる場合)
