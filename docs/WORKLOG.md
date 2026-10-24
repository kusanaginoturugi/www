# 作業記録

## 2026-07-30

- ライト/ダークモードを追加。OS 設定を初期値にし、ヘッダー操作の選択は `localStorage` の `showway-theme` に保存する。
- `/en/` を追加し、トップ、事業内容、実績、会社情報、お問い合わせを翻訳した。
- テーマ本体を変更せず、`layouts/partials/` と `assets/` の上書きで実装した。
- `hugo --minify` が日本語・英語の全ページで成功した。
- 127.0.0.1 の Hugo 開発サーバーで、デスクトップとモバイル幅のヘッダー表示を確認した。
- 参照サイト由来の緑系配色は取り消し、従来のヒーロー画像上の黒いオーバーレイと白文字に戻した。
- 甲州弁版は中止し、鹿児島弁版へ置き換えた。
- 実績リストへ藤棚の横長アイキャッチを追加し、トリミングと暗め処理を適用した。

## 2026-10-09

- `memos-mcp-with-codex` と `tailscale-authentik-small-team` の2記事を追加した。
- 既存のサービス記事から Cloudflare Tunnel / Access の訴求を外し、Tailscale / authentik による社内アクセス・認証基盤へ更新した。
- 既存サービス記事の slug を固定し、タイトル変更後も旧 URL を維持した。
- `hugo --minify` が成功し、新規記事2本がブログ一覧に出ることを確認した。

## 2026-10-09: 鹿児島弁版の整理

- 鹿児島弁版は言語切替と公開構成から外し、ブログ記事として実装事例を残した。

## 2026-10-24: セキュリティ点検

- 点検対象: Hugo 本体、テーマ (submodule)、ブラウザ側 JS、公開ヘッダー、`scripts/`、リポジトリ内のシークレット。npm の依存はない。
- Hugo: Cloudflare Pages の `HUGO_VERSION` が 0.162.0 のままで、0.166.0〜0.168.0 で修正された medium の advisory が 10 件あった (TOC 見出しや lineAnchors の stored XSS、テーマ経由のファイル読み取りなど)。記事は自作でテーマもタグ固定のため悪用の余地は小さいが、Pages の production/preview と CI を 0.168.0 にそろえた。
- テーマ: Ananke v2.17.0 → 最新 v2.19.1 は、このサイトで上書きしている `head-additions` / `site-scripts` / `list` / `summary` 自体が変わるため今回は見送った。セキュリティ修正は含まれていない。未対応事項として残す。
- ヘッダー: 本番は `nosniff` と `Referrer-Policy` だけだった。`static/_headers` で CSP (`script-src 'self'`)、`X-Frame-Options: DENY`、`Permissions-Policy`、HSTS (サブドメインなし) を追加した。
- CSP に合わせて、`head-additions.html` の inline script を `assets/js/theme-init.js` (defer なし、SRI 付き) に移した。
- `scripts/import-wp.sh`: WP API の slug をそのままファイル名にしていたため、`/` や `..` を含む slug を無視するようにした。旧 WP の API はすでに 404。
- シークレット: `git grep` でトークンや秘密鍵の形式は見つからなかった。Secret scanning と push protection はすでに有効だった。
- GitHub: Dependabot (github-actions 週次)、CI (Hugo ビルド、inline script 検出、Hugo/テーマの新版 warning、週次)、CodeQL (actions / javascript-typescript / python)、Dependency Review を追加した。Dependabot 脆弱性アラートを有効にした。main の保護設定と Dependabot security updates は変更していない。
- 検証: ローカルの Hugo 0.168.0 で `hugo --minify` が成功し、出力に inline script がないことを確認した。
