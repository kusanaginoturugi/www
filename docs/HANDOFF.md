# 引き継ぎ

## 表示テーマ

- 初期テーマは OS の `prefers-color-scheme` に従う。
- 手動選択は `localStorage` の `showway-theme` に `light` または `dark` として保存される。
- 実装は `layouts/partials/head-additions.html`、`layouts/partials/site-scripts.html`、`assets/js/theme-toggle.js`、`assets/ananke/css/custom.css`。
- ヘッダーとフッターは既存の Ananke 配色を維持する。`custom.css` で背景色を指定しないこと。

## 多言語

- 日本語: `/`
- English: `/en/`
- 翻訳済みなのは固定ページのみ。ブログ本文は日本語のままなので、英語の記事を増やすときは同じ slug の `.en.md` を `content/posts/` に置く。

## 実績リスト画像

- `static/images/actual-list-wisteria.png` を日本語・英語の実績リストで共用している。
- `cover_dimming_class: 'bg-black-20'` を指定して、画像内の暗め処理と重なっても見出しが読める濃さにしている。

## サービスとブログ

- `content/posts/cloudflare-small-business-services.md` は、Tailscale / authentik を含む社内アクセス・認証基盤のサービス記事。タイトルを変えても、旧 URL を維持するため slug を固定している。
- `content/posts/memos-mcp-with-codex.md` はセルフホスト Memos の MCP 接続手順。実際のホスト名や PAT は載せない。
- `content/posts/tailscale-authentik-small-team.md` は Tailscale と authentik の役割分担を説明する記事。実案件の構成を断定する表現は避けている。
