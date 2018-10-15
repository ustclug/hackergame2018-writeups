# 小 T 的 hackergame 2018 writeup

## 我是谁

大家好，我是小 T，听说这几天你们都在找我，~~希望与我一起讨论哲学与文学（大误）~~。首先非常感谢大家参与 hackergame 2018，这是我第一次为这样的比赛出题，有这么多人回答出了我的题目，我感到非常感动。

废话不多说了。接下来是「我是谁」的 writeup。

这道题是在 hackergame 题目准备末期出的，因为需要一些简单的题目。灵感来源是我在大一上半学期的时候，在「[计算机导论](http://mis.teach.ustc.edu.cn/queryxkkccx.do?kcid=2430&bjbh=01104401&xnxq=20181&comefrom=kb)」（大致是计算机的简单概念入门课程）课上玩手机的时候——那时候刚好在讲网络——看到了[维基百科的 HTTP Status Code 的页面](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)，发现里面有一个非常搞笑的代码，就是你们在这道题里面看到的 418 I'm a teapot。

这就是第一小题（哲学思考）的题解，其实只要在页面上打开开发者工具，在 Network 部分就能看到解答了（致萌新：如果你什么都没看到，刷新一下页面）。只要输入的内容小写之后包含 teapot 这个单词，就能拿到 flag，这里我根本没有打算为难别人。（不过可以试试输入 coffee 会发生什么）

至于第二小题的话……Can I help me?

![Can I help me?](imgs/little_busters_kud_can_i_help_me.png)

*（图文无关）*

其实本来是没有第二小题的，但是有人希望我实现 HTCPCP-TEA，于是就……

页面提醒尝试用其他的 *methods* 来请求页面。我承认这里确实需要一点点脑洞……这里的 method 其实是指 [Request method](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods)，直接点击链接的话使用的是 GET 来连接的。不过如果你尝试用 POST 来请求页面的话，会有非常清楚的提示：

> The method "POST" is deprecated.
>
> See RFC-7168 for more information.

去读 [RFC-7168](https://tools.ietf.org/html/rfc7168) 就行了。根据：

> To this end, a TEA-capable pot that receives a BREW message of content type "message/teapot" MUST respond in accordance with the URI requested, as below.

最终使用 BREW 请求页面，且带上 `Content-Type: message/teapot` 请求头的时候，页面会在 `Alternates` 响应头给出真正可以泡红茶的 URL。用相同的方式请求那个 URL，就能获得第二个 flag。（其实还隐藏着一些彩蛋，可以试试）

嗯？你说不知道怎么请求？发送特定请求的方式有很多，这道题中可以使用的一种方式是使用 `curl` 的 `-I`, `-X` 和 `-H` 参数来完成。具体内容可以查看 `man curl`。用 BurpSuite 等工具，甚至是 Firefox 的开发者工具改请求也都是可以的。

其实第二小题的协议实现还可以再逼真一些，但是出于 Flask 的限制，加上时间有一些仓促，所以没有实现，不然这道题还可以更真（qiàn）实（biǎn）得多。至于有人问是否有实现了 HTCPCP-TEA 的茶壶~~手办~~嘛……反正我是没有，不过我很期待有人能做出来。

## 她的诗

当我得知这道题出现了非预期解时，我的内心是崩溃的。如果您是用非预期解完成的题目（表现为：得到了 flag，但完全不知道为什么），请先查询资料，思考一下为什么会存在这个非预期解，然后继续看这篇 writeup。~~顺便想给某站点的站长致以亲切友好的问候。~~

### 预期题解

运行 `helper.py` 可以得到诗的内容，但比较明显的事情是，重点不在这个脚本可以解码出的诗上——如果是的话，我没有必要再去绕一大圈编码再写解码脚本发给你；而且题干里面也是有暗示的。

> 「我要提醒一下你，只纠结于字面意思是很费劲的，而且……你不会得到任何有用的结论。」

我都这么说了啊……

`helper.py` 里面的 `begin 666 <data>` 是什么？搜索引擎可以很快告诉你，这是 uuencoding 编码。可以看到，这个脚本将文件的每一行当作一个被 uuencoding 编码后的文件进行解码。如果你去试一下，会发现一大部分明文行重新编码之后获得的字符串和原文件在末尾的地方不一样。那么很明显，这里有问题。

Uuencoding 编码的结构是这样的：

```
 <length character><formatted characters><newline>
```

第一个是长度字符，通过长度 + 32，再转成 ASCII 的方式出现（比如说，有 3 个字符，就是 `chr(3 + 32)`，即 `#`）。之后每三个字节（字符）为一组，以如下的方式编码：

![Uuencoding 编码方式](imgs/uuencoding_wikipedia.png)

*（摘自[维基百科对应页面](https://en.wikipedia.org/wiki/Uuencoding)）*

但不是每一行的字符都是 3 的倍数，那么如果最后一组没法填充的话（即长度乘 4 模 3 不为 0），那么对应部分就会填 0。那么我们想要隐藏的东西能不能就这样塞在填 0 的部分里面呢？答案当然是可以的，不然就没有这道题目了。

获得 flag 的做法中其中一种是一行一行用位运算的方式把 flag 的每个比特拼起来；另一种特定于这道题的方式是：直接扩大每行第一个长度字符到正确的值，具体的原因见下。

### 非预期题解

那么非预期题解是怎么回事呢？在出题的时候，因为 flag 很长，为了让「诗」短一点，把所有能用的比特都用上了，但是：

- 如果最后一组只有一个字符，那么最多能填 16 位。
- 只有两个的话，就是 8 位。

发现什么问题了吗？**它们都是 8 的倍数，即一个字符位数的倍数**。在大多数的实现中，解码都是正常的，但是**如果有 uuencoding 解码的实现忽略了表示长度的第一个字符**，并且你找到了这个实现，那么……就可以无脑获得 flag。

（对我来讲）悲痛欲绝的是，想找到这个不太正常的实现并不难。

![emotion_feeling_hurt](imgs/emotion_feeling_hurt.png)

*（图文无关 \* 2）*

这是我出题时候的疏忽，向各位道歉。

### 修复版本

这是修复了「她的诗」非预期解的版本：[https://github.com/taoky/her_poem_fixed_version](https://github.com/taoky/her_poem_fixed_version)。如果您用了非预期解完成原题，我强烈建议再试一下我微调后的题目。

### 花絮

后台看提交记录的时候，各位提交的 flag 千奇百怪，很心疼真跑去文本分析诗句和脚本写得有问题的同学。比如说这位同学，一直在正确 flag 的边缘徘徊：![Have some trouble writing scripts](imgs/wrong_script.png)

还有这位：

![Search Engine](imgs/ability_to_use_google.png)

我想表扬一下这位同学，他/她提交的 flag 证明了自己使用搜索引擎的能力，虽然……很遗憾，方向……是完全错误的。

另外的话，这道题是「她的诗」，不是 [请使用最新版黑曜石浏览器查看] 的诗啊……为什么会有人提交那种 flag 啊😂

## 她的礼物

这道题做出来的人数比我预想的少……难道都是被混淆吓跑的吗？实话讲，混淆确实是我故意弄上去的，为了劝退一般的逆向方法。~~万恶之源在[这](https://github.com/obfuscator-llvm/obfuscator/)~~。为了不让你轻易发现这是个魔改 clang，我特意在二进制文件里把 LLVM 的版本信息改成别的了。

打开程序，可以倾听到~~悦耳的~~蜂鸣器声（取决于环境），欣赏到~~美妙的~~歌词，只是运行了 10 秒，这个程序就会自己退出。难道大家真的没有一种想要让这个程序正常一点的冲动吗……

正解其实是 hook（或者 patch）这个二进制，把所有烦人的函数都搞掉。使用 `LD_PRELOAD` hook（动态编译的）Linux 二进制文件的相关内容，可以参考 [[1]](http://kaiyuan.me/2017/05/03/function_wrapper/), [[2]](https://blog.netspi.com/function-hooking-part-i-hooking-shared-library-function-calls-in-linux/) 等资料。

Hook 的话至少需要把 `alarm()`、`sleep()` 和 `system()` hook 掉，要加速的话输出部分也可以处理一下。最后我自己写的「库」的代码如下：

```c
#include <stdarg.h>
#include <stdio.h>

int system(const char *command) {
    return 0; // no beeping
}

unsigned int alarm(unsigned int seconds) {
    return 0;
}

unsigned int sleep(unsigned int seconds) {
    return 0;
}

int puts(const char *s) {
    return 0; // speed up
}

int printf(const char *format, ...) {
    if (format[0] == 'f') {
        // is flag
        va_list arg_ptr;
        va_start(arg_ptr, format);
        vprintf(format, arg_ptr);
        return 0;
    }
    return 0;
}
```

用对应的编译参数编译，然后改 `LD_PRELOAD` 环境变量，等待一小段时间之后程序就乖乖把 flag 吐出来了。

打 patch 也是同理，只是注意不要 patch 太过火：有人问我为什么他 patch 了之后结果不对，我看到他把 `main()` 里面所有的循环都 nop 掉了，很想跟他说他的思路基本是正确的，但是根据规定，又只能回复「无可奉告」，我也很无奈。

花絮:

1. 其实原来这个程序是静态编译的，后来为了降低难度（毕竟是定向新生的比赛），改成了动态编译。不知道有没有人真的用硬碰硬的办法获得 flag 的……其实我也很希望能看到用其他（我）想象不到的方式做出这道题的题解。

2. 没人觉得，「她」所在的文学社似乎不是很文学吗😂 其实在编第一道题「她的诗」的时候，「她」的原型是某个游戏的真女主角，但是随着后面题面修改、加题目，就看起来不太像了。