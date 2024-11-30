# Word 文档

自从加入了 Doki Doki Linux Club ([注1](https://dokidokilinux.club/)），用上了 Linux，D 同学每天都能学到好多新东西。

Linux 好是好，就是没有 Microsoft Office 系列软件，导致看学校的各种通知文件，填申请表等等都变得不那么方便，上次还差点因此错过了 7 号的会议。

突然有一天 D 同学的一个朋友告诉他，其实新版 Office 的文件格式是公开的！

D 同学非常高兴，公开的文件格式或许意味着可以自己写程序来读取和编辑内容，再也不用切换系统或者开虚拟机了。

D 同学追问这个朋友：那么这个文件格式具体是怎么样的呢？

朋友传来一个 OfficeOpenXML.docx。

[打开题目](src/OfficeOpenXML.docx)

---

这道题是一道非常简单的题目，主要是想让同学们了解一些文件格式的常识。

## 解法

根据题目中的提示，下载 word 文件，打开提示损坏，修复后可以看见维基百科上关于 Microsoft Office 系列文件格式的介绍。

注意到：

> 一种以[XML](https://zh.wikipedia.org/wiki/XML)为基础并以[ZIP格式](https://zh.wikipedia.org/wiki/ZIP%E6%A0%BC%E5%BC%8F)压缩的电子文件规范

将文件后缀名改为 `.zip` 或直接强行解压，打开解压后的文件，可以得到 flag.txt，去掉换行之后即为答案。

```shell
cat flag.txt | tr -d '\n'
```

flag 为：`flag{xlsx,pptx,docx_are_just_zip_files}`

不仅是 `docx`，还有 `xlsx`, `pptx`等的本质都是 zip 压缩包。