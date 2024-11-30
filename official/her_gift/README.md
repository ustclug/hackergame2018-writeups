# 她的礼物

（在做这道题之前，你可能需要先完成题目「她的诗」的一部分。）

小 T 的生日就要到了，在一天前，他收到了她发的电子邮件。

「祝你生日快乐！……」庆生邮件的开头大概都是这个样子的。自从小 T 加入校文学社以来，她可没少给他带去惊吓。这家伙邮件里面又会写什么东西？

出乎他意料的是，这封邮件看起来挺正常的，除了结尾之外。

「另外呢，我写了一个小小的程序送给你，在里面藏了一些东西，不过运行它是需要密码的，密码我想想……哦，还记得上次我给你的那首诗吗？就是那首诗，用你朋友的脚本解密之后的第 10 行，然后啊我还要去赶路呢，就先写到这里吧，拜拜～」

附件看起来像是一个 Linux 下的可执行文件。理论上讲，把密码作为参数启动程序，就能看到她想要告诉小 T 的字符串了。不过……这家伙不会藏了什么 `rm -rf / --no-preserve-root` 这种命令（注：请勿在自己的机器上执行此命令！）在里面吧？但小 T 又想，她不可能会做出这种事情的。

[打开题目](src/gift)

---

（承接“她的诗”）

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