# 王的特权

小王同学刚刚学会了 Rust 语言，今天拿着自己写的 BUG 来找老张同志。

老张：哟，小子学会写 Rust 了？

小王：没错，刚出炉的程序，而且只有我能运行！

老张：只有你能运行？我不信。

小王：不信你就试试呗！

小王放心地把程序交给了老张，并声称可以找任何人来帮忙。作为老张多年的好友，你能帮他破开「王的特权」的秘诀吗？

注意：

- 做这道题，你可能需要准备 64 位 Linux 环境。
- 做题时请保证网络畅通。**但这是为了避免直接拿到 flag 而给你的小小考验，预期解法与网络无关，请不要在这方面下工夫。**

[打开题目](src/rev)

---

这是一道 Rust 逆向科普题。[Rust 官网](https://www.rust-lang.org/zh-CN/)的
介绍是：**Rust 是一种系统编程语言。 它有着惊人的运行速度，能够防止段错
误，并保证线程安全。**

## 源代码

会 Rust 的选手看到代码应该什么都明白了吧！

``` rust
use std::env;
use std::net::{TcpStream, Ipv4Addr};
use std::io::{Write, Read};

const KEY: u64 = 19260817;
const ADDR: [u8; 4] = [0, 0, 0, 0]; // Not relevant MASKED
const PORT: u16 = 0; // NOT relevant MASKED

fn main() {
    let args = env::args().collect::<Vec<String>>();
	
	// 本题的预期解法
    args[0].find("sudo").expect("Permission denied");
    
	// 下面代码的目的只是：
	// 1. 不要把文件拖到 IDA 里面就看到 flag
	// 2. 不要被随便看到服务器 IP 和端口号……
	let local_key = args[0].as_bytes()[0] as u8;
    let addr = Ipv4Addr::new(ADDR[0] ^ KEY as u8, ADDR[1] ^ KEY as u8, ADDR[2] ^ KEY as u8, ADDR[3] ^ KEY as u8);
    let port = PORT ^ KEY as u16;
    let mut stream = TcpStream::connect((addr, port)).unwrap();
    stream.write(&[local_key]).expect("write");
    let mut buf = Vec::new();
    stream.read_to_end(&mut buf).expect("read");
    for c in &mut buf {
        *c ^= local_key;
    }
    println!("{}", String::from_utf8(buf).expect("decode"));
}
```

题目中的粗体字「不是网络题」其实就是明示，不要尝试手动构造网络请求。

## 思路

首先，把 `b` 跑一下：

``` shell
thread 'main' panicked at 'Permission denied', libcore/option.rs:1010:5
note: Run with `RUST_BACKTRACE=1` for a backtrace.
```

给不熟悉 Rust 的选手的注释：这句话来自于代码的第二行的 `.expect` 调用。
熟悉 Rust 的选手可能直接就会发现这个 Permission denied 的 panic 来自于
`Option` panic 的而不是真正的没有权限。而且是默认的输出。那就按它说的，
运行一下：

``` shell
$ RUST_BACKTRACE=1 ./b
thread 'main' panicked at 'Permission denied', libcore/option.rs:1010:5
stack backtrace:
   0: std::sys::unix::backtrace::tracing::imp::unwind_backtrace
             at libstd/sys/unix/backtrace/tracing/gcc_s.rs:49
   1: std::sys_common::backtrace::print
             at libstd/sys_common/backtrace.rs:71
             at libstd/sys_common/backtrace.rs:59
   2: std::panicking::default_hook::{{closure}}
             at libstd/panicking.rs:211
   3: std::panicking::default_hook
             at libstd/panicking.rs:227
   4: std::panicking::rust_panic_with_hook
             at libstd/panicking.rs:477
   5: std::panicking::continue_panic_fmt
             at libstd/panicking.rs:391
   6: rust_begin_unwind
             at libstd/panicking.rs:326
   7: core::panicking::panic_fmt
             at libcore/panicking.rs:77
   8: core::option::expect_failed
             at libcore/option.rs:1010
   9: <core::option::Option<T>>::expect
  10: b::main
  11: std::rt::lang_start::{{closure}}
  12: std::panicking::try::do_call
             at libstd/rt.rs:59
             at libstd/panicking.rs:310
  13: __rust_maybe_catch_panic
             at libpanic_unwind/lib.rs:102
  14: std::rt::lang_start_internal
             at libstd/panicking.rs:289
             at libstd/panic.rs:392
             at libstd/rt.rs:58
  15: std::rt::lang_start
  16: main
  17: __libc_start_main
  18: _start
```

为了降低题目难度，没有使用优化编译，也没有去除调试符号，所以你可以轻松
看到完整的 backtrace。注意到第 10 行的 `b::main`，这意味着 panic 就发
生在 `b::main` 函数中。

那么直接看反汇编喽。（建议首先使用 `rustfilt` 工具去除命名修饰。）

``` assembly
; 在 b::main 中

   10b27:	e8 14 12 00 00       	callq  11d40 <std::env::args>
; 这个函数可以收集程序选项参数，类似于 C 语言里的 argv

   10b4d:	e8 ee 97 ff ff       	callq  a340 <core::iter::iterator::Iterator::collect>
; 注意到这个 collect 和周围的一些代码，可以推测源代码就是把 args 收集到 Vec<String>

   10b5e:	e8 bd c0 ff ff       	callq  cc20 <<alloc::vec::Vec<T> as core::ops::index::Index<I>>::index>
; 那么这里显然是对 vec 进行取下标操作（不难发现就是 argv[0]）

   10b75:	e8 c6 9b ff ff       	callq  a740 <<alloc::string::String as core::ops::deref::Deref>::deref>
; String deref 到 &char，不懂的话其实可以略过

   10b9b:	48 8d 15 cf a3 04 00 	lea    0x4a3cf(%rip),%rdx        # 5af71 <str.1+0x21>
; 下面来到这里…… 于是你找到了一个字符串常 'sudo'

   10bb7:	e8 a4 f3 ff ff       	callq  ff60 <core::str::<impl str>::find>
; 在 argv[0] 里面找这个 'sudo'
```

下面就先不看了，直接试试把文件名改成 sudo 或者 bsudo 或者
bbbsudofhdksj 然后跑一下看看效果。

``` shell
$ ./abcdefghijklmnopqrsuvwxyzsudoxiaowang
flag{CA11m30xidiz3r}
```

好的，你拿到了 flag，去交吧！

## Flag

`flag{CA11m30xidiz3r}`

里面的文本是 call me oxidizer（叫我氧化剂），暗示 rust（铁锈）是被氧化
剂氧化的产物。

## 花絮

这道题原本是一道签到题，想在 `argv[0]` 上做文章而已，只不过顺手用了
Rust 而没有用 C，然后发现其实没那么签到，因为有很多选手对 Rust 并不熟
悉。第一版时里面还使用了多线程和 MPSC channel，后来发现不太容易就去掉
了这个设定，感兴趣的选手可以自己试试。然后，剩下的就成为了历史。
