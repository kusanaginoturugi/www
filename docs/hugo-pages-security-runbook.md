# Hugo + Cloudflare Pages サイトの脆弱性点検・更新手順 (共通版)

www.showway.biz で 2026-10-24 に行った作業を、他の Hugo サイトでも使える形にまとめたもの。サイト固有の内容は [security-maintenance-playbook.md](security-maintenance-playbook.md) を参照。npm 依存や Worker のコードがある repo は [npbinfo の手順](https://github.com/kusanaginoturugi/npbinfo/blob/main/docs/security-maintenance-playbook.md) と組み合わせる。

## 対象

- Hugo の静的サイトで、Cloudflare Pages の Git 連携で公開しているもの
- テーマは git submodule (Hugo Modules の場合は「テーマ更新」の手順を `hugo mod get -u` に置き換える)
- サーバー側の API やフォームがないもの (ある場合は入力処理の点検を追加する)

## 依頼文 (Claude / Codex に渡す)

> このリポジトリの脆弱性を点検して対策し、GitHub で継続検出できるようにしてください。手順は kusanaginoturugi/www の docs/hugo-pages-security-runbook.md に従ってください。Cloudflare Pages の HUGO_VERSION とテーマを最新リリースにそろえ、セキュリティヘッダーを追加し、CI・CodeQL・Dependency Review・Dependabot を設定し、Dependabot 脆弱性アラートを有効にしてください。main の保護設定は変更しないでください。push 後は CI、Pages のデプロイ、本番のヘッダーまで確認してください。権限確認が多くならないよう、コマンドはまとめて実行してください。

## 手順

### 1. 現状確認 (読み取りだけ)

1回の Bash でまとめて取る。

```sh
git status --short
git ls-files | grep -v '^content/'          # 上書きしている layouts/ assets/ static/ を把握
ls .github/workflows .github/dependabot.yml static/_headers 2>/dev/null
git submodule status
hugo version
gh repo view --json nameWithOwner,visibility,viewerPermission
gh api repos/OWNER/REPO --jq .security_and_analysis
gh api -X GET repos/OWNER/REPO/vulnerability-alerts -i | head -1   # 404 なら無効
curl -sSI https://<本番ドメイン>/                                 # 現在のヘッダー
curl -s  https://<本番ドメイン>/ | grep -oE '<meta name=generator[^>]*>'  # 本番の Hugo 版
```

Cloudflare Pages の設定は wrangler のログイン情報で API から読める (トークンは表示しない)。

```sh
T=$(wrangler auth token 2>/dev/null | tail -1)
A=$(curl -sS -H "Authorization: Bearer $T" https://api.cloudflare.com/client/v4/accounts | jq -r '.result[0].id')
wrangler pages project list
curl -sS -H "Authorization: Bearer $T" \
  "https://api.cloudflare.com/client/v4/accounts/$A/pages/projects/<PROJECT>" \
  | jq '{build_config:.result.build_config, prod:.result.deployment_configs.production.env_vars, prev:.result.deployment_configs.preview.env_vars}'
```

### 2. Hugo 本体

```sh
gh release view -R gohugoio/hugo --json tagName
gh api 'repos/gohugoio/hugo/security-advisories?per_page=30' \
  --jq '.[]|[.ghsa_id,.severity,.summary,(.vulnerabilities|map(.patched_versions)|join(","))]|@tsv'
```

- Pages の `HUGO_VERSION` より後の版で修正された advisory を数える。多くは「信頼できないテーマ・コンテンツによる XSS やファイル読み取り」なので、自作コンテンツ + タグ固定テーマのサイトでは影響は小さい。過大に書かず、それでも更新する。
- ローカルの最新版で `hugo --minify -d <scratch>/before` が通ることを先に確かめる。
- Pages の環境変数を production・preview の両方まとめて更新し、GET で確認する。環境変数の変更だけでは再ビルドされず、次の push で反映される。

```sh
curl -sS -X PATCH -H "Authorization: Bearer $T" -H 'Content-Type: application/json' \
  "https://api.cloudflare.com/client/v4/accounts/$A/pages/projects/<PROJECT>" \
  -d '{"deployment_configs":{"production":{"env_vars":{"HUGO_VERSION":{"type":"plain_text","value":"X.Y.Z"}}},"preview":{"env_vars":{"HUGO_VERSION":{"type":"plain_text","value":"X.Y.Z"}}}}}' \
  | jq -c '{success, errors}'
```

- 同じ版を `.github/workflows/ci.yml` の `HUGO_VERSION` と README にも書く。

### 3. テーマ

```sh
git -C themes/<theme> fetch --tags -q origin
gh release view -R <theme-repo> --json tagName
git -C themes/<theme> diff --stat <現tag> <新tag> -- layouts/
git -C themes/<theme> diff <現tag> <新tag> -- <上書きしているファイル>
```

- サイト側の `layouts/` で上書きしているファイルがテーマ側で変わっていれば、上書きが古くなっていないか読む。Hugo 0.146 以降はテーマが `layouts/_partials/` に移っていても、サイト側の `layouts/partials/` の上書きはそのまま効く。
- 更新前後で `hugo --minify -d <scratch>/before|after` を出し、`diff -rq` → 変わったページを `sed 's/></>\n</g'` で改行してから `diff` で中身を見る (minify 後は1行なので、そのままでは差分が読めない)。全ページが変わるのは CSS の fingerprint 変更であることが多い。
- テーマの partial に inline の `<script>` が増えていたら、CSP (`script-src 'self'`) に合わない。`assets/js/` に移し、`resources.Get | minify | fingerprint` で読み込む上書きを作る。
- 見た目は headless Chromium で確認する (Chrome 拡張がなくても使える)。

```sh
hugo server --port 1414 --bind 127.0.0.1 &   # 停止は kill <PID>。pkill -f は自分のシェルに一致して落ちるので使わない
chromium --headless=new --disable-gpu --hide-scrollbars --window-size=1280,1400 --screenshot=<scratch>/home.png http://127.0.0.1:1414/
chromium --headless=new --disable-gpu --hide-scrollbars --window-size=390,1400  --screenshot=<scratch>/mobile.png http://127.0.0.1:1414/
chromium --headless=new --disable-gpu --virtual-time-budget=3000 --dump-dom http://127.0.0.1:1414/<page> | grep ...  # JS 実行後の DOM
```

- テーマ更新は Hugo 更新・ヘッダー追加とは別コミットにする (戻しやすくするため)。

### 4. セキュリティヘッダー (`static/_headers`)

先にビルド結果を棚卸しする。

```sh
grep -rlE '<script>|<script [^>]*>[^<]' public --include='*.html'          # inline script
grep -rhoE '<style|on(click|load|error|submit)=|<iframe|<form[^>]*' public | sort | uniq -c
grep -rhoE 'style=[^ >]{0,40}' public | sort | uniq -c | sort -rn | head    # minify で引用符が消える点に注意
grep -rhoE '(src|srcset|action)="?https?://[^/" >]+' public | sort | uniq -c   # 外部ホスト
curl -s https://<本番>/contact/ | grep -oE '<script[^>]*>'                  # Cloudflare が差し込む script
```

- inline script はすべて `assets/js/` に移す。表示前に必要なもの (ダークモード初期化など) は `defer` を付けず `<head>` で読む。
- コードハイライトとテーマは `style=` 属性を出すので `style-src 'unsafe-inline'` は必要。
- Cloudflare のメール難読化は `/cdn-cgi/` の同一オリジン script なので `'self'` で動く。Web Analytics や Rocket Loader を使っているサイトは、そのホストを `script-src` / `connect-src` に足す。
- 埋め込み (YouTube など) やフォームがあれば `frame-src` / `form-action` に追加する。
- HSTS は `includeSubDomains` / `preload` を付けない。全サブドメインの HTTPS を確認してから検討する。

雛形:

```
/*
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Strict-Transport-Security: max-age=31536000
```

### 5. GitHub の設定

www の次のファイルをコピーし、ブランチ名・`HUGO_VERSION`・テーマのリポジトリ名・CodeQL の言語を合わせる。

- [`.github/dependabot.yml`](../.github/dependabot.yml): `github-actions` のみ週次。`gitsubmodule` は submodule のブランチ HEAD を追うので入れない。
- [`.github/workflows/ci.yml`](../.github/workflows/ci.yml): Hugo を固定版で入れてビルド、`_headers` の存在、inline script の検出、Hugo とテーマの新版を warning。週次でも実行。
- [`.github/workflows/codeql.yml`](../.github/workflows/codeql.yml): `actions` と、repo にある言語 (`javascript-typescript` / `python` など)。`build-mode: none`。
- [`.github/workflows/dependency-review.yml`](../.github/workflows/dependency-review.yml): PR で実行。

Actions は commit SHA で固定する。最新の SHA:

```sh
for r in actions/checkout actions/dependency-review-action; do t=$(gh release view -R $r --json tagName --jq .tagName); echo "$r $t $(gh api repos/$r/commits/$t --jq .sha)"; done
gh api repos/github/codeql-action/tags --jq '[.[]|select(.name|test("^v4\\.[0-9]+\\.[0-9]+$"))][0]|[.name,.commit.sha]|@tsv'
```

脆弱性アラートを有効にする (204 を確認)。Secret scanning と push protection は public repo なら通常すでに有効。main の保護設定と Dependabot security updates は変えない。

```sh
gh api -X PUT repos/OWNER/REPO/vulnerability-alerts -i | head -1
gh api -X GET repos/OWNER/REPO/vulnerability-alerts -i | head -1
```

### 6. その他の点検

- `scripts/` のシェル・Python: 外部から取った値をファイル名やパスに使っていないか (`..`、`/` を弾く)。
- シークレット: `git grep -nIE '(AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{36}|github_pat_|sk-[A-Za-z0-9]{20,}|xox[bp]-|-----BEGIN [A-Z ]*PRIVATE KEY)'`
- `wrangler` を実行すると `.wrangler/` ができるので `.gitignore` に入れる。
- `markup.goldmark.renderer.unsafe = true` は、他人の書いた Markdown を載せないなら許容してよい。理由を記録する。

### 7. 反映と確認

push 後に、CI と Pages の完了まで待って確認する。

```sh
sha=$(git rev-parse HEAD); sleep 20
for id in $(gh run list --commit $sha --json databaseId --jq '.[].databaseId'); do gh run watch $id --exit-status >/dev/null 2>&1; done
gh run list --commit $sha --json name,conclusion --jq '.[]|[.name,.conclusion]|@tsv'
gh run view $(gh run list --workflow CI --commit $sha --json databaseId --jq '.[0].databaseId') --log | grep '##\[warning\]'
gh api repos/OWNER/REPO/commits/$sha/check-runs --jq '.check_runs[]|select(.name=="Cloudflare Pages")|.status+" "+(.conclusion//"")'
curl -sSI https://<本番>/ | grep -iE 'content-security|x-frame|strict-transport|permissions-policy'
curl -s  https://<本番>/ | grep -oE 'Hugo [0-9.]+'
gh api 'repos/OWNER/REPO/dependabot/alerts?state=open' --jq length
gh api 'repos/OWNER/REPO/code-scanning/alerts?state=open' --jq length
```

- Pages は `/foo.html` を `/foo` に 308 リダイレクトする。本番の記事ページを確かめるときは `curl -L` を付ける。
- CodeQL の初回は数分かかる。完了前の code-scanning API は 404 (`no analysis found`) を返す。

### 8. 記録

`docs/WORKLOG.md` (なければ作る) に、日付、Hugo とテーマの前後の版、該当した advisory、追加したヘッダー、GitHub の設定、検証結果、見送った事項とその理由を書く。サイト固有の点検手順は `docs/security-maintenance-playbook.md` に置く。

## つまずいた点

| 現象 | 原因 | 対処 |
|---|---|---|
| CI のテーマ版チェックがタグ名ではなく SHA を返す | `actions/checkout` の submodule は shallow でタグがない | 最新リリースのタグを API で SHA にして `rev-parse HEAD` と比べる |
| ビルド後の HTML に `style="` が見つからない | minify で属性の引用符が消える | `style=` で検索する |
| `pkill -f '<コマンド>'` の後の処理が実行されない | 自分のシェルのコマンドラインにも一致して終了した | 起動時の PID を控えて `kill` する |
| 本番の記事ページの中身が空 | Pages の `.html` → 拡張子なしへのリダイレクト | `curl -L` |
| `gh run list` が空 | push 直後はまだ登録されていない | 20 秒ほど待ってから取る |
| CF の環境変数を変えたのに古い Hugo のまま | 環境変数の変更では再ビルドされない | 変更後に push する |

## 権限確認を減らす進め方

- 調査、ビルドと検証、コミットと push、push 後の確認を、それぞれ1回の Bash にまとめる。
- ファイル作成は Write/Edit で一度に出し、その後にまとめてビルドする。
- 読み取り系コマンドの許可は `~/.claude/settings.json` の `permissions.allow` に入っている。
