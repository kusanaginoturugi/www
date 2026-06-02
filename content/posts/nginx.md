---
title: "ウェブサーバをNginxに変えてみた"
date: 2015-12-23T16:00:51
slug: "nginx"
categories: ["コンピューター"]
tags: []
---

## Nginxのインストールおよび設定

- ArchLinuxのWikiは新しく正しい情報が多いので、まずはそちらを参照する。
- [nginx – ArchWiki](https://wiki.archlinuxjp.org/index.php/Nginx)
- phpinfo()が動作することを確認

## dokuwiki

- まずはデータベースを使わないウェブアプリで試す
- [dokuwiki – ArchWiki](https://wiki.archlinuxjp.org/index.php/Dokuwiki)
- nginx での設定方法が載っているので、こちらもさくっと動作確認

## wordpress

- WordPress Codex 内の Nginx 情報がよさげだったのでそれを参照。
- [nginx – WordPress Codex 日本語版](https://wpdocs.osdn.jp/Nginx#.E3.83.A1.E3.82.A4.E3.83.B3.E3.82.B9.E3.82.BF.E3.83.BC.E3.83.88.E3.82.A2.E3.83.83.E3.83.97.E3.83.95.E3.82.A1.E3.82.A4.E3.83.AB)
- でものっけから、「nginxを検討する前に、PHP APCや、WordPressのキャッシュプラグインが、単純にApacheをnginxに変更するよりも大きなパフォーマンス向上をもたらしてくれるかもしれないことに留意しましょう。」とか書いてあり複雑な心境。
- ほぼ上記設定ファイルがそのまま使えたのですが、php-fpm.sock の場所が違っていたので変更してあります。
- でも、WordPressの記事の更新したりした感触では、さして早くなっていない印象。
- ちゃんと外部からアクセスしたら軽く感じられたので一応満足。ストレステストをかけてみる予定

## できあがった設定ファイル

``` brush:
worker_processes  auto;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;

    keepalive_timeout  65;

    client_max_body_size 13m;
    index              index.php index.html index.htm;

    fastcgi_intercept_errors        on;
    fastcgi_ignore_client_abort     off;
    fastcgi_connect_timeout 60;
    fastcgi_send_timeout 180;
    fastcgi_read_timeout 180;
    fastcgi_buffer_size 128k;
    fastcgi_buffers 4 256k;
    fastcgi_busy_buffers_size 256k;
    fastcgi_temp_file_write_size 256k;
    
    # Upstream to abstract backend connection(s) for PHP.
    upstream php {
    server unix:/run/php-fpm/php-fpm.sock;
    }
    include sites-enabled/*;
}
```

``` brush:
server {
    server_name www.showway.biz;
    root /srv/http/showway;

    if ($http_host != "www.showway.biz") {
        rewrite ^ http://www.showway.biz$request_uri permanent;
        }

    include global/restrictions.conf;
    include global/wordpress.conf;

    access_log /var/log/nginx/showway_access.log main;
    error_log  /var/log/nginx/showway_error.log;
}
```

``` brush:
server {
        listen 80;
    server_name wiki.showway.biz;
    root /srv/http/dokuwiki;
    location / {
        index index.php index.html index.htm;
    }
    location ~^/(data|conf|bin|inc)/ { deny all; }
    location ~^/\.ht { deny all; }
    location ~^/lib/^((?!php).)*$ { expires 30d; }
    location ~ \.php$ {
        fastcgi_pass  unix:/run/php-fpm/php-fpm.sock;
        fastcgi_index index.php;
        include fastcgi.conf;
    }
    access_log /var/log/nginx/wiki_access.log main;
    error_log /var/log/nginx/wiki_error.log;
}
```

``` brush:
location = /favicon.ico {
     log_not_found off;
     access_log off;
}

location = /robots.txt {
     allow all;
     log_not_found off;
     access_log off;
}

location ~ /\. {
     deny all;
     access_log off;
     log_not_found off;
}
```

``` brush:
location / {
    try_files $uri $uri/ /index.php?$args;
}

rewrite /wp-admin$ $scheme://$host$uri/ permanent;

location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
    expires 24h;
    log_not_found off;
}

location ~ \.php$ {
    try_files $uri =404;
    fastcgi_split_path_info ^(.+\.php)(/.+)$;
    include fastcgi_params;
    fastcgi_index index.php;

    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;

    fastcgi_pass php;
}
```
