---
title: "月間予定表の編集・広報業務をGoogleAppsで解決"
date: 2012-09-12T00:13:08
slug: "monthly_schedule_in_googleapps"
categories: ["コンピューター"]
tags: ["Google","コンピューター","案件"]
---

<span class="alignright size-full wp-image-95" style="font-size: 10px;"><a href="http://www.flickr.com/photos/busbong/5345325898/" target="_blank"><img src="http://farm6.static.flickr.com/5165/5345325898_e3d3241bec_m.jpg" decoding="async" alt="カレンダーをの画像「カレンダーをめくりました。 / senov」" /></a>  
credit: [senov](http://www.flickr.com/photos/busbong/ "senov")  
</span>

会社の予定表をGoogleカレンダーに書いてあり、その内容を一覧表に出すという仕事があるそうです。Googleカレンダーに入っているなら、それを共有するだけでええやんと思うのだが、そうは問屋が卸さない。これを Excel で再作成して紙で渡さなければならないとの事。

予定が入りしだい Google カレンダーに入力していき、最終的にはそれを見ながら、手作業で Excel に入力しなおしていると言う。

システム屋はこういう手作業を許せない。頼むから自動化させてくれーとお願いしてでも自動化したいのがシステム屋というものです。 調べてみると、Google Apps Script を使えば簡単にできるっぽい。 よーし、さっそくやってみるかー。

さっそく、やってみました。Google Apps Script は わかりやすく言うと Google 版の VBA です。すんません、わかる人にしかわかりませんね。Google ドキュメントを直接さわれる Java Script のマクロ と言ったらわかりますかね。

ま、そんなこんなで、Google カレンダーの内容をプログラムからひっぱってきて、ちょいちょいと加工して、最終的に Google スプレッドシートに貼りつけるプログラムを書きました。内容が特殊なのでここでは公開できませんが、こういった事はやるための仕組みがちゃんと用意されているのは、大変すばらしい事だと思います。

同じような事をOutlookとExcel でやろうとすると、もっと手間がかかったり、VBに悪態をつきながらプログラミングする事になった事と思います。

もっとも紙での出力を前提とした Excel ファイル の作成などというプログラミングがこれから何度もあるようなら、それはそれでなんだかなぁというような気がします。

[Google Apps Script — Google Developers](https://developers.google.com/apps-script/ "Google Apps Script — Google Developers")

[初心者のためのGoogle Apps Scriptプログラミング入門](http://libro.tuyano.com/index2?id=638001 "初心者のためのGoogle Apps Scriptプログラミング入門")
