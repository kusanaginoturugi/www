#!/usr/bin/env python3
"""
WordPress 由来の画像クレジット行 (Photo Dropper / Flickr / igosso) を本文から除去する。

- 本文中の `<span class="small">…</span>` (Photo Dropper credit) を削除
- 本文中の `<span style="font-size:10px;">…</span>` 系を削除
- Flickr / igosso 外部画像の <a><img></a> ラッパーを削除
- 壊れた `\<span ... \>` 形式 (Markdown 化失敗) も対応
- 連続空行は 2 行に圧縮

front matter には触らない (summary は別途 add-summary.py で再生成)。
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

POSTS_DIR = Path("content/posts")

PATTERNS = [
    # Photo Dropper credit
    re.compile(r'<span\s+class="small"[^>]*>.*?</span>', re.DOTALL),
    # font-size: 10px 系 (igosso / Flickr credit)
    re.compile(r'<span\s+[^>]*font-size:\s*10px[^>]*>.*?</span>', re.DOTALL),
    # alignright + 小さい span (Photo Dropper の派生形)
    re.compile(
        r'<span\s+[^>]*class="alignright[^"]*"[^>]*>.*?</span>', re.DOTALL
    ),
    # Flickr / igosso / photodropper の外部リンクラッパー (<a><img/></a>)
    re.compile(
        r'<a\s+[^>]*href="https?://(?:www\.)?flickr\.com[^"]*"[^>]*>\s*(?:<br\s*/?>\s*)?<img[^>]*>\s*(?:<br\s*/?>\s*)?</a>',
        re.DOTALL,
    ),
    re.compile(
        r'<a\s+[^>]*href="https?://(?:www\.)?igosso\.net[^"]*"[^>]*>\s*<img[^>]*>\s*</a>',
        re.DOTALL,
    ),
    re.compile(r'<a\s+[^>]*href="https?://(?:www\.)?photodropper\.com[^"]*"[^>]*>[^<]*</a>'),
    # 単独の Flickr 系外部画像
    re.compile(r'<img[^>]*farm\d+\.static(?:flickr)?\.com[^>]*/?>'),
    re.compile(r'<img[^>]*static\.flickr\.com[^>]*/?>'),
    # 壊れた wordpress_convert 型: `\<span ...\>` 開始 ... 続く Flickr 画像と </a>
    re.compile(
        r'\\<span[^>\n]*\\>\s*<a[^>]*flickr\.com[^>]*>.*?</a>',
        re.DOTALL,
    ),
]


def clean(text: str) -> str:
    for p in PATTERNS:
        text = p.sub("", text)
    # 残った <br /> や <br>
    text = re.sub(r"\s*<br\s*/?>\s*", "\n", text)
    # 連続空行を 2 行に圧縮
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 先頭の空行を除去 (front matter とのつなぎ目)
    text = re.sub(r"\A\n+", "\n", text)
    return text


def main() -> int:
    if not POSTS_DIR.is_dir():
        print(f"not found: {POSTS_DIR}", file=sys.stderr)
        return 1

    updated = 0
    for md in sorted(POSTS_DIR.glob("*.md")):
        if md.name == "_index.md":
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        parts = text.split("---\n", 2)
        if len(parts) < 3:
            continue
        _, fm, body = parts
        new_body = clean(body)
        if new_body != body:
            md.write_text(f"---\n{fm}---\n{new_body}", encoding="utf-8")
            updated += 1
            print(f"cleaned: {md.name}")

    print(f"\n完了: cleaned={updated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
