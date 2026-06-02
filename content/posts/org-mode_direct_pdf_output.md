---
title: "org-modeから直接PDFを出力してみる"
date: 2019-09-11T15:55:17
slug: "org-mode_direct_pdf_output"
categories: ["コンピューター"]
tags: []
summary: "org-modeを使って、PDFファイルを出力するのは、いったんODTファイルに出力した後、LibreOfficeを立ち上げてから、PDFに出力するのが一般的だろうと思う。 しかし、本来はODTファイルを経由しなくともLaTex経由で直接PDFファイルを生成できるはずである。 実は何度か試してはいたけれど、エラーがでるので放置していたのだ。"
---

org-modeを使って、PDFファイルを出力するのは、いったんODTファイルに出力した後、LibreOfficeを立ち上げてから、PDFに出力するのが一般的だろうと思う。

しかし、本来はODTファイルを経由しなくともLaTex経由で直接PDFファイルを生成できるはずである。

実は何度か試してはいたけれど、エラーがでるので放置していたのだ。

今日になってやっと一応出力できたので、まとめておく。

まず、以下のパッケージをインストールする。エラーが出たら、`*Messages*`バッファをチェックしてエラーを潰していこう。

    pacman -S texlive-bin texlive-core texlive-latexextra texlive-fontsextra otf-ipamjfont otf-ipaexfont

いろいろ試したので、不要なパッケージもあるかもしれない。  
さらに手作業でできあがったtexファイルの冒頭の部分を以下のように変更する。

変更前

    \documentclass[11pt]{article}

変更後

    \documentclass[pdflatex,ja=standard]{bxjsarticle}

そして、

    pdflatex hoge.tex

うん、ODTファイルでいいや。

<https://texwiki.texjp.org/?LaTeX-CJK>

#### 追記

<https://texwiki.texjp.org/?Emacs%2FOrg%20mode> なにげにググってみると、たまたまビンゴの情報にヒットしたので、設定ファイルを追加してもう一度やってみた。設定例のLinuxの項目を `init.el` に追加して、PDFを作成してみた。

    (setq org-latex-pdf-process '("latexmk -e '$latex=q/uplatex %S/' -e '$bibtex=q/upbibtex %B/' -e '$biber=q/biber --bblencoding=utf8 -u -U --output_safechars %B/' -e '$makeindex=q/upmendex -o %D %S/' -e '$dvipdf=q/dvipdfmx -o %D %S/' -norc -gg -pdfdvi %f"))

の行で `%S` がどうとかエラーがでるので、この部分はコメントアウトして、もう一度作成。

成功。

LaTex出力らしい、かっちょいい出力ができました。
