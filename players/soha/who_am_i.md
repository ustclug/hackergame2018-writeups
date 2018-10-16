[返回](./README.md)

## 0x06 我是谁.哲学思考

一直开着开发者工具的我一眼就看出了 Network 里面的不对劲。

![Snipaste_2018-10-09_20-59-16.png](./images/960723743.png)

填入 `teapot` 搞定。

## 0x07 我是谁."Can I help me?"

根据第一根 flag 提供的 url，建议我们使用别的 method 来请求。既然说到 brew tea，说到 teapot，那肯定是 RFC 7168 啦。（ `HTCPCP-TEA` 真好玩！）

读一读 RFC 7168 就可以写出下面这个 payload:

```
BREW /the_super_great_hidden_url_for_brewing_tea/ HTTP/1.1
Content-Type: message/teapot
```

![Snipaste_2018-10-09_21-03-31.png](./images/3376090344.png)

然后接着请求 `Alternates` 里面提供的 url。

```
BREW /the_super_great_hidden_url_for_brewing_tea/black_tea HTTP/1.1
Content-Type: message/teapot
```

![Snipaste_2018-10-09_21-04-39.png](./images/831079774.png)

嗯……给大佬递茶……
