---
title: "Vagrant(ベイグラント)は便利です"
date: 2015-11-19T15:56:52
slug: "vagrant"
categories: ["コンピューター"]
tags: ["コンピューター","仮想マシン"]
summary: "vagrantがいかに便利かを説明します。開発者にはとても便利なツールです。 Vagrantを使って仮想マシンを作るのってこれだけですよ。これだけ。 次にまた起動したいときもこれだけ。 lxcを使うときもこんだけ (lxcを使えるようにするまでは、もう一手間必要ですが。"
---

vagrantがいかに便利かを説明します。開発者にはとても便利なツールです。

Vagrantを使って仮想マシンを作るのってこれだけですよ。これだけ。

``` brush:
$ sudo pacman -S virtualbox       #virtualboxパッケージのインストール
$ sudo pacman -S vagrant          #vagrantパッケージのインストール
$ vagrant plugin install vagrant-vbguest vagrant-share #プラグインのインストール
$ mkdir -p ~/dev/vagrant/jessie64 #作業フォルダ作成
$ cd ~/dev/vagrant/jessie64       #作業フォルダに移動
$ vagrant box add debian/jessie64 #仮想イメージのダウンロード
$ vagrant init debian/jessie64    #仮想環境の初期化
$ vagrant up                      #仮想環境の起動
$ vagran ssh                      #仮想環境へのログイン
```

次にまた起動したいときもこれだけ。

``` brush:
$ cd ~/dev/vagrant/jessie64       #作業フォルダに移動
$ vagrant up                      #仮想環境の起動
$ vagran ssh                      #仮想環境へのログイン
```

lxcを使うときもこんだけ

``` brush:
$ pacman -S lxc arch-install-scripts #パッケージのインストール
$ vagrant plugin install vagrant-lxc #プラグインのインストール
$ mkdir ~/dev/vagrant/jessie64lxc    #作業フォルダ作成
$ cd ~/dev/vagrant/jessie64lxc       #作業フォルダに移動
$ vagrant init glenux/jessie64-lxc   #仮想環境の初期化
$ vagrant up                         #仮想環境の起動
$ vagran ssh                         #仮想環境へのログイン
```

(lxcを使えるようにするまでは、もう一手間必要ですが。それでも素のlxcを使うよりは断然楽です)

<a href="https://wiki.archlinuxjp.org/index.phphttps://atlas.hashicorp.com/boxes/search?utm_source=vagrantcloud.com&amp;vagrantcloud=1/Vagrant#.E3.83.97.E3.83.AD.E3.83.93.E3.82.B8.E3.83.A7.E3.83.8B.E3.83.B3.E3.82.B0" target="_blank">Vagrent – Archlinux</a>

「debian/jessie64」「glenux/jessie64-lxc」とかは、「Base Box」といって、以下のサイトのリストからよさそうなものを選びます。

<a href="https://atlas.hashicorp.com/boxes/search?utm_source=vagrantcloud.com&amp;vagrantcloud=1" target="_blank">Vagrant Cloud</a>

ちょろっと見てみましたが、  
「dpsxp/windows-ie10」とか「dpsxp/windows-ie9」とかもあるのですね。ボリュームライセンスがあれば、テストがはかどりそうですね。

追記

作った仮想環境の削除方法

``` brush:
$ cd ~/dev/vagrant/jessie64lxc #作業フォルダに移動
$ vagrant destroy              #仮想環境の停止と削除
```

インストールすると、Base Box が保存されるので、そのファイルは上記コマンドでは削除されないので、手作業で削除します。場所は「~/.vagrant.d/boxes」です。これを知らずに、知らぬまにハードディスクの残り容量が0になってことがありました。
