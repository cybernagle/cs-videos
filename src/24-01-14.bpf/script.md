# BPF 是什么?

它可以安全高效地扩展内核的能力而无需修改内核源代码或加载内核模块。
它可以监控内核中的网络流量，并根据流量类型进行流量控制。
它可以在程序运行时, 动态的植入监控点,获取运行时的状态.
它叫做 ebpf.

# BPF 历史 

在 1993 年, 一篇论文 ("The BSD Packet Filter: A New Architecture for User-level Packet Capture" 在屏幕上显示这个, 并翻译成中文) 
描述了如何解决数据包的抓取过程当中, 在内核态和用户态之间的数据复制导致了大量的性能损耗问题.(一个图, 从内核态流动到用户态, 判断, drop , 或者流给用户)

文中提到了的解决方案是, 在内核态当中,使用自定义的指令来对数据包进行过滤的功能. 并将这种解决方案被称之为: BPF
(一个图, 从在内核态进行判断, drop , 或者直接给到用户)

1997 年, linux kernel 2.1.75 在内核当中实现了一个小的 bpf 的虚拟机,用于执行 bpf 的指令, 而后, tcpdump 采用了该技术用于 socket 过滤功能.

时间进一步来到了 2014 年, linux 的内核版本来到了 3.18, bpf 也进化成为了 ebpf

我们说进化, 主要是 bpf 的功能发生了以下主要的改变: 
1. 它的指令扩展支持了 64 位的指令集
2. 在原有的执行环境当中, 添加了 map 功能, 让大数据的操作成为可能.
3. 操作系统专门新增了一个系统调用, 被称之为 bpf()
4. 为了安全性, 新增了代码检查器.

从这个时间点开始, ebpf 的应用范围逐渐的迈出网络过滤. ebpf 可以使用在系统调用, socket, 文件系统,KPROBE, CGROUP 等等. 

(在内核态的方框上面, 添加上系统调用,文件系统,SOCKET等等.)
换句话说, 基本上内核中的各种功能, 都可以动态的附加上 ebpf 的程序.

2016 年, 各个大厂, Netflix 开始大批量应用 ebpf 在系统监控领域, Cilium 项目启动, 2017 年, Facebook 的所有流量都使用 ebpf 的 xdp 来进行处理.

如今, 国外的 GCP , AWS, RedHat, 微软

国内的阿里云,蚂蚁金服, 字节跳动, kindling 等等, 都在使用该项技术来提升安全性以及可观测性.
微软最近也开始研发了 eBPF for windows. 足见该项功能未来的应用场景.

# 一个实例

我们知道内核一般分为用户态和内核态, 内核态将负责对硬件进行调度工作, 而用户态则根据内核态的各种系统调用, 来实现各种各样的应用程序和服务.

ebpf 程序, 会分为两个部分, 用户态代码, 另外一个部分内核态代码. 

用户态代码, 可以是 python ,可以是 rust, 内核态代码, 会被编译成 ebpf 虚拟机的字节码, 在 bpf 虚拟机当中运行. 

而用户态的程序, 可以通过 bpf map 来获取 bpf 字节码获取到的内容.

让我们来看一个例子:

```
bpf = r"""
int hello(void *ctx) {
    bpf_trace_printk("Hello World!");
    return 0;
}
"""

from bcc import BPF
b = BPF(text=bpf)
syscall = b.get_syscall_fnname("execve")
b.attach_kprobe(event=syscall, fn_name="hello")

b.trace_print()
```

上面的程序可以被分为两个部分, 第一行 bpf 是 bpf 程序本身, 被编译后,会变成字节码在 bpf 虚拟机当中执行.
`b.get_syscall_fnname("execve")` 将这个字节码程序附加到了 execve 系统调用.
这样, 当操作系统每次执行 execve 的时候, bpf 虚拟机当中字节码就会被执行. 并且在标准输出打印 "Hello World!"

如下所示:

<video width="320" height="240" controls>
  <source src="ebpfhello.mov" type="video/mov">
</video>
