---
title: "もう一度Markdown"
date: 2020-04-02T18:11:53
slug: "retry_markdown"
categories: ["コンピューター"]
tags: []
summary: "以下のプラグインをインストール 1. Classic Editor 2. Markdown Editor theme/theme-name/functions.php"
---

以下の**プラグイン**をインストール

1.  Classic Editor
2.  Markdown Editor

theme/theme-name/functions.php

``` brush:
add_post_type_support( &#039;page&#039;, &#039;wpcom-markdown&#039; );
add_post_type_support( &#039;post&#039;, &#039;wpcom-markdown&#039; );
add_filter( &#039;markdown_editor_highlight&#039;, &#039;__return_false&#039; );
```
