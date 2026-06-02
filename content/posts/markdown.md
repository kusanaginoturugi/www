---
title: "WordPressでMarkdownを使ってみた"
date: 2015-11-20T11:53:48
slug: "markdown"
categories: ["コンピューター"]
tags: ["WordPress","コンピューター","プラグイン"]
---

以下のような記述をすると

``` brush:
#### Markdownテスト
- Jetpackに付属しているmarkdown機能を使ってみるテスト
- セットアップはJetpackで有効にするだけ
- 投稿の設定にmarkdownの設定とかは見つからなかった
- コメントの設定にはmarkdownの設定があった。
- さて、**プレビュー**してみるか。

[Markdown](https://ja.wikipedia.org/wiki/Markdown)

段落がいまいちよくわからない。空行で段落分けになるはずだけどならないし。

引用はこんな感じか。

> " Markdownは、文書を記述するための軽量マークアップ言語のひとつである。もとはプレーンテキスト形式で手軽に書いた文書からHTMLを生成するために開発された。現在ではHTMLのほかパワーポイント形式やLaTeX形式のファイルへ変換するソフトウェア（コンバータ）も開発されている。各コンバータの開発者によって多様な拡張が施されるため、各種の方言が存在する。)"
```

以下のような出力になりますよ。

#### Markdownテスト

- Jetpackに付属しているmarkdown機能を使ってみるテスト
- セットアップはJetpackで有効にするだけ
- 投稿の設定にmarkdownの設定とかは見つからなかった
- コメントの設定にはmarkdownの設定があった。
- さて、**プレビュー**してみるか。

[Markdown](https://ja.wikipedia.org/wiki/Markdown)

段落がいまいちよくわからない。空行で段落分けになるはずだけどならないし。

引用はこんな感じか。

> ” Markdownは、文書を記述するための軽量マークアップ言語のひとつである。もとはプレーンテキスト形式で手軽に書いた文書からHTMLを生成するために開発された。現在ではHTMLのほかパワーポイント形式やLaTeX形式のファイルへ変換するソフトウェア（コンバータ）も開発されている。各コンバータの開発者によって多様な拡張が施されるため、各種の方言が存在する。”

#### 追記(2016/9/16)

- functions.phpに以下のコードを追加しないと段落が生成されない。(テーマが更新されてない？)

  ``` brush:
      remove_filter('the_content','wpautop');
      add_filter('the_content','wpautop_nobr');

      function wpautop_nobr($txt) {
      return wpautop($txt, false);
      }
      
  ```

#### 追記(2019/3/22)

markdownで入力しても、保存するとHTMLに変換されるクソ仕様なので、こんなゴミは使ってられない。markdownはmarkdownで保存されなければならない。

#### さらに追記

- htmlで書いた記事にmarkdownで追記すると、markdownの部分はhtmlに書き換えられるようだ。
- すべてを markdown で書いた場合は、htmlに書き換えられることはないようだ。
- 必要なら、html を markdown に書き換えろってことか。

#### WP Editor.md

- こちらのマークダウンエディタを使う方がよさそう。これはMarkdownを勝手に変換したりはしない。

#### 2020年の追記

- classic editor と markdown editor に代えて、Jetpackを無効にして、ようやく期待通り(markdownで書いて、markdownで編集。htmlに変換しない)に動作した。サイドバイサイドで表示の確認もできるようになった。
