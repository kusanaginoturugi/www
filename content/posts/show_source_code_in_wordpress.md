---
title: "WordPressでソースコードを表示"
date: 2013-01-20T07:41:46
slug: "show_source_code_in_wordpress"
categories: ["コンピューター"]
tags: ["WordPress"]
summary: "ワードプレスでソースコードを表示させるには、「SyntaxHighlighter Evolved」を使うと便利です。(注 本来は大括弧の前後のスペースは削除しないと動作しません) 対応している言語もいろいろある。 試しに先程のテキストを実際に表示させるとこうなる。 SQLの場合"
---

ワードプレスでソースコードを表示させるには、「<a href="http://wordpress.org/extend/plugins/syntaxhighlighter/" target="_blank" rel="noopener noreferrer">SyntaxHighlighter Evolved</a>」を使うと便利です。(注 本来は大括弧の前後のスペースは削除しないと動作しません)

``` brush:
[ text ]
対応言語
html,actionscript3,bash,coldfusion,cpp,csharp,css,delphi,
erlang,fsharp,diff,groovy,javascript,java,javafx,
matlab (keywords only),objc,perl,php,text,powershell,
python,r,ruby,scala,sql,vb,xml
[ /text ]
```

<a href="http://en.support.wordpress.com/code/posting-source-code/" target="_blank" rel="noopener noreferrer">対応している言語</a>もいろいろある。

試しに先程のテキストを実際に表示させるとこうなる。

``` brush:
対応言語
html,actionscript3,bash,coldfusion,cpp,csharp,css,delphi,
erlang,fsharp,diff,groovy,javascript,java,javafx,
matlab (keywords only),objc,perl,php,text,powershell,
python,r,ruby,scala,sql,vb,xml
```

SQLの場合

``` brush:
select * from table1 where id = 1;
```
