#!/usr/bin/env python3
"""
content/posts/*.md の front matter に `summary:` を自動で追加する。

- 本文の先頭から HTML タグ・コードブロック・画像・Markdown 装飾を除去
- 改行・連続空白を 1 つにまとめ、先頭 MAX_CHARS 文字で打ち切り
- すでに `summary:` が書かれている記事はスキップ

使い方:
    python3 scripts/add-summary.py [--force] [--min N] [--max N] [--target N]

オプション:
    --force      既存の summary を上書き
    --min N      最小文字数 (デフォルト 80)
    --max N      最大文字数 (デフォルト 260)
    --target N   目安文字数 (デフォルト 180)。句点候補のうち target に近いものを採用。
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

POSTS_DIR = Path("content/posts")


def extract_text(body: str) -> str:
    # 行頭のコードブロック
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"~~~.*?~~~", "", body, flags=re.DOTALL)
    # HTML タグ
    body = re.sub(r"<[^>]+>", "", body)
    # Markdown 画像 / リンク
    body = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", body)
    body = re.sub(r"\[([^\]]*)\]\([^\)]*\)", r"\1", body)
    # 見出し記号、強調記号、リストマーカー、引用記号
    body = re.sub(r"^[#>\-\*\+]+\s*", "", body, flags=re.MULTILINE)
    body = re.sub(r"[*_`]+", "", body)
    # Markdown のバックスラッシュエスケープを解除 (例: \# → #, \| → |)
    body = re.sub(r"\\([!-/:-@\[-`{-~])", r"\1", body)
    # 連続する空白・改行を 1 スペースに
    body = re.sub(r"\s+", " ", body).strip()
    return body


SENTENCE_END = re.compile(r"[。．！？\.!?]")


def truncate_at_sentence(text: str, min_chars: int, max_chars: int, target: int) -> str:
    if len(text) <= max_chars:
        return text
    candidates = []
    for m in SENTENCE_END.finditer(text):
        pos = m.end()
        if pos < min_chars:
            continue
        if pos > max_chars:
            break
        candidates.append(pos)
    if candidates:
        best = min(candidates, key=lambda p: abs(p - target))
        return text[:best]
    return text[:max_chars].rstrip() + "…"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--min", type=int, default=80)
    ap.add_argument("--max", type=int, default=260)
    ap.add_argument("--target", type=int, default=180)
    args = ap.parse_args()

    if not POSTS_DIR.is_dir():
        print(f"not found: {POSTS_DIR}", file=sys.stderr)
        return 1

    updated = 0
    skipped = 0
    for md in sorted(POSTS_DIR.glob("*.md")):
        if md.name == "_index.md":
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            skipped += 1
            print(f"skip (no front matter): {md.name}")
            continue
        # ---\n の 2 回目で分割
        parts = text.split("---\n", 2)
        if len(parts) < 3:
            skipped += 1
            print(f"skip (malformed): {md.name}")
            continue
        _, fm, body = parts

        has_summary = re.search(r"^summary:", fm, re.MULTILINE) is not None
        if has_summary and not args.force:
            skipped += 1
            print(f"skip (has summary): {md.name}")
            continue

        plain = extract_text(body)
        if not plain:
            skipped += 1
            print(f"skip (empty body): {md.name}")
            continue
        summary = truncate_at_sentence(plain, args.min, args.max, args.target).rstrip()

        # YAML エスケープ (ダブルクォート文字列内)
        safe = summary.replace("\\", "\\\\").replace('"', '\\"')

        if has_summary:
            new_fm = re.sub(
                r"^summary:.*$", f'summary: "{safe}"', fm, count=1, flags=re.MULTILINE
            )
        else:
            new_fm = fm.rstrip("\n") + f'\nsummary: "{safe}"\n'

        md.write_text(f"---\n{new_fm}---\n{body}", encoding="utf-8")
        updated += 1
        preview = summary[:40] + ("…" if len(summary) > 40 else "")
        print(f"updated: {md.name}: {preview}")

    print(f"\n完了: updated={updated}, skipped={skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
