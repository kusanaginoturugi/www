---
title: "VirtualBoxとの絶えまない抗争の日々"
date: 2016-10-06T14:58:52
slug: "virtualboxwar"
categories: ["コンピューター"]
tags: []
summary: "pacmanだけで最新版を使うのは無理なのがVirtualbox。 バージョンアップの度に動かなくなるのがVirtualbox。 何度やってもどこかに落とし穴があるのがVirtualbox。 最近だと dkms (Dynamic Kernel Modules System)絡みで動かなくなったが、今のところ以下のパッケージのインストールで不満なく使えている。"
---

- pacmanだけで最新版を使うのは無理なのがVirtualbox。
- バージョンアップの度に動かなくなるのがVirtualbox。
- 何度やってもどこかに落とし穴があるのがVirtualbox。

最近だと dkms (Dynamic Kernel Modules System)絡みで動かなくなったが、今のところ以下のパッケージのインストールで不満なく使えている。  
dkmsだといろいろ厳しいということなのか、virtualbox-guest-modules-arch と virtualbox-host-modules-arch が追加されるようになった(いつから追加されたっけ？)。  
とりあえず普通のLinuxカーネルを使う場合は、dkmsは使わない方がよさげ。

``` brush:
community/virtualbox 5.1.6-1 [インストール済み]
community/virtualbox-host-modules-arch 5.1.6-1 [インストール済み]
community/virtualbox-guest-iso 5.1.6-1 [インストール済み]
# aurからも以下のパッケージをインストールする
aur/virtualbox-ext-oracle 5.1.6-1
aur/virtualbox-guest-iso
```

## 過去のトラブル例

- Oracleから提供されている VirtualBox Oracle VM VirtualBox Extension Pack を直接インストールするといろいろと問題が
- 仮想マシンのディスク容量が一杯になってしまった(vboxmanageコマンドを使ってちっさくしよう)
- iPhoneを繋いだときに、USBデバイスフィルターにiPhoneを追加しなきゃいけないこと
- iPhoneをUSBデバイスフィルターに繋ぐときに、素のiPhoneとリカバリーモード時のiPhoneでは別なこと
- 準仮想化インターフェイスはHyper-Vでも良い(1割ほど早いらしい)が、ディスク容量変更時は「なし」にしないとダメ
  - 2018/9/19時点では、ディスク容量変更可能になっていました。
- オーディオ設定で、ホストオーディオドライバーをPulseAudioにして、オーディオコントローラーをIntel HDオーディオにしないと動かないとか(というかいつのまにか設定が変わって音がでなくなるのヤメてくれ)
- virtualbox-host-modules-arch と virtualbox-guest-modules-arch を同時に使った場合にどちらを先に入れるかで1/2の確立でトラブルになる(まあ、そりゃそうだわな)。  
  両方入れるとどちらかのモジュールが設定されないのでエラーがでる。うっかりと両方入れてしまって、エラーメッセージを解消するのに焦った。
- Virtualbox のバージョンアップ時には、virtualbox-ext-oracle のアップデートと、Windowsログイン後に virtualbox-guest-iso の更新を行うこと

WindowsOSは仮想環境で動かすのがいろいろと便利なのだが、その基盤たるVirtualboxを安定して使いつづけることがなかなかに厳しい。

追記  
WSLもかなり使えるようになっているし、WSLでArchLinuxも動くけど、まだシェル上から音を出したりできないので、まだまだVirtualBoxの優位は動かないですね。ArchLinuxを絶対に使いたいという前提ですが。
