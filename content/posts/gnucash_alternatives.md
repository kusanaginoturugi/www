---
title: "Gnucashを使いつづけてよいものか？"
date: 2017-09-06T16:43:41
slug: "gnucash_alternatives"
categories: ["コンピューター"]
tags: []
---

今年こそGnucashから別のアプリに切り替えようかと思って調べてみた。

[AlternativesTo](http://alternativeto.net/software/gnucash/)

上記のような便利なサイトがあったのでここからいくつかを試してみた。

- HomeBank

パッケージマネージャーからインストール可能。  
QIFファイルからインポート可能。

    sudo pacman -S homebank

- Money Manager Ex

パッケージマネージャーからインストール可能。  
QIFファイルからインポート可能。

    sudo pacman -S moneymanagerex

バグっぽい。日本語化が中途半端。  
日本語表示のためには以下の手順が必要(ln -sの方が良いかもだけど未検証)

    sudo cd /usr/share/mmex/po
    sudo mkdir en
    sudo cp english.mo en/
    sudo cp japanese.mo en/

- KMyMoney

パッケージマネージャーからインストール可能

    pacman -S kmymoney

##### 総括

振替伝票形式でないとイメージがつかめないことがわかった。  
2017年もGnucashを使いつづけることになりそうだ。
