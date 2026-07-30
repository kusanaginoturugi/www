# 引き継ぎ

## 表示テーマ

- 初期テーマは OS の `prefers-color-scheme` に従う。
- 手動選択は `localStorage` の `showway-theme` に `light` または `dark` として保存される。
- 実装は `layouts/partials/head-additions.html`、`layouts/partials/site-scripts.html`、`assets/js/theme-toggle.js`、`assets/ananke/css/custom.css`。
- ヘッダーとフッターは既存の Ananke 配色を維持する。`custom.css` で背景色を指定しないこと。

## 多言語

- 日本語: `/`
- English: `/en/`
- 甲州弁: `/koshu/`
- 翻訳済みなのは固定ページのみ。ブログ本文は日本語のままなので、英語・甲州弁の記事を増やすときは同じ slug の `.en.md` / `.koshu.md` を `content/posts/` に置く。
