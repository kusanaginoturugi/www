# www.showway.biz

Showway (IT 開発受託・コンサルティング) の公式サイト。
Hugo + Ananke テーマで構築、Cloudflare Pages で公開。

## ローカル開発

```sh
# 依存
# - hugo (extended, 0.160+ )
# - git (submodule 取得のため)

# クローン直後はテーマを取得
git submodule update --init --recursive

# 開発サーバ
hugo server -D

# 本番ビルド
hugo --minify
```

## ディレクトリ構成

```
content/
  _index.md           トップ
  _index.en.md        英語トップ
  about/              会社情報
  services/           事業内容
  contact/            問い合わせ
  posts/              ブログ記事 (WP から移行)
themes/ananke/        テーマ (git submodule)
scripts/
  import-wp.sh        WordPress 記事を Markdown に変換するスクリプト
hugo.toml             サイト設定
```

## 最近追加した記事

- `content/posts/memos-mcp-with-codex.md`: セルフホスト Memos を Codex の MCP として使う手順
- `content/posts/tailscale-authentik-small-team.md`: Tailscale と authentik のアクセス・認証の役割分担

## 表示言語とテーマ

- 日本語 (既定): `/`
- English: `/en/`

トップ、事業内容、実績、会社情報、お問い合わせは日本語と英語で用意している。ヘッダーの切替で OS のライト/ダーク設定を初期値にし、手動で選んだ表示モードはブラウザに保存する。

実装の経緯と保守時の注意点は `docs/PLAN.md`、`docs/WORKLOG.md`、`docs/HANDOFF.md` を参照。

## URL 構造

WordPress 時代と同じ `/<slug>.html` 形式 (`uglyURLs` + permalink `/:slug` で実現)。

## デプロイ (Cloudflare Pages)

GitHub の `main` ブランチに push されたら、Cloudflare Pages が自動でビルドして公開する。

### 初回のセットアップ

1. Cloudflare ダッシュボード → **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**
2. リポジトリ `kusanaginoturugi/www` を選択
3. **Production branch**: `main`
4. **Build settings**:
   - Framework preset: **Hugo**
   - Build command: `hugo --minify`
   - Build output directory: `public`
   - Root directory: `/` (空欄)
5. **Environment variables** に追加:
   - `HUGO_VERSION` = `0.162.0`
6. **Save and Deploy**

### カスタムドメイン

1. デプロイ完了後、Pages プロジェクトの **Custom domains** に `www.showway.biz` を追加
2. Cloudflare DNS で対象ドメインの A/CNAME を Pages 向けに変更 (Cloudflare 上の DNS なら自動で案内が出る)
3. 旧 EC2 オリジン (WordPress) は切替確認後に停止

## WordPress 記事の再取り込み

旧サイトに記事を追加した場合などに使う。

```sh
./scripts/import-wp.sh
```
