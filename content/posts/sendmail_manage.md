---
title: "メール送信管理アプリを作成しました"
date: 2015-08-26T18:58:58
slug: "sendmail_manage"
categories: ["コンピューター"]
tags: ["コンピューター","サーバー"]
summary: "メールからの情報漏洩が騒がれる今日このごろですが、ちょうどそれに対応するアプリを作成しました。 Windowsのアプリケーションで、メール送信すると、送信内容をチェックして、設定済みのルールに合致するメールの場合は、ポップアップ表示を出して注意を喚起したり、送信メールを管理用サーバーに送信して、履歴を残すといった処理を行います。"
---

メールからの情報漏洩が騒がれる今日このごろですが、ちょうどそれに対応するアプリを作成しました。

Windowsのアプリケーションで、メール送信すると、送信内容をチェックして、設定済みのルールに合致するメールの場合は、ポップアップ表示を出して注意を喚起したり、送信メールを管理用サーバーに送信して、履歴を残すといった処理を行います。

メールの受信には Willpe/SMTP を使用

<a href="https://github.com/willpe/SMTP" target="_blank">https://github.com/willpe/SMTP</a>

受け取ったメールのパースには MimeKit を使用

<a href="https://github.com/jstedfast/MimeKit" target="_blank">https://github.com/jstedfast/MimeKit</a>

メールの送信には MailKit を使用

<a href="https://github.com/jstedfast/MailKit" target="_blank">https://github.com/jstedfast/MailKit</a>

これらのライブラリを使うことで、メール固有のノウハウにはあまり触れることなく実装することができました。

デバッグ中に MimeKit の不具合を発見して、プログラムを一部修正して、githubにフォークしたプロジェクトを変更したところ、オリジナルの作者の jstedfast 氏が日本語の適当なコメントにもかかわらず反応してまして、おわっ、これはマズいと再度適切な文章を同僚に作成してもらってコメントを追加して、ようやく作者さんにも問題を理解してもらい、最終的にはオリジナルのプロジェクトの方も修正してもらえたのは、貴重な体験でした。

<a href="https://github.com/kusanaginoturugi/MimeKit/commit/3f1d0c9c83a2fb46d51d82446afd4869a069839a#commitcomment-12613986" target="_blank">https://github.com/kusanaginoturugi/MimeKit/commit/3f1d0c9c83a2fb46d51d82446afd4869a069839a#commitcomment-12613986</a>

オープンソースプロジェクトはこうして使われていく事で磨かれていくのだなと実感しました。

今回は Windows のクライアントアプリだけではなく、サーバーサイドのプログラムも実装しました。サーバーサイドはRailsで作りました。

このあたりにも技術的に面白い話はたくさんあるのですが、長くなるので割愛します。

次もこんな開発をやりたいものです。
