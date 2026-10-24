# 脆弱性点検手順 (Hugo + Cloudflare Pages)

[npbinfo の手順](https://github.com/kusanaginoturugi/npbinfo/blob/main/docs/security-maintenance-playbook.md) を、npm 依存のない Hugo 静的サイト向けに置き換えたもの。他の Hugo サイトに使える共通手順は [hugo-pages-security-runbook.md](hugo-pages-security-runbook.md)。

## 構成と攻撃面

- 公開物は Hugo が出力する静的ファイルだけ。サーバー側の API、フォーム、認証、シークレットはない。
- ビルドは Cloudflare Pages の Git 連携 (プロジェクト `www`)。Hugo のバージョンは Pages の環境変数 `HUGO_VERSION` で決まる。
- 依存は Hugo 本体、テーマ `themes/ananke` (git submodule)、GitHub Actions の3つ。npm の lockfile はない (テーマ内の `package.json` はテーマ開発用で、このサイトのビルドでは使わない)。
- ブラウザ側の JS は `assets/js/theme-init.js`、`assets/js/theme-toggle.js`、`assets/js/code-copy.js` (テーマのコピーボタン処理を外部ファイル化したもの) だけ。いずれも fingerprint + SRI 付きで配信する。

## 定期点検

1. Hugo: `gh release view -R gohugoio/hugo` で最新版を確認し、`gh api repos/gohugoio/hugo/security-advisories` で固定版より後に修正された advisory を見る。
2. 更新するときは、ローカルの同じ版で `hugo --minify` が通ることを確認してから、次の3か所を同じ版にそろえる。
   - Cloudflare Pages の `HUGO_VERSION` (production と preview の両方)
   - `.github/workflows/ci.yml` の `HUGO_VERSION`
   - `README.md` の初回セットアップ手順
3. テーマ: `gh release view -R theNewDynamic/gohugo-theme-ananke` と `git -C themes/ananke describe --tags` を比べる。Dependabot は submodule のブランチ HEAD を追うため使っていない。更新するときは、上書きしている `layouts/partials/`、`layouts/list.html`、`layouts/summary.html` がテーマ側で変わっていないか `git -C themes/ananke diff <旧tag> <新tag> -- layouts/` で確認し、更新前後の `public/` を `diff -r` で比べる。テーマの `_partials/site-scripts.html` が変わったら、`assets/js/code-copy.js` にも反映する。
4. GitHub Actions は Dependabot が週次で PR を出す。Actions は commit SHA で固定する。
5. CI の週次実行で、Hugo とテーマに新しいリリースがあれば warning が出る。
6. GitHub の Security タブで Dependabot alerts、Code scanning (CodeQL: actions / javascript-typescript / python)、Secret scanning を確認する。

## セキュリティヘッダー

`static/_headers` で全パスに CSP、`X-Frame-Options`、`Referrer-Policy`、`Permissions-Policy`、HSTS を付ける。

- `script-src 'self'` のため inline script は使わない。JS は `assets/js/` に置いて `resources.Get | minify | fingerprint` で読み込む。CI が `public/` 内の inline script を検出すると失敗する。
- `style-src` はコードハイライトとテーマが `style=` 属性を出力するため `'unsafe-inline'` を許可している。
- 記事内に外部画像 (paypalobjects.com) があるため `img-src` は `https:` を許可している。
- Cloudflare のメールアドレス難読化は `/cdn-cgi/` の同一オリジン script なので `'self'` で動く。
- HSTS は `includeSubDomains` / `preload` を付けていない。全サブドメインが HTTPS であることを確認してから検討する。
- 反映確認: `curl -sI https://www.showway.biz/`

## 許容しているリスク

- `markup.goldmark.renderer.unsafe = true`: WordPress から移した記事が HTML を含むため。記事は自分で書いたものだけなので許容する。外部から受け取った Markdown を載せる場合は見直す。
- 古い記事の `target="_blank"` リンクに `rel="noopener"` がない: 現行ブラウザは `target="_blank"` を noopener 扱いにするため対応していない。
- `access-control-allow-origin: *`: Cloudflare Pages が静的ファイルに付ける既定値。公開情報だけなので問題ない。

## 作業履歴

[WORKLOG](WORKLOG.md) の「セキュリティ点検」の項を参照。
