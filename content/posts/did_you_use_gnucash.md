---
title: "Gnucash使ってますか？"
date: 2015-03-08T20:33:13
slug: "did_you_use_gnucash"
categories: ["コンピューター"]
tags: ["コンピューター"]
---

Gnucashとはフリーの財務ソフトウェアです。  
<a href="http://www.gnucash.org/index.phtml?lang=ja_JP" target="_blank" rel="noopener noreferrer">http://www.gnucash.org/index.phtml?lang=ja_JP</a>

確定申告の時期になると(というかその時期だけ)とても利用頻度の高まるアプリケーションです。  
私も使いはじめて今年で三年目となります。

さすがに三年目ともなると、使い方にも慣れてはくるのですが、  
どうしても許せない点があります。

それは日付入力時にキーボードのプラス(+)を押すと日付が一週間後になるという点です。テンキーでの動作は問題ないのですが、Shiftキーと併用して入力するプラスの場合だけ動作がおかしいのです。  
確定申告の締切直前にこんなことを調べてしまう私もバカだと思いますが、ソースを調べてみましたよ。  
たしかにこれだとJISキーボードの場合に+を押すと一週間後になってしまいますね。さらに=の場合も一週間後なので、JISキーボードの場合は一日後を押せるキーがないというオチ。JIS配列が腐ってるのも確かだけど、このコードの書き方はないわ。英語キーボード使ってないやつなんているの？って事じゃないか。

ソースに注意書きは書いてはあるものの直っていない様子だし。  
とりあえず7日後は必要ないので、7を1に変えてビルドしなおして今日のところは気持ち良く作業を進めたいと思います。(実はこの場所を探すのにえらく手間取りました)

src/gnome-utils/dialog-utils.c

``` brush:
/*
* Check those keys where the code does different things depending
* upon the modifiers.
*/
switch (event->keyval)
{
case GDK_KP_Add:
case GDK_plus:
case GDK_equal:
if (event->state & GDK_SHIFT_MASK)
g_date_add_days (&gdate, 7);
else if (event->state & GDK_MOD1_MASK)
g_date_add_months (&gdate, 1);
else if (event->state & GDK_CONTROL_MASK)
g_date_add_years (&gdate, 1);
else
g_date_add_days (&gdate, 1);
g_date_to_struct_tm (&gdate, tm);
return TRUE;
```

<http://gnucash.sourcearchive.com/documentation/1:2.4.2-1ubuntu1/dialog-utils_8c_source.html>
