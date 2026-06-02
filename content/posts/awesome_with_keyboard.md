---
title: "Awesomeをマウスなしで操作する"
date: 2019-03-22T16:08:10
slug: "awesome_with_keyboard"
categories: ["コンピューター"]
tags: []
summary: "何がいやって、キーボードでアクティブウィンドウを変更しても、マウスカーソルがアクティブウィンドウの上にないと文字入力ができないのである。 なぜかいつのなにかマウス操作主体になってしまう原因がここにある。 なので、マニュアルを引きつつ、rc.lua に以下のコードを追加する。 とりあえず今日のところはここまで。"
---

何がいやって、キーボードでアクティブウィンドウを変更しても、マウスカーソルがアクティブウィンドウの上にないと文字入力ができないのである。

なぜかいつのなにかマウス操作主体になってしまう原因がここにある。

なので、マニュアルを引きつつ、rc.lua に以下のコードを追加する。

``` brush:
awful.key({ modkey,           }, "j",
function ()
awful.client.focus.byidx( 1)
c = client.focus
mouse.coords {
x = c.x + c.width / 2,
y = c.y + c.height / 2
}
end,
{description = "focus next by index", group = "client"}
),
awful.key({ modkey,           }, "k",
function ()
awful.client.focus.byidx(-1)
c = client.focus
mouse.coords {
x = c.x + c.width / 2,
y = c.y + c.height / 2
}
end,
{description = "focus previous by index", group = "client"}
),
```

とりあえず今日のところはここまで。
