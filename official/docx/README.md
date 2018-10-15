# Word 文档

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