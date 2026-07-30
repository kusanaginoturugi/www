# 引き継ぎ

## 表示テーマ

- 初期テーマは OS の `prefers-color-scheme` に従う。
- 手動選択は `localStorage` の `showway-theme` に `light` または `dark` として保存される。
- 実装は `layouts/partials/head-additions.html`、`layouts/partials/site-scripts.html`、`assets/js/theme-toggle.js`、`assets/ananke/css/custom.css`。
- ヘッダーとフッターは既存の Ananke 配色を維持する。`custom.css` で背景色を指定しないこと。

## 多言語

- 日本語: `/`
- English: `/en/`
- 鹿児島弁: `/kagoshima/`
- 翻訳済みなのは固定ページのみ。ブログ本文は日本語のままなので、英語・鹿児島弁の記事を増やすときは同じ slug の `.en.md` / `.kagoshima.md` を `content/posts/` に置く。

## 実績リスト画像

- `static/images/actual-list-wisteria.png` を日本語・英語・鹿児島弁の実績リストで共用している。
- `cover_dimming_class: 'bg-black-20'` を指定して、画像内の暗め処理と重なっても見出しが読める濃さにしている。
