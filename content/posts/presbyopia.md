---
title: "はなせばわかる世代のためのPC環境"
date: 2020-01-28T17:45:00
slug: "presbyopia"
categories: ["コンピューター"]
tags: []
summary: "気付けばもう50代。PCモニターの解像度がどんどん上っていった頃は若くて、解像度なんかなんぼでも上ってええんやでと思っていたのは、もはや過去の話。 ついに、「ノートPCの解像度にフルHDなんぞいらん」と言う始末。 おまけに、コントラストの強い画面構成がつらい。コンソールの黒背景に白文字がかすんで良く見えないなんてことも。 嘆いていてもしかたがないので、老眼者のためのPC環境を設定する。"
---

気付けばもう50代。PCモニターの解像度がどんどん上っていった頃は若くて、解像度なんかなんぼでも上ってええんやでと思っていたのは、もはや過去の話。  
ついに、「ノートPCの解像度にフルHDなんぞいらん」と言う始末。  
おまけに、コントラストの強い画面構成がつらい。コンソールの黒背景に白文字がかすんで良く見えないなんてことも。  
嘆いていてもしかたがないので、老眼者のためのPC環境を設定する。  

- Solarized Light テーマを設定する。ダークモードは年寄には無理
- アプリ毎の設定でアイコンのスタイルが変更できるので、Solarized Light で見易いアイコンに変更する
- 文字サイズのデフォルトはやや大きめに設定し、厳しい場合は、すぐにキーボードかマウスで拡大できるように設定する
- アイコンテーマも見易いものにする
- 部屋の明るさを調整する。窓際を避けるか、カーテン、ブラインドを有効利用する
- 疲れ目、ドライアイにならないよう、ディスプレイを見る時間をできるだけ減らす
- 自分に必要な睡眠時間を確保する

~/.xinitrc

``` brush:
export GTK_THEME=NumixSolarizedLightBlue
export GTK2_RC_FILES=/usr/share/themes/${GTK_THEME}/gtk-2.0/gtkrc
export QT_QPA_PLATFORMTHEME='gtk2'
```

~/.Xresources

``` brush:
! Perl extensions                                                                   
URxvt.perl-ext-common:      default,clipboard,url-select,keyboard-select,selection-to-clipboard,resize-font,xim-onthespot,matcher,tabbedex,solarized
URxvt.url-select.launcher:  firefox
URxvt.url-select.underline: true
! url-select                                                                        
URxvt.keysym.M-u:       perl:url-select:select_next
! keyboard-select                                                                   
URxvt.keysym.M-Escape:  perl:keyboard-select:activate
URxvt.keysym.M-e:       perl:keyboard-select:activate
URxvt.keysym.M-s:       perl:keyboard-select:search
! resize                                                                            
URxvt.keysym.C-minus:     resize-font:smaller
URxvt.keysym.C-plus:      resize-font:bigger
URxvt.keysym.C-equal:     resize-font:reset
URxvt.keysym.C-question:  resize-font:show
URxvt.resize-font.step:   2
```

アイコンテーマ /usr/share/icons/default/index.theme

``` brush:
Inherits=papirus
```

あ、そもそもこのサイトも文字がちっさすぎやな。
