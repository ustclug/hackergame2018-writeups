# 回到过去

那些发明Unix操作系统的大叔们怎么编辑文本文件呢？

据记载，他们使用一种叫做ed的神奇编辑器，而Unix Hater's Handbook对此有生动的描述：

Ken Thompson has an automobile which he helped design. Unlike most automobiles, it has neither speedometer, nor gas gauge, nor any of the other numerous idiot lights which plague the modern driver. Rather, if the driver makes a mistake, a giant “?” lights up in the center of the dashboard. “The experienced driver,” says Thompson, “will usually know what’s wrong.”

也许是八十年代的某天，调皮的Lawrence正在使用他的DEC VT终端连接到一台大型Unix主机编辑文件——他是个机灵的家伙，使用ed的时候从不需要看屏幕的输出。只看他正在用ed写本题的flag。写了半天，兴高采烈的Lawrence接了个电话，关上ed才发现自己没有保存。

聪明的你能根据对他键盘的记录，还原出你要找的flag吗？

**info ed** 命令对于没有使用过ed的你是十分有用的。

Hint1：有多个字符串的话，就从上到下连成一行提交就好啦。

Hint2：flag只接受数字和字母。

[打开题目](src/input_sequence)

---
## 背景和题目设定
一道简单题目，考察选手对 Unix 环境基本操作的熟悉程度，和对输入输出重定向等的基本理解。
灵感来源于 *Unix Hater's Handbook*，这也是小 L 同学第一次知道还有 ed 这个~~鬼畜~~编辑器。事实上，当你把环境变量 `$TERM` 设置为一个 `terminfo` 中没有的终端类型时，比如

```
export TERM=vt233
```

那么各种~~牛鬼蛇神~~编辑器就都不太能正常工作了——比如新手友好的 `nano`：
```
Error opening terminal: vt233.
```

不过友好的 Vim 会猜测你的终端是 ansi，继而在你的终端模拟器上运行。但如果你的终端模拟器是一个毫不解析控制字符的傻终端呢？
除了用 `cat` 编辑文件，你还可以用 `ed`。

`ed` 虽然已经埋入历史的尘埃，但是它还是 [Single Unix Specification](https://en.wikipedia.org/wiki/Single_UNIX_Specification) 的一部分。

## 一个典型的解题思路
第一步，看到题面上的提示：*忘记保存文件 *、*ed 编辑器 *、*info ed*、*给定输入序列*
第二步，去看看 `info ed`：

> 首先，*ed * 是一个 Line Editor（行编辑器），这意味着用户进行的编辑操作无法在屏幕上得到所见即所得的反馈。*ed * 在内存中维护一个缓冲区，用户所有的修改都会存在缓冲区中，直到 * w filename * 命令将其写入文件。

> a 命令用于向缓冲区的末尾加入文本，以单独一行的 *.*（英文句点）作为结束输入的标志。

> *,p* 命令可以向屏幕输出缓冲区的内容。
> *2* （一个单独的行号）用于选择需要修改的行。
> *s/old/new* 可以替换选择行中的 *old* 为 *new*。
> *2m3* （行号 m 行号）命令可以将第 2 行挪到第 3 行后面。特别的，*2m0* 表示把第二行放在第一行前面。
> *q* 命令用于退出 *ed* 编辑器。
> 值得注意的是 *ed* 独特的报错方式：一个大大的 **?**。特别的，一个缓冲区没有保存的 ed 需要两个 *q* 命令才可以退出，第一个 *q* 命令的结果是一个大大的 **?**。

第三步，继续看题目的 `input_sequence`：

```
q
ed
a
flag{
.
a
44a2b8
a3d9b2[ESC]c
c44039
f93345
}
.
2m3
2m5
2m1
2
s/4/t
q
q
```

前面的 q 和 ed 是上一次 ed 会话的残留，我们应该先删去。
然后发现他没有保存，所以删去末尾的 q，加上 `w flag.txt`，变成这样：

```
a
flag{
.
a
44a2b8
a3d9b2ESCc
c44039
f93345
}
.
2m3
2m5
2m1
2
s/4/t
w flag.txt
q
```

并且运行
```
ed input_sequence && less flag.txt
```

得到 `flag.txt` 如下：
```
flag{
t4a2b8
c44039
f93345
a3d9b2ESCc
}
```

发现一个神秘的 `ESCc`，那是什么？那其实是一个 *转义序列*，用来控制终端的行为。在本例中为清屏。值得注意，`ESC` 并不是三个普通的字母，而是一个不可打印字符，而 `less` 为了向用户显示，所以写成 `ESC`，并且用白底标出。所以，如果你直接运行
```
cat flag.txt
```

你将不能看到完整的 flag。
所以，本题的 flag 是 `flag{t4a2b8c44039f93345a3d9b2}`。

可能最后的 Escape Sequence 有些小坑，但是没有这一道小弯弯不就不 *DEC VT 终端* 了？（大雾
