这个目录内部包括参考答案 `solution.py` 和其它依赖文件。
目录同时包含了 `Dockerfile`, 用户可以用以下方式检验答案：

```bash
docker build -t solution .
```

```bash
docker run -it solution
```