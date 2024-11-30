# 猫咪遥控器

<p style="color:red;">提示：flag 格式为 flag{......}，只包含字母，其中有且只有两个为大写字母。</p>

今天的 App Store 首页故事是《猫咪占领世界》([详情](https://itunes.apple.com/cn/story/id1435731237))。

SERIOUSLY?

D 同学不禁开始幻想被猫咪占领的世界：集中营里成群的铲屎官，密密麻麻的 Nepeta cataria（[Wikipedia](https://en.wikipedia.org/wiki/Catnip)）农田，随意摆放的纸箱子占满了道路……

想想就可怕，不过 D 同学知道人类还有终极秘密武器可以用——猫咪遥控器，有了猫咪遥控器，再多的猫咪也只会乖乖地听人类的话，哈哈哈哈哈～

下面是制作猫咪遥控器的技术总结，需要的原料有：

- 5mW 6mm 点状激光二极管一个；
- 锂电池一个；
- 导线若干；

然后用导线将锂电池和激光二极管连接起来（这一步的目的是让二极管亮起来，不想二极管亮起来的同学可以不连），一个美味的猫咪遥控器就做好了。

猫咪遥控器的原理非常简单！撸猫学会曾经有论文给出过结论：[激光笔指向哪里，猫咪就会跑到哪里](https://ftp.ustclug.org/misc/cat_remote.mov)。

为了报复猫咪把自己的代码打乱（见：猫咪与键盘），D 同学把猫咪遥控器绑在可以上（UP）下（DOWN）左（LEFT）右（RIGHT）移动的三轴机械臂上，开始使用树莓派（一款基于 Linux 的单片机计算机）控制三轴机械臂，进而控制猫咪在草地上跑来跑去。

附件是树莓派上留下的调试输出信息，我们赶到现场时只剩下这个了。

[打开题目](src/seq.txt)

---

欢迎来到猫咪系列题目之**猫咪遥控器**。

这道题是一道非常简单的题目，主要是想让同学们学会一些程序画图的技巧。

根据题目提示，我们需要将控制序列画出来，并且我们根据常识和题目提示，能知道：

UDLR 分别代表：上（UP）下（DOWN）左（LEFT）右（RIGHT）。

## 解法一：传统而可靠的办法

找一张纸（需要比较大的），花一下午即可。

## 解法二：使用 JS Canvas

我觉得这是最简单的一个办法，编程和解题都借助常见的浏览器（比如 Chrome）即可完成，我的解题代码如下：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cat Controller</title>
    <style>
        #path {
            border: 1px solid #000000;
        }
    </style>
</head>
<body>
<canvas id="path" width="1200" height="300"></canvas>
<script>
    var seq = "DDDDDDD...DDDLLLLLLLL"; // 题目中的序列
    var ctx = document.getElementById('path').getContext('2d');
    var x = 0, y = 0;
    
    function move(type) {
        switch (type) {
            case 'U': y -= 1; break;
            case 'D': y += 1; break;
            case 'L': x -= 1; break;
            case 'R': x += 1; break;
        }
        ctx.fillRect(x, y, 1, 1);
    }
    
    for (var i = 0; i < seq.length; i++) {
        move(seq[i]);
    }
</script>
</body>
```

把上面的代码保存为 remote.html，用浏览器打开即可得到路径：

![image-20181016114941390](images/image-20181016114941390.png)



flag: `flag{MeowMeow}`
