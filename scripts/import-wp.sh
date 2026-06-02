#!/usr/bin/env sh
# WordPress (www.showway.biz) の記事を WP REST API 経由で取得し、
# Hugo 用の Markdown (content/posts/<slug>.md) に変換する。
#
# 必要コマンド: curl, jq, pandoc
#
# 使い方:
#   ./scripts/import-wp.sh

set -eu

WP_BASE="${WP_BASE:-https://www.showway.biz/wp-json/wp/v2}"
OUT_DIR="${OUT_DIR:-content/posts}"

command -v curl   >/dev/null || { echo "curl が必要"   >&2; exit 1; }
command -v jq     >/dev/null || { echo "jq が必要"     >&2; exit 1; }
command -v pandoc >/dev/null || { echo "pandoc が必要" >&2; exit 1; }

mkdir -p "$OUT_DIR"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

posts="$tmp/posts.json"
cats="$tmp/cats.json"
tags="$tmp/tags.json"

echo "[1/3] 記事一覧取得"
curl -fsSL "${WP_BASE}/posts?per_page=100" -o "$posts"

echo "[2/3] カテゴリ・タグ取得"
curl -fsSL "${WP_BASE}/categories?per_page=100" -o "$cats"
curl -fsSL "${WP_BASE}/tags?per_page=100"       -o "$tags"

cat_map=$(jq '[.[] | {key: (.id|tostring), value: .name}] | from_entries' "$cats")
tag_map=$(jq '[.[] | {key: (.id|tostring), value: .name}] | from_entries' "$tags")

count=$(jq 'length' "$posts")
echo "[3/3] $count 件を変換"

i=0
while [ "$i" -lt "$count" ]; do
  slug=$(jq -r ".[$i].slug" "$posts")
  title=$(jq -r ".[$i].title.rendered" "$posts")
  date=$(jq -r ".[$i].date" "$posts")
  html=$(jq -r ".[$i].content.rendered" "$posts")

  cat_names=$(jq -c --argjson m "$cat_map" ".[$i].categories | map(\$m[tostring]) | map(select(. != null))" "$posts")
  tag_names=$(jq -c --argjson m "$tag_map" ".[$i].tags       | map(\$m[tostring]) | map(select(. != null))" "$posts")

  # front matter (YAML フロー形式 = JSON 互換)
  front_matter=$(jq -nr \
    --arg title "$title" \
    --arg date  "$date" \
    --arg slug  "$slug" \
    --argjson categories "$cat_names" \
    --argjson tags       "$tag_names" \
    '"title: "      + ($title|@json) + "\n" +
     "date: "       + $date          + "\n" +
     "slug: "       + ($slug|@json)  + "\n" +
     "categories: " + ($categories|tostring) + "\n" +
     "tags: "       + ($tags|tostring)')

  body=$(printf '%s' "$html" | pandoc -f html -t gfm --wrap=none)

  out="${OUT_DIR}/${slug}.md"
  {
    echo "---"
    printf '%s\n' "$front_matter"
    echo "---"
    echo
    printf '%s\n' "$body"
  } > "$out"

  echo "  - ${slug}"
  i=$((i + 1))
done

echo "完了: $OUT_DIR/ に $count 件出力"
