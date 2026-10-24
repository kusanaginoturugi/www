# 脆弱性点検・対策の共通手順

kusanaginoturugi の GitHub リポジトリ向けの共通手順。npm / Cloudflare Workers のプロジェクト ([npbinfo](https://github.com/kusanaginoturugi/npbinfo/blob/main/docs/security-maintenance-playbook.md)) と、Hugo + Cloudflare Pages の静的サイト ([www](https://github.com/kusanaginoturugi/www)) で行った作業をまとめたもの。repo の構成に当てはまる節だけ実施する。repo 側に既存の方針があればそちらを優先する。

| 節 | npm / Workers | Hugo + Pages |
|---|---|---|
| 1. 現状確認 | ○ | ○ |
| 2. npm 依存 | ○ | テーマ開発用の package.json だけなら不要 |
| 3. Hugo 本体 | − | ○ |
| 4. テーマ | − | ○ |
| 5. コードの点検 | ○ | `scripts/` と JS |
| 6. セキュリティヘッダー | Worker が HTML を返すなら | ○ |
| 7. GitHub の設定 | ○ | ○ |
| 8. 反映と確認 | ○ | ○ |
| 9. 記録 | ○ | ○ |

## 依頼文 (Claude / Codex に渡す)

> このリポジトリの脆弱性を点検して対策し、GitHub で継続検出できるようにしてください。手順は https://github.com/kusanaginoturugi/www/blob/main/docs/security-runbook.md に従い、この repo の構成に当てはまる節だけ実施してください。既存のユーザー変更は戻さないでください。main の保護設定は変更しないでください。commit/push とデプロイは CLAUDE.md の方針に従い、push した場合は CI とデプロイ、本番の反映まで確認してください。権限確認が多くならないよう、コマンドはまとめて実行してください。

## 進め方

- 調査、ビルドと検証、コミットと push、push 後の確認を、それぞれ1回の Bash にまとめる。ファイル作成は Write/Edit で一度に出し、その後にまとめて検証する。
- 監査ツールの件数は依存ツリー全体の集計で、独立した攻撃経路の数ではない。監査結果だけで「外部から悪用できる／できない」と断定しない。
- 更新は種類ごとに別コミットにする (依存更新、ヘッダー追加、テーマ更新、CI 追加)。戻しやすくするため。

## 1. 現状確認 (読み取りだけ)

```sh
git status --short
git ls-files | grep -vE '^(content|static/images)/' | head -100
ls .github/workflows .github/dependabot.yml 2>/dev/null; cat .github/workflows/* 2>/dev/null
cat package.json wrangler.json* wrangler.toml hugo.toml 2>/dev/null
ls package-lock.json static/_headers 2>/dev/null
git submodule status
gh repo view --json nameWithOwner,visibility,viewerPermission
gh api repos/OWNER/REPO --jq .security_and_analysis
gh api -X GET repos/OWNER/REPO/vulnerability-alerts -i | head -1      # 404 なら無効
curl -sSI https://<本番>/                                              # 現在のヘッダー
```

Cloudflare の設定は wrangler のログイン情報で API から読める。トークンは表示しない。

```sh
T=$(wrangler auth token 2>/dev/null | tail -1)
A=$(curl -sS -H "Authorization: Bearer $T" https://api.cloudflare.com/client/v4/accounts | jq -r '.result[0].id')
wrangler pages project list
curl -sS -H "Authorization: Bearer $T" \
  "https://api.cloudflare.com/client/v4/accounts/$A/pages/projects/<PROJECT>" \
  | jq '{build_config:.result.build_config, prod:.result.deployment_configs.production.env_vars, prev:.result.deployment_configs.preview.env_vars}'
```

`wrangler` を実行すると `.wrangler/` ができるので `.gitignore` に入れる。

## 2. npm 依存

基準値を取る。

```sh
npm audit
npm audit --omit=dev
npm outdated --json
npm ls <指摘のpackage> --all      # 依存経路
```

- 直接の開発依存は `npm install -D <package>@latest ...` で更新し、lockfile も同時に更新する。
- `npm audit fix --force` は、提案されるダウングレードや破壊的変更を調べずに実行しない。
- 間接依存の `overrides` は、修正版と互換性を確認できた場合だけ追加する。外す条件を記録に書く。
- Cloudflare Workers では、`devDependency` でも Worker に import されてバンドルされていることがある。import 経路を確認してから影響を判断する。
- 残る指摘は、実際の利用経路と修正版の有無を記録する。

## 3. Hugo 本体

```sh
gh release view -R gohugoio/hugo --json tagName
gh api 'repos/gohugoio/hugo/security-advisories?per_page=30' \
  --jq '.[]|[.ghsa_id,.severity,.summary,(.vulnerabilities|map(.patched_versions)|join(","))]|@tsv'
curl -s https://<本番>/ | grep -oE '<meta name=generator[^>]*>'      # 本番の Hugo 版
```

- Pages の `HUGO_VERSION` より後で修正された advisory を数える。多くは「信頼できないテーマ・コンテンツによる XSS やファイル読み取り」なので、自作コンテンツ + タグ固定テーマなら影響は小さい。過大に書かず、それでも更新する。
- 先にローカルの最新版で `hugo --minify -d <scratch>/before` が通ることを確かめる。
- Pages の環境変数を production・preview まとめて更新する。変更だけでは再ビルドされず、次の push で反映される。

```sh
curl -sS -X PATCH -H "Authorization: Bearer $T" -H 'Content-Type: application/json' \
  "https://api.cloudflare.com/client/v4/accounts/$A/pages/projects/<PROJECT>" \
  -d '{"deployment_configs":{"production":{"env_vars":{"HUGO_VERSION":{"type":"plain_text","value":"X.Y.Z"}}},"preview":{"env_vars":{"HUGO_VERSION":{"type":"plain_text","value":"X.Y.Z"}}}}}' \
  | jq -c '{success, errors}'
```

- 同じ版を CI の `HUGO_VERSION` と README にも書く。

## 4. テーマ (Hugo、git submodule)

Hugo Modules の場合は `hugo mod get -u` に置き換える。

```sh
git -C themes/<theme> fetch --tags -q origin
gh release view -R <theme-repo> --json tagName
git -C themes/<theme> diff --stat <現tag> <新tag> -- layouts/
git -C themes/<theme> diff <現tag> <新tag> -- <サイト側で上書きしているファイル>
git -C themes/<theme> checkout -q <新tag>
```

- サイト側 `layouts/` で上書きしているファイルがテーマ側で変わっていれば、上書きが古くなっていないか読む。Hugo 0.146 以降はテーマが `layouts/_partials/` に移っていても、サイト側 `layouts/partials/` の上書きは効く。
- 更新前後で `hugo --minify -d <scratch>/before|after` を出し、`diff -rq` で変わったファイルを出す。minify 後は1行なので `diff <(sed 's/></>\n</g' before/x.html) <(sed 's/></>\n</g' after/x.html)` で中身を見る。全ページが変わるのは CSS の fingerprint 変更であることが多い。
- テーマの partial に inline `<script>` が増えていたら、CSP に合わないので `assets/js/` に移し、上書きした partial から `resources.Get | minify | fingerprint` で読む。
- 見た目は headless Chromium で確認する (Chrome 拡張がなくても使える)。

```sh
hugo server --port 1414 --bind 127.0.0.1 >/dev/null 2>&1 & echo $! > <scratch>/hugo.pid
chromium --headless=new --disable-gpu --hide-scrollbars --window-size=1280,1400 --screenshot=<scratch>/home.png   http://127.0.0.1:1414/
chromium --headless=new --disable-gpu --hide-scrollbars --window-size=390,1400  --screenshot=<scratch>/mobile.png http://127.0.0.1:1414/
chromium --headless=new --disable-gpu --virtual-time-budget=3000 --dump-dom http://127.0.0.1:1414/<page> | grep ...   # JS 実行後の DOM
kill $(cat <scratch>/hugo.pid)     # pkill -f は自分のシェルにも一致して落ちるので使わない
```

- Dependabot の `gitsubmodule` は submodule のブランチ HEAD を追うので使わない。CI でリリースタグとの差を warning にする (7 節の CI 雛形)。

## 5. コードの点検

- 認証、リクエスト本文の上限、外部 URL とファイルパス、HTML 出力、シークレットの扱いを見る (公開 API がある場合)。
- `scripts/` のシェル・Python: 外部から取った値をファイル名やパスに使っていないか。`''|.|..|*/*` を弾く。
- Hugo の `markup.goldmark.renderer.unsafe = true` は、他人の書いた Markdown を載せないなら許容してよい。理由を記録する。
- シークレット:

```sh
git grep -nIE '(AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{36}|github_pat_|sk-[A-Za-z0-9]{20,}|xox[bp]-|-----BEGIN [A-Z ]*PRIVATE KEY)'
```

## 6. セキュリティヘッダー

Cloudflare Pages / Workers Static Assets は `_headers` (Hugo なら `static/_headers`)、Worker が HTML を返す場合はレスポンスで付ける。先にビルド結果を棚卸しする。

```sh
grep -rlE '<script>|<script [^>]*>[^<]' public --include='*.html'               # inline script
grep -rhoE '<style|on(click|load|error|submit)=|<iframe|<form[^>]*' public | sort | uniq -c
grep -rhoE 'style=[^ >]{0,40}' public | sort | uniq -c | sort -rn | head         # minify で引用符が消える
grep -rhoE '(src|srcset|action)="?https?://[^/" >]+' public | sort | uniq -c      # 外部ホスト
curl -s https://<本番>/contact/ | grep -oE '<script[^>]*>'                       # Cloudflare が差し込む script
```

- inline script はすべて外部ファイルにする。表示前に必要なもの (ダークモード初期化など) は `defer` を付けずに `<head>` で読む。
- コードハイライトやテーマが `style=` 属性を出すなら `style-src 'unsafe-inline'` は必要。
- Cloudflare のメール難読化は `/cdn-cgi/` の同一オリジン script なので `'self'` で動く。Web Analytics や Rocket Loader を使っていれば、そのホストを `script-src` / `connect-src` に足す。
- 埋め込み (YouTube など) やフォームがあれば `frame-src` / `form-action` に足す。
- HSTS は `includeSubDomains` / `preload` を付けない。全サブドメインの HTTPS を確認してから検討する。

```
/*
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Strict-Transport-Security: max-age=31536000
```

## 7. GitHub の設定

既存の設定がなければ追加する。Actions は commit SHA で固定する。最新の SHA は次で調べ、下の雛形の SHA を置き換える。

```sh
for r in actions/checkout actions/setup-node actions/dependency-review-action; do t=$(gh release view -R $r --json tagName --jq .tagName); echo "$r $t $(gh api repos/$r/commits/$t --jq .sha)"; done
gh api repos/github/codeql-action/tags --jq '[.[]|select(.name|test("^v4\\.[0-9]+\\.[0-9]+$"))][0]|[.name,.commit.sha]|@tsv'
```

### `.github/dependabot.yml`

npm がない repo は `npm` の項を消す。

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
      timezone: Asia/Tokyo
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
      timezone: Asia/Tokyo
    groups:
      github-actions:
        patterns:
          - "*"
```

### `.github/workflows/ci.yml` (npm)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "0 0 * * 1"

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7.1.0
        with:
          node-version: 24
          cache: npm
      - run: npm ci
      - run: npm test
      - run: npm audit --omit=dev --audit-level=high
```

### `.github/workflows/ci.yml` (Hugo)

`HUGO_VERSION` は Pages の環境変数と、テーマのリポジトリ名は実際のものとそろえる。

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "0 0 * * 1"
  workflow_dispatch:

permissions:
  contents: read

env:
  # Cloudflare Pages の環境変数 HUGO_VERSION と揃える
  HUGO_VERSION: 0.168.0

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          submodules: true
          persist-credentials: false

      - name: Install Hugo
        run: |
          curl -fsSL -o hugo.deb "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb"
          sudo dpkg -i hugo.deb
          hugo version

      - name: Build
        run: hugo --minify

      - name: Check security headers file
        run: grep -q "Content-Security-Policy" public/_headers

      - name: Check inline scripts
        # CSP の script-src 'self' を壊す inline script がないか確認する
        run: |
          if grep -rlE '<script>|<script [^>]*>[^<]' public --include='*.html'; then
            echo "::error::inline script が出力されています"
            exit 1
          fi

      - name: Check Hugo and theme releases
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          latest_hugo=$(gh release view -R gohugoio/hugo --json tagName --jq .tagName)
          if [ "v${HUGO_VERSION}" != "$latest_hugo" ]; then
            echo "::warning::Hugo ${latest_hugo} が出ています (固定版 v${HUGO_VERSION})"
          fi
          # submodule は shallow checkout でタグがないため commit SHA で比べる
          current_theme=$(git -C themes/ananke rev-parse HEAD)
          latest_theme=$(gh release view -R theNewDynamic/gohugo-theme-ananke --json tagName --jq .tagName)
          latest_theme_sha=$(gh api "repos/theNewDynamic/gohugo-theme-ananke/commits/${latest_theme}" --jq .sha)
          if [ "$current_theme" != "$latest_theme_sha" ]; then
            echo "::warning::Ananke ${latest_theme} が出ています (現在 ${current_theme})"
          fi
```

### `.github/workflows/codeql.yml`

`language` は repo にある言語に合わせる (`actions` は常に入れる。`javascript-typescript`、`python` など)。

```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 1 * * 1"

permissions:
  contents: read

jobs:
  analyze:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    permissions:
      contents: read
      security-events: write
      actions: read
    strategy:
      fail-fast: false
      matrix:
        language: [actions, javascript-typescript]
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: github/codeql-action/init@9b3254085494b55a0f7c4c2b3d2d52cc712ce370 # v4.39.1
        with:
          languages: ${{ matrix.language }}
          build-mode: none
          queries: security-extended
      - uses: github/codeql-action/analyze@9b3254085494b55a0f7c4c2b3d2d52cc712ce370 # v4.39.1
        with:
          category: /language:${{ matrix.language }}
```

### `.github/workflows/dependency-review.yml`

```yaml
name: Dependency Review

on:
  pull_request:

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: actions/dependency-review-action@a1d282b36b6f3519aa1f3fc636f609c47dddb294 # v5.0.0
        with:
          fail-on-severity: high
```

private repo では、CodeQL と Dependency Review に GitHub Advanced Security が必要なことがある。利用条件を確認する。

### 脆弱性アラート

対象 repo の管理権限を確認してから有効にし、204 を確認する。

```sh
gh repo view --json nameWithOwner --jq .nameWithOwner
gh api -X PUT repos/OWNER/REPO/vulnerability-alerts -i | head -1
gh api -X GET repos/OWNER/REPO/vulnerability-alerts -i | head -1
gh api 'repos/OWNER/REPO/dependabot/alerts?state=open' --jq length
```

- 有効化直後の一覧が空でも、ローカル監査の指摘が解消したとは判断しない。
- Secret scanning と push protection は public repo なら通常すでに有効。`security_and_analysis` で確認する。
- 自動修正 PR の Dependabot security updates は別の設定。main の保護設定と合わせて、依頼がなければ変えない。

## 8. 反映と確認

push 前にローカルで `npm ci` / テスト / ビルド / `npm audit --omit=dev --audit-level=high` (npm)、`hugo --minify` と inline script 検出 (Hugo) を通す。失敗した項目は更新前からの問題かを切り分ける。

push 後:

```sh
sha=$(git rev-parse HEAD); sleep 20      # 直後は gh run list が空のことがある
for id in $(gh run list --commit $sha --json databaseId --jq '.[].databaseId'); do gh run watch $id --exit-status >/dev/null 2>&1; done
gh run list --commit $sha --json name,conclusion --jq '.[]|[.name,.conclusion]|@tsv'
gh run view $(gh run list --workflow CI --commit $sha --json databaseId --jq '.[0].databaseId') --log | grep '##\[warning\]'
gh api repos/OWNER/REPO/commits/$sha/check-runs --jq '.check_runs[]|[.name,.status,.conclusion]|@tsv'   # Cloudflare Pages / Workers Builds
curl -sSI https://<本番>/ | grep -iE 'content-security|x-frame|strict-transport|permissions-policy'
curl -s  https://<本番>/ | grep -oE 'Hugo [0-9.]+'
gh api 'repos/OWNER/REPO/code-scanning/alerts?state=open' --jq length
```

- Worker をデプロイした場合は、公開 API の build 情報などで反映を確認する。
- Pages は `/foo.html` を `/foo` に 308 リダイレクトする。本番の記事ページは `curl -L` で取る。
- CodeQL の初回完了前は、code-scanning API が 404 (`no analysis found`) を返す。

## 9. 記録

repo の作業履歴 (`docs/WORKLOG.md` など) に書く。

- 日付、更新したパッケージ・Hugo・テーマの前後の版
- 監査の前後件数、該当した advisory、残る指摘と影響範囲
- 追加したヘッダー、GitHub の設定
- 検証結果
- 見送った事項とその理由、次に外す override

## つまずいた点

| 現象 | 原因 | 対処 |
|---|---|---|
| CI のテーマ版チェックがタグ名ではなく SHA を返す | `actions/checkout` の submodule は shallow でタグがない | 最新リリースのタグを API で SHA にして `rev-parse HEAD` と比べる |
| ビルド後の HTML に `style="` が見つからない | minify で属性の引用符が消え、全体が1行になる | `style=` で検索し、差分は `sed 's/></>\n</g'` で改行してから見る |
| `pkill -f '<コマンド>'` の後の処理が実行されない | 自分のシェルのコマンドラインにも一致して終了した | 起動時の PID を控えて `kill` する |
| 本番の記事ページの中身が空 | Pages の `.html` → 拡張子なしへのリダイレクト | `curl -L` |
| `gh run list` が空 | push 直後はまだ登録されていない | 20 秒ほど待ってから取る |
| CF の環境変数を変えたのに古い Hugo のまま | 環境変数の変更では再ビルドされない | 変更後に push する |
| Dependabot の submodule 更新が使えない | ブランチ HEAD を追い、リリースタグを見ない | `gitsubmodule` を入れず、CI の warning で気づく |
