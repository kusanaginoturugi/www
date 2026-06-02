---
title: "Rails4を使ったシステムの構築"
date: 2013-08-31T00:30:30
slug: "rails4_solutions"
categories: ["コンピューター"]
tags: ["paypal","コンピューター","案件"]
summary: "歯科医院用の診療記録のシステムを作成しました。 開発環境など プログラミング言語 Ruby v.2.0 フレームワーク Ruby On Rails v.4.0.0 CSSフレームワーク Twitter BootStrap v.2.3.2 主に使用したエディタ Sublime Text 2 PDF出力に使用したツール wkhtmltopdf v.0.9.9."
---

歯科医院用の診療記録のシステムを作成しました。

**開発環境など**

- <span style="line-height: 13px;">プログラミング言語 Ruby v.2.0</span>
- <span style="line-height: 13px;">フレームワーク Ruby On Rails v.4.0.0</span>
- CSSフレームワーク Twitter BootStrap v.2.3.2
- 主に使用したエディタ Sublime Text 2
- PDF出力に使用したツール <span class="GINGER_SOFATWARE_noSuggestion GINGER_SOFATWARE_correct">wkhtmltopdf</span> v.0.9.9.1

**主な内容**

- 患者情報の入力・表示・保存
- <span style="line-height: 13px;">BPI値、Pd値の入力・保存</span>
- BPI値、Pd値の平均値の表示
- BPI値のカラー表示・印刷
- BPI値の履歴表示・印刷

**総括**

- PaaSとしてHerokuを使用。Herokuはとても簡単にデプロイできるので好きだ。
- ソースコードの記述は簡潔に書けた。Rails4になり、さらに簡潔に書けるようになり、ソースコードが設計書(仕様書)に近くなった。
- テストコードをほとんど書かなかった(ロジック部が薄いので)。やはり最初から意識してテストコードを書かないと、途中からは書けない。
- 今回もCSSまわりで躓いた。やはりきっちり勉強しておかなければ。
- HAML、Slimに関しては微妙。大量のページを作るのなら便利かもれないが、この規模ならまだ導入するのは躊躇する。次にやるときは最初から使うならありかも。[SlimかHamlか、Rails Rumbleで使われたGem](http://silentpower2.blogspot.jp/2012/10/slimhamlrails-rumblegem.html "SlimかHamlか、Rails Rumbleで使われたGem")
- PDF出力のwkhtmltopdfのバグでテーブルの途中で改行が入る問題が残ってしまった。(現在対応中なので、すぐに修正されるはず)
- RDOCの出力はYARDを使った。
- rails4が出たばかりで情報がないので最初は苦労した。しかし、それでも新しいものを使う方が効率が良いことがわかった。
- ユーザーのパスワード変更のためにgmailの二段階認証を使えたのはよかった。
- 今のところ1ユーザー専用になっているが、将来的にはSaaS展開を目標としているので、その場合の設計はこれから検討する。
- Saasの決済用にPayPalを検討中。PayPalは、PayPalアカウントを持っていないと使えないので、クレジット決済の方法も調査する。
