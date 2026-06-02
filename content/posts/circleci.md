---
title: "CircleCIを試してみた"
date: 2019-02-28T18:52:37
slug: "circleci"
categories: ["コンピューター"]
tags: []
---

いったいどれくらい周回遅れの話題かわからないけど、[CircleCI](https://circleci.com/%20) を試してみた。

お題はこちらの工数入力Webアプリ。

https://github.com/kusanaginoturugi/man-hour

しょぼいアプリなんだけど、工数の入力ができて、毎月報告書をPDFで出力できて、工数の残高を自動計算してくれる自分だけが幸せになるRailsアプリである。

そもそもgithubをリポジトリにしているので、CircleCIに登録するだけでサクっと使えるようになる。

肝となるのは、.circleci/config.yml というYAML形式の設定ファイルの書き方。YAML形式に慣れていないとかなり辛い。慣れていても辛い。

ちゃんと設定できれば、git push origin master する度に、テストが通ることを確認してくれて、テストが通ると、deployまでやってくれるので、最初の設定は大変でも、以降はコードの実装に集中できるので良いと思う。うんうん。

githubに登録して、herokuで公開しているアプリにはうってつけであった。

あれ、gitlabのアプリはどうしよう。
