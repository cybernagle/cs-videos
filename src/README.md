# unlink
2001 的一篇文章, once upon a free, 介绍了关于 glibc 中关于 free 代码存在了数十年的的一个漏洞. 
具体一点, 就是 malloca 过程当中,管理 malloc 的数据结构, malloc\_chunk , 在从其中的双链表释放的过程当中,对小空间的合并以及链表的重新链接的利用,从而访问以及修改我们不能修改的内容. 
该代码于 glibc 当中,于 2018 年从 unlink 宏修改位了 unlink_chunk 函数, 所以,本视频将介绍的是 2018 年的关于 unlink 的版本, 有兴趣的同学可以去研究最新的代码.

言归正传, 我们将以两个角度来看该问题: 
1. 源代码的结构是什么? 包括 chunk 的结构, unlink 的时候,释放过程以及安全机制.
2. 基于这个结构, 我们看该结构会如何被利用从而可以做到一些逾规之事.

话不多说,咱们开始吧.首先我们来阅读一下 glibc 当中, 关于管理内存单元的结构以及释放的关键性代码.
可以看到,我们的每个单元由数据结构 malloc_chunk 来进行管理,
其包含一个上一个 chunk 的大小, 当前大小以及指向前驱节点以及后驱节点的指针.
这里, 我们就可以知道,malloc 得到的数据结构是一个双向链表.
chunk definition
继续向下, 我们可以看到 free 的代码, 在free 的过程当中,会判断上一个节点是否是inuse的状态.
如果没有,那么当前节点和前一个节点将会进行合并.
然后, 使用unlink宏,将合并后的节点进行释放.
而释放的过程页很简单, 在判定前后两个节点是否指向释放节点本身后.
将双向链表重新进行链接,从而释放该区域.
接下来, 我们将这些数据结构可视化,看看对应代码具体执行了什么事情.
restore state
首先, 是我们的内存块管理单元.
这个内存块管理单元当中, 黄色区域是chunk 的头,而蓝色部位是chunk的数据节点本身.
当我们访问 chunk 的地址的时候,一般指向的,都是chunk的数据节点本身.
假设我们现在申请了两个内存单元, chunk0, chunk1
chunk desc 
chunk double link arrows
申请了之后,它们将会链接起来.chunk1 的F就是chunk0,
chunk0的B就是chunk1
如果我们要释放 chunk1
normal unlink
那么 chunk0 的B将会指向chunk1 的后继节点.而chunk1的后继节点将会指向chunk0
并且, 我们在释放前会再次确认被释放的前驱节点的后继节点是我自己.
以及后继节点的前驱节点是我自己.
而如果 chunk1 的 presize 的低1位为0
那么 chunk1, chunk2 将进行合并之后, 再进行释放.
上面我们讲了正常释放的逻辑, 接下来我们看看该漏洞会以怎样的形式被利用.
我们还是用代码的形式来进行演示.
about how to hack
what we need to do is, unlink ...
首先, 这个代码块的前三行在 chunk0 的位置创建了一个fakechunk.
并且申请了两个地址放在了 fakechunk 的前后指针当中.
这两个指针作为变量都位于栈上.
这里注意看, fakechunk的F也就是前驱是相较于 chunk0 向上的两个位置.
fakechunk的 B 也就是后继, 是相较于 chunk0 向上的三个位置.
而这两行代码,fake_chunk -> F -> B == B->F = chunk0_addr
就可以保证fakechunk它的前驱的后继,以及后继的前驱是指向自己fakechunk本身.从而通过安全检查.
接下来咱们对要释放的 chunk1 的头部进行修改.即将presize修改为fakechunk的大小0x80,然后将最低位置为0
让堆管理器认为 chunk0 下的 fake chunk 是空闲的. 从而可以让fakechunk和chunk1一起被释放掉.
最后, 咱们来到 unlink 的过程.即将fake_chunk 的前驱节点的后继节点.
在我们的视频当中, fake_chunk 的前驱节点是chunk0 - 3
而在malloc_chunk的数据结构告诉我们,后继节点是存储在其起始地址+3的位置,
也就是存储我们的chunk0地址的位置.
这样,chunk0 的前驱节点也就是 chunk0-3 的位置, 指向了chunk0 本身.
也就是意味着,我们访问chunk0 的时候,就是在访问chunk0-3的栈上面的位置.
这样,我们就可以通过chunk0来访问本不该能够访问的栈地址而完成了hack.
