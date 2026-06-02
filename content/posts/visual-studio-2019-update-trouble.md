---
title: "Visual Studio 2019 にアップデートしたら2017で作ったWebアプリが動かなくなった"
date: 2019-08-21T15:52:16
slug: "visual-studio-2019-update-trouble"
categories: ["コンピューター"]
tags: []
---

うむ。では、2017を入れれば良いのだなと思って、ダウンロードしようとすると、サブスクリプションに登録されていないと言われた。うむ、登録していないのに、そんな事を言われても困る。

https://stackoverflow.com/questions/44061932/ms-build-2017-microsoft-webapplication-targets-is-missing

動かすためには2017版の、Web development build tools(Web開発ビルドツール) が必要らしい。

だが、これで入れただけでは動かない。パスが通っていないからだ。アホんだら畜生め。  
ということで、必要なファイルが入っていると思われるフォルダをそれらしいフォルダに入れたら起動した。

コピー元フォルダ

`C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\MSBuild\Microsoft\VisualStudio\v15.0`

コピー先フォルダ

`C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Microsoft\VisualStudio`

なんだかな。
