---
title: "C言語の #if 0 を使ったおもしろ技"
date: 2014-03-23T22:12:22
slug: "c-if-0"
categories: ["コンピューター"]
tags: ["コンピューター"]
summary: "C言語なのにスクリプト言語のように実行できるところが面白いですね。"
---

``` brush:
$ cat ./hello.c
#if 0
gcc -o hello hello.c
./hello
exit
#endif

#include <stdio.h>

int main( void )pre {
  printf( "Hello, World!\n");
  return 1;
}
$ chmod +x hello.c
$ ./hello.c
Hello, World!
```

C言語なのにスクリプト言語のように実行できるところが面白いですね。
