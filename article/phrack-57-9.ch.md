# Once Upon a Free

在Unix系统中，后来在C标准库中也出现了处理动态内存变量的函数。这允许程序以动态方式从系统中请求内存块。操作系统只提供了一个非常粗糙的系统调用'brk'来改变一个大内存块（被称为堆）的大小。

在这个系统调用之上，位于malloc接口，它在应用程序和系统调用之间提供了一层。它可以将大的单一块动态分割成较小的块，在应用程序请求时释放这些块，并在此过程中避免碎片化。你可以将malloc接口比作一个大型、但动态大小的原始设备上的线性文件系统。

malloc接口必须满足以下几个设计目标：

- 稳定性
- 性能
- 避免碎片化
- 低空间开销

通常只有少数几种常见的malloc实现。最常见的几种是System V实现（由AT&T实现）、GNU C库实现以及Microsoft操作系统（RtlHeap*）的类似malloc的接口。

以下是使用的算法及其所适用的操作系统的表格：

```
算法      	      | 操作系统
----------------------+----------------------------------------------
BSD kingsley          | 4.4 BSD、AIX（兼容性）、Ultrix
BSD phk               | BSDI、FreeBSD、OpenBSD
GNU Lib C（Doug Lea） | Hurd、Linux
System V AT&T         | Solaris、IRIX
Yorktown    	      | AIX（默认）
RtlHeap*    	      | Microsoft Windows *
----------------------+----------------------------------------------
```

有趣的是，大多数malloc实现都很容易移植，并且它们与体系结构无关。其中大部分实现只是构建了一个与'brk'系统调用交互的接口。你可以通过定义进行更改。我遇到的所有实现都是用ANSI C编写的，只进行了最少或甚至没有合理性检查。它们中的大多数都有一个特殊的编译定义，其中包括了断言和额外的检查。出于性能原因，在最终构建中默认关闭这些功能。其中一些实现还提供了额外的可靠性检查，可以检测缓冲区溢出。这些检查旨在在开发过程中检测溢出，而不是在最终版本中阻止攻击。

### 在带内存中存储管理信息

大多数malloc实现共享一种行为，即在堆空间内部存储自己的管理信息，如已使用或空闲块的列表、内存块的大小和其他有用的数据。由于malloc/free的整个理念是基于应用程序的动态需求，管理信息本身也占据了可变数量的数据。因此，实现很少会为自己的目的预留一定数量的内存，而是将管理信息“带内”存储在应用程序使用的内存块之前和之后。

一些应用程序使用malloc接口请求内存块，而后来可能会受到缓冲区溢出的漏洞。这种情况下，块后面的数据可能会被更改。可能会损害malloc管理结构。这首先由Solar Designer的向导式漏洞利用[1]所证明。

利用malloc分配的缓冲区溢出的核心攻击是以一种方式修改管理信息，使得随后可以进行任意内存覆写。这样，可以在可写的进程内存中覆写指针，从而允许修改返回地址、链接表或应用程序级数据。

要发动这样的攻击，我们必须深入研究要利用的实现的内部工作原理。本文讨论了常用的GNU C库和System V实现，以及如何在Linux、Solaris和IRIX系统下利用malloc缓冲区溢出来控制进程。

## System V malloc实现
==========

IRIX和Solaris使用基于自调整二叉树的实现方式。这种实现的理论背景已在[2]中描述。

这种实现的基本思想是在二叉树内保持等大小的malloc块列表。如果您分配两个相同大小的块，它们将位于同一节点以及该节点的同一列表中。树按其元素的大小进行排序。

### TREE结构

TREE结构的定义可以在mallint.h中找到，其中还包括一些易于使用的宏，用于访问其元素。mallint.h文件可以在Solaris操作系统的源代码分发中找到[4]。虽然我无法验证IRIX是否基于相同的源代码，但有几个相似之处表明如此。malloc接口在内部创建相同的内存布局和函数，除了一些64位对齐。你也可以在IRIX上使用Solaris的源代码进行利用。

为了允许每个树元素用于不同的目的以避免开销并强制对齐，每个TREE结构元素被定义为一个联合体：

```
/* 原型单词；大小必须为ALIGN字节 */
typedef union w {
size_t w_i; /* 无符号整数 */
struct t w_p; /* 指针 */
char w_a[ALIGN]; /* 强制大小 */
} WORD;
```

中央TREE结构定义：

```
/* 自由树中的节点结构 */
typedef struct t {
WORD t_s; /* 此元素的大小 */
WORD t_p; /* 父节点 */
WORD t_l; /* 左子节点 */
WORD t_r; /* 右子节点 */
WORD t_n; /* 链表中的下一个 */
WORD t_d; /* 保留空间给自指针的虚拟元素 */
} TREE;
```

块头的't_s'元素包含用户在调用malloc时请求的大小的向上取整值。由于该大小总是向上取整到字边界，'t_s'元素的至少低两位未使用 - 它们通常一直具有零值。它们不用于所有与大小相关的操作，而是作为标志元素使用。

从`malloc.c`源代码中可以看到：

- BIT0: 1表示忙碌（块正在使用），0表示空闲。
- BIT1: 如果块正在使用，如果连续内存中的前一个块为空闲，则此位为1。否则，它始终为0。

TREE访问宏：

```
/* 块中可用的字节数 */
#define SIZE(b) (((b)->t_s).w_i)

/* 自由树指针 */
#define PARENT(b) (((b)->t_p).w_p)
#define LEFT(b) (((b)->t_l).w_p)
#define RIGHT(b) (((b)->t_r).w_p)

/* 小块链表中的前向链接 */
#define AFTER(b) (((b)->t_p).w_p)

/* 树中列表的前向和后向链接 */
#define LINKFOR(b) (((b)->t_n).w_p)
#define LINKBAK(b) (((b)->t_p).w_p)
```

在所有分配操作中，都会强制执行一定的对齐和最小大小，这在这里定义：

```
#define WORDSIZE (sizeof (WORD))
#define MINSIZE (sizeof (TREE) - sizeof (WORD))
#define ROUND(s) if (s % WORDSIZE) s += (WORDSIZE - (s % WORDSIZE))
```

树结构是每个分配块的核心元素。通常只使用't_s'和't_p'元素，用户数据存储在't_l'之后。一旦节点被释放，这种情况就会改变，数据被重新使用以更有效地管理自由元素。这个块代表了自旋树中的一个元素。随着越来越多的块被释放，malloc实现试图将自由块合并到其旁边。最多可以在相同的时间内存在FREESIZE（默认为32）个悬空的自由块。它们都存储在'flist'数组中。如果在列表已满时进行了释放调用，那么此位置上的旧元素将被排除，并转发到realfree。然后，该位置被新释放的元素占用。

这样做是为了加速并避免在连续进行大量释放调用时出现碎片化的情况。真正的合并过程是由realfree完成的。它将块插入中央树中，该树从'Root'指针开始。树按其元素的大小进行排序，并且是自平衡的。这是所谓的“自旋树”，其中元素以特定的方式循环以加速搜索（请参考google.com上的“自旋树”以获取更多信息）。这在这里并不太重要，但请记住，自由块有两个阶段：一个在flist数组中，一个在从'Root'开始的自由元素树中。

有一些专门的管理例程用于分配小块内存，这些内存块的大小可能低于40字节。这里不考虑这些，但基本思想是有额外的列表，不将它们保留在树中，而是保留在列表中，一个列表对应一个小于40的WORD大小。

有多种方法可以利用基于malloc的缓冲区溢出，但以下是一种方法，可用于IRIX和Solaris两者。

当一个块被realfree时，会检查相邻块是否已在realfree的树中。如果是这种情况，唯一需要做的就是在逻辑上合并这两个块，并在树中重新排列它们的位置，因为大小已经改变。

此合并过程涉及到树内的指针修改，这些指针是由块头本身表示的节点。指向其他树元素的指针存储在其中。如果我们可以覆写它们，那么在合并块时可能会修改操作。

这是如何在malloc.c中实现的：
（已修改以显示其中有趣的部分）

```
static void realfree(void *old)
{
    TREE *tp, *sp, *np;
    size_t ts, size;

    /* 指向块 */
    tp = BLOCK(old);
    ts = SIZE(tp);
    if (!ISBIT0(ts))
        return;
    CLRBITS01(SIZE(tp));

    /* 看看是否值得与下一个块合并 */
    np = NEXT(tp);
    if (!ISBIT0(SIZE(np))) {
        if (np != Bottom)
            t_delete(np);
        SIZE(tp) += SIZE(np) + WORDSIZE;
    }

    // ...
}
```

我们将NEXT指针定义为直接跟随当前块的块。因此，我们有这种内存布局：

```
          tp               old              np
          |                |                |
          [chunk A header] [chunk A data] | [chunk B 或者 空闲块 ....]
                                          |
                                          块边界
```
在通常情况下，应用程序分配了一些空间，并从malloc获得了一个指针（old）。然后，出现了一次缓冲区溢出，溢出到块数据之后，可能会击中块后面的数据，这些数据要么是空闲空间，要么是另一个已使用的块。

```
np = NEXT(tp);
```

由于我们只能溢出到'old'之后的数据，所以我们无法修改自己块的头部。因此，我们无法以任何方式影响'np'指针。它总是指向块边界。

现在，进行检查以测试是否可能向前合并，即我们的块和其后的块。请记住，我们可以控制我们右侧的块。

```
if (!ISBIT0(SIZE(np))) {
    if (np != Bottom)
        t_delete(np);
    SIZE(tp) += SIZE(np) + WORDSIZE;
}
```

如果块为空闲块且不是最后一个块（特殊的'Bottom'块），则BIT0为零。然后，释放块的大小都会加起来，稍后在realfree函数的代码中，整个调整大小后的块会被重新插入树中。

一个重要的部分是，溢出的块不能是malloc空间内的最后一个块，条件是：

溢出的块不能是最后一个块
这是't_delete'函数的工作原理：

```
static void t_delete(TREE *op)
{
    TREE *tp, *sp, *gp;

    /* 如果这是一个非树节点 */
    if (ISNOTREE(op)) {
        tp = LINKBAK(op);
        if ((sp = LINKFOR(op)) != NULL)
            LINKBAK(sp) = tp;
        LINKFOR(tp) = sp;
        return;
    }

    // ...
}
```

还有其他情况，但这是最容易利用的一种情况。因为我已经对这个感到厌倦了，所以我只会在这里解释这个。其他情况非常相似（查看malloc.c）。

ISNOTREE将TREE结构的't_l'元素与-1进行比较。-1是非树节点的特殊标记，用作双向链表，但这并不重要。

无论如何，这是我们必须遵守的第一个条件：

fake->t_l = -1;
现在，链接FOR（t_n）和BAK（t_p）之间的解链操作被执行，可以重写为：

```
t1 = fake->t_p
t2 = fake->t_n
t2->t_p = t1
t1->t_n = t2
```
这是（以同时发生的伪原始赋值方式编写的）：

```
[t_n + (1 * sizeof (WORD))] = t_p
[t_p + (4 * sizeof (WORD))] = t_n
```

通过这种方式，我们可以一次性写入任意地址，同时与有效地址一起。我们选择使用这个：

```
t_p = retloc - 4 * sizeof (WORD)
t_n = retaddr
```
这样，retloc将被覆盖为retaddr，*(retaddr + 8)将被覆盖为retloc。如果在retaddr处有代码，应该有一个小跳跃越过字节8-11，以不执行此地址作为代码。此外，如果这符合情况，还可以交换地址。

最后，我们的覆盖缓冲区如下所示：

```
  | <t_s> <t_p> <t_l> <j: t_r> <t_n> <j: t_d>
  |
  块边界
```

其中：t_s = 一些小的大小，将较低的两位设置为零

```
t_p = retloc - 4 * sizeof (WORD)
t_l = -1
t_r = 垃圾
t_n = retaddr
t_d = 垃圾
```

请注意，尽管所有数据都存储为32位指针，但每个结构元素占用八个字节。这是因为WORD联合强制为每个元素使用至少ALIGN字节。默认情况下，ALIGN定义为八。

因此，块边界之后的真正溢出缓冲区可能如下所示：

```
ff ff ff f0 41 41 41 41  ef ff fc e0 41 41 41 41  | ....AAAA....AAAA
ff ff ff ff 41 41 41 41  41 41 41 41 41 41 41 41  | ....AAAAAAAAAAAA
ef ff fc a8 41 41 41 41  41 41 41 41 41 41 41 41  | ....AAAAAAAAAAAA
```

所有的'A'字符都可以随意设置。't_s'元素已被替换为一个小的负数，以避免NUL字节。如果想使用NUL字节，请使用很少的数量。否则，稍后的realfree函数将崩溃。

上面的缓冲区将覆盖：

```
[0xeffffce0 + 32] = 0xeffffca8
[0xeffffca8 +  8] = 0xeffffce0
```

请查看示例代码（mxp.c）以获取更详细的解释。

总之，如果你恰好在IRIX或Solaris上利用了基于malloc的缓冲区溢出：

1. 在溢出块后面创建一个伪块。
2. 这个伪块在传递给realfree时与溢出的块合并。
3. 为了使它传递给realfree，必须再次调用malloc()，或者必须有大量连续的free()调用。
4. 溢出的块不能是最后一个块（即Bottom之前的块）。
5. 在shellcode/nop-space之前加上跳跃，以不执行不可避免的unlink-overwrite地址作为代码。
6. 使用t_splay例程，也可以进行类似这样的攻击。因此，如果你无法使用此处描述的攻击（例如，你无法写入0xff字节），请使用源代码。
有许多其他利用System V malloc管理的方法，远远超过GNU实现中可用的方法。这是由于动态树结构造成的，这也使得有时很难理解。如果你已经读到这里，我相信你可以找到自己利用基于malloc的缓冲区溢出的方法。

## GNU C库实现
==========

GNU C库将应用程序请求的内存切片的信息保留在所谓的'chunks'中。它们如下所示（从malloc.c进行了适当的调整）：

```
             +----------------------------------+
    chunk -> | prev_size                        |
             +----------------------------------+
             | size                             |
             +----------------------------------+
      mem -> | data                             |
             : ...                              :
             +----------------------------------+
nextchunk -> | prev_size ...                    |
             :                                  :
```

其中，mem是你从malloc()获得的指针。所以如果你执行：

```
unsigned char *mem = malloc(16);
```

那么'mem'等于图中的指针，而(mem - 8)将等于'chunk'指针。

'prev_size'元素具有特殊功能：如果当前块之前的块未使用（被free'd），则它包含之前的块的长度。在另一种情况下 - 当前块之前的块已使用 - 'prev_size'是其'数据'的一部分，保存四个字节。

'size'字段有一个特殊的含义。正如你所预期的，它包含当前内存块的长度，数据部分的长度。在调用malloc()时，将其大小增加了四个字节，然后将其大小舍入到下一个双字边界。因此，malloc(7)将变为malloc(16)，malloc(20)将变为malloc(32)。对于malloc(0)，它将被填充为malloc(8)。这种行为的原因将在后面解释。

由于填充意味着较低的三位始终为零，不用于实际长度，它们可以以另一种方式使用。它们用于指示块的特殊属性。最低位，称为PREV_INUSE，指示前一个块是否使用。如果下一个块在使用中，则将其设置。次低位设置如果内存区域是mmap的 - 一种特殊情况，我们不会考虑。第三低位未使用。

为了测试当前块是否正在使用，必须检查下一个块的PREV_INUSE位，在其大小值中。

一旦我们使用free()释放了块，某些检查就会进行，并且内存被释放。如果其相邻块也是空闲的（使用PREV_INUSE标志进行检查），它们将合并在一起，以保持可重用块的数量较低，但其大小尽可能大。如果无法合并，则下一个块将带有清除的PREV_INUSE位，并且块会发生一些变化：

```
             +----------------------------------+
    chunk -> | prev_size                        |
             +----------------------------------+
             | size                             |
             +----------------------------------+
      mem -> | fd                               |
             +----------------------------------+
             | bk                               |
             +----------------------------------+
             | （旧内存，可以为零字节）          |
             :                                  :
nextchunk -> | prev_size ... | : |
```

可以看到，存在两个新值，原本存储在'data'的位置（在'mem'指针）。这两个值称为'fd'和'bk' - 前向和后向指针。它们指向一个未合并的自由内存块的双向链表。每次发出新的free，都将检查该列表，并可能合并未合并的块。内存会不时地进行碎片整理，以释放一些内存。

由于malloc的大小始终至少为8个字节，因此有足够的空间来容纳这两个指针。如果在'bck'指针之后保留了旧数据，直到再次分配内存之前，它将保持未使用。

与此管理有关的有趣事情是，整个内部信息都在带内部保留 - 这是一个明确的通道问题（就像字符串内部的格式化字符串命令一样，就像可破解的电话线中的控制通道一样，就像堆栈内存中的返回地址一样）。

由于如果我们可以溢出到malloc的区域，我们可以覆盖这些内部管理信息，因此我们应该看一下以后如何处理它。由于每个malloc的区域最终都会被free()，所以我们看一下free，它是对malloc.c中的chunk_free()的包装（稍微简化了一些，去掉了#ifdef）：

```
static void chunk_free(arena *ar_ptr, mchunkptr p)
{
  size_t     hd = p->size; /* its head field */
  size_t     sz;           /* its size */
  int        idx;          /* its bin index */
  mchunkptr  next;         /* next contiguous chunk */
  size_t     nextsz;       /* its size */
  size_t     prevsz;       /* size of previous contiguous chunk */
  mchunkptr  bck;          /* misc temp for linking */
  mchunkptr  fwd;          /* misc temp for linking */
  int        islr;         /* track whether merging with last_remainder */

  check_inuse_chunk(ar_ptr, p);

  sz = hd & ~PREV_INUSE;
  next = chunk_at_offset(p, sz);
  nextsz = chunksize(next);

  // ...

  if (next == top(ar_ptr)) /* merge with top */
  {
    sz += nextsz;

    if (!(hd & PREV_INUSE)) /* consolidate backward */
    {
      prevsz = p->prev_size;
      p = chunk_at_offset(p, -(long)prevsz);
      sz += prevsz;
      unlink(p, bck, fwd);
    }

    set_head(p, sz | PREV_INUSE);
    top(ar_ptr) = p;

    if ((unsigned long)(sz) >= (unsigned long)trim_threshold)
        main_trim(top_pad);
    return;
  }

  islr = 0;

  if (!(hd & PREV_INUSE)) /* consolidate backward */
  {
    prevsz = p->prev_size;
    p = chunk_at_offset(p, -(long)prevsz);
    sz += prevsz;

    if (p->fd == last_remainder(ar_ptr)) /* keep as last_remainder */
      islr = 1;
    else
      unlink(p, bck, fwd);
  }

  // ...

  if (!(inuse_bit_at_offset(next, nextsz))) /* consolidate forward */
  {
    sz += nextsz;

    if (!islr && next->fd == last_remainder(ar_ptr)) /* re-insert last_remainder */
    {
      islr = 1;
      link_last_remainder(ar_ptr, p);
    }
    else
      unlink(next, bck, fwd);

    next = chunk_at_offset(p, sz);
  }
  else
    set_head(next, nextsz); /* clear inuse bit */

  set_head(p, sz | PREV_INUSE);
  next->prev_size = sz;
  if (!islr)
    frontlink(ar_ptr, p, sz, idx, bck, fwd);
}
```

正如Solar Designer所展示的，我们可以使用unlink宏来覆盖任意内存位置。以下是如何做到的：

一个通常的缓冲区溢出情况可能如下：

```
mem = malloc(24);
gets(mem);
// ...
free(mem);
```

这样，malloc的块如下所示：

```
[ prev_size ] [ size P] [ 24 字节 ... ]（从现在开始的下一个块）
       [ prev_size ] [ size P] [ fd ] [ bk ] or [ data ... ]
```

你可以看到，下一个块直接与我们溢出的块相接。我们可以覆盖数据区域之后的任何内容，包括以下块的头部。

如果我们仔细观察chunk_free函数的结尾，我们会看到以下代码：

```
if (!(inuse_bit_at_offset(next, nextsz))) /* 向前合并 */
{
  sz += nextsz;

  if (!islr && next->fd == last_remainder(ar_ptr))
    /* 重新插入 last_remainder */
  {
    islr = 1;
    link_last_remainder(ar_ptr, p);
  }
  else
    unlink(next, bck, fwd);

  next = chunk_at_offset(p, sz);
}
```

inuse_bit_at_offset是在malloc.c开头定义的宏：

```
#define inuse_bit_at_offset(p, s)\
 (((mchunkptr)(((char*)(p)) + (s)))->size & PREV_INUSE)
```
由于我们控制了'next'块的头部，因此我们可以随意触发整个if块。内部的if语句不是很有趣，除非我们的块与最顶部的块相接。所以，如果我们选择触发外部的if语句，我们将调用unlink，它也是一个宏：

```
#define unlink(P, BK, FD)                                                \
{                                                                        \
  BK = P->bk;                                                            \
  FD = P->fd;                                                            \
  FD->bk = BK;                                                           \
  BK->fd = FD;                                                           \
}
```

unlink被传递一个指向自由块的指针，以及两个临时指针变量bck和fwd。它对'next'块头部执行以下操作：

```
*(next->fd + 12) = next->bk
*(next->bk + 8) = next->fd
```

尽管这两者没有交换，但是'fd'和'bk'指针指向其他块。这两个被指向的块被链接在一起，将当前块从表中删除。

所以，为了利用基于malloc的缓冲区溢出，我们必须在以下块的头部写入一个虚假的头部，然后等待我们的块被释放。

```
[缓冲区 ...] | [prev_size] [size] [fd] [bk]
```
其中，'|'是块边界。

我们设置的'prev_size'和'size'的值并不重要，但是要满足以下条件才能使其起作用：

'size'的最低有效位必须为零。
'prev_size'和'size'都应该能够被从内存中读取的指针相加，要么使用非常小的值，最多几千，要么 - 为了避免NUL字节 - 使用像0xfffffffc这样的大值。
你必须确保在(chunk_boundary + size + 4)处的最低位被清零（0xfffffffc将完全起作用）。
'fd'和'bk'可以这样设置（与Solar Designer的Netscape Exploit中使用的方法相同）：

```
fd = retloc - 12
bk = retaddr
```
但要注意，(retaddr + 8)将被写入，并且那里的内容将被破坏。你可以通过在retaddr处使用简单的'\xeb\x0c'来解决这个问题，这将跳过被破坏的内容，向前跳12个字节。

然而，无论如何，现在的利用方法都非常简单：

```
<跳转，2字节> <6字节> <4字节的虚假头部> <nop指令> <shellcode> |
\ff\ff\ff\fc \ff\ff\ff\fc <retloc - 12> <retaddr>
```

其中，'|'是块边界（从那一点开始溢出）。现在，接下来的两个负数只是为了在free()中存活一些检查，并且避免NUL字节。然后，我们正确编码了(retloc - 12)，然后是返回地址，它将返回到'jmp-ahead'。在'|'之前的缓冲区与任何x86 exploit相同，只是前12个字节不同，因为我们必须考虑到unlink宏的额外写操作。

Off-by-one / Off-by-five
甚至在只能溢出五个字节或特殊情况下只能溢出一个字节的情况下，我们仍然可以覆盖任意指针。当溢出五个字节时，内存布局必须如下所示：

```
[chunk a] [chunk b]
```

其中，chunk a在你的控制下且可溢出。chunk b已经作为溢出的发生而分配。通过覆盖chunk b的前五个字节，我们破坏了块头的'prev_size'元素和'size'元素的最低有效字节。现在，由于chunk b被free()，由于'size'的PREV_INUSE标志被清除（见下文），将发生向后合并。如果我们为'prev_size'提供一个小值，该值小于chunk a的大小，我们就可以创建一个虚假的块结构：

```
[chunk a ... fakechunk ...] [chunk b]
             |
             p 
```
chunk b的'prev_size'指针相对于虚假块是负的。通过这种设置，我们可以利用的代码已经被讨论过：

```
if (!(hd & PREV_INUSE)) /* 向后合并 */
{
  prevsz = p->prev_size;
  p = chunk_at_offset(p, -(long)prevsz);
  sz += prevsz;

  if (p->fd == last_remainder(ar_ptr)) /* 保留为 last_remainder */
    islr = 1;
  else
    unlink(p, bck, fwd);
}
```

其中，'hd'是chunk b的大小元素。当我们覆盖它时，我们清除了最低两位，因此清除了PREV_INUSE，并且匹配了if条件（实际上，NUL就足够了）。在接下来的几条指令中，原来指向chunk b的'p'指针被重定位到我们的虚假块上。然后调用了unlink宏，我们就可以像往常一样覆盖指针。我们现在使用向后合并，而在先前的描述中，我们使用了向前合并。这些是否有些混淆？当利用malloc溢出时，不必太担心细节，当你从更广泛的角度了解malloc函数时，它们会变得更加清晰。

要想详细了解和描述GNU C库中malloc实现的内容，可以查阅GNU C库参考手册[3]。它也对与malloc无关的内容提供了很好的阅读。



## 可能的障碍以及如何应对它们
==========

与任何新的利用技术一样，总会有人提出在他们头脑中或以malloc函数补丁的形式有“完美”解决问题的人。这些人 - 通常是那些从未亲自撰写过利用代码的人 - 被误导进入错误的安全感觉，我想就这些方法留下几句话，以及为什么它们很少奏效。

有三个基于主机的阶段，可以在其中阻止导致妥协的缓冲区溢出：

1. 漏洞/溢出阶段

   这是真正的溢出发生的地方，数据被覆盖。如果知道了这个地方，就可以在源代码级别修复问题。然而，大多数方法认为这个地方是未知的，因此问题还无法解决。

2. 激活阶段

   在溢出发生后，应用程序的部分数据被损坏。无论是堆栈帧、malloc管理记录还是缓冲区后面的静态数据，都无关紧要。进程仍在运行自己的代码路径，覆盖的数据仍然是被动的。这个阶段是溢出本身之后，执行控制被夺取之前的一切。这就是攻击者必须以某种方式通过的自然的、非人为引入的障碍。

3. 夺取阶段

   这是从控制从其原始执行路径被重定向之后的一切。这是执行nopspace和shellcode的阶段，没有真正的利用障碍。

现在谈谈保护系统。大多数“非执行堆栈”和“非执行堆”补丁试图捕捉从第二阶段到第三阶段的切换，即夺取执行控制的阶段，而一些专有系统则检查来自内核空间内部的系统调用的来源。它们并不禁止以这种方式运行代码，它们试图限制哪些代码可以运行。

那些允许你首先重定向执行的系统基本上是有缺陷的。它们试图以黑名单的方式限制利用，试图封堵你可能想要去的地方。但是，如果你可以在进程空间内执行合法的代码，几乎总是足以妥协整个进程。

现在是更具挑战性的保护措施，试图限制你在第二阶段的情况。其中包括 - 但不限于 - libsafe、StackGuard、FormatGuard以及任何基于编译器或库的补丁。它们通常需要重新编译或重新链接现有代码，以将安全“措施”插入到代码中。这包括金丝雀值、检查字节的障碍或重新排序，以及在执行可能是坏事之前进行广泛的检查。虽然在安全性方面进行合理性检查通常是一项良好的政策，但它无法修复之前破损的东西。每一种这样的保护措施都是建立在可能出现在你的程序中的某种错误情况的基础上，试图预测攻击者滥用该错误时的结果。它们设置陷阱，假设你将要触发或必须触发以利用漏洞。这是在你的控制还没有被激活之前完成的，因此你不能太多地影响它，除非选择输入数据。当然，这些保护措施比仅监视第三阶段的保护系统要严格得多，但仍然有方法可以绕过它们。过去已经讨论过一些方法，所以我不会在这里深入探讨。相反，我会简要地讨论一种我已经在地平线上看到的保护措施，类似于“MallocGuard”。

这种保护措施不会在很大程度上改变malloc管理块的机制，因为当前的代码已经证明是有效的。malloc函数在整个系统性能中扮演着关键角色，所以你不能在这里随意调整。这种保护措施只能引入一些额外的检查，它不能在每次调用malloc()时都验证全部一致性。而且这就是它的缺陷所在：一旦你控制了一个malloc块的信息，你就可以控制其他块。因为块是通过使用存储的指针（SysV）或存储的长度（GlibC）来“遍历”的，所以有可能“创建”新的块。由于在最坏情况下必须假设所有块都不一致，所以进行健全性检查时必须检查所有块。但这会消耗太多的性能，因此在保持良好性能的情况下很难检查malloc溢出。所以，将不会有“MallocGuard”，或者它将是一个毫无用处的保护措施，传统上是毫无用处的伪保护措施。正如一位朋友所说：“每一种保护措施都有一个反保护措施”。

## 致谢
==========

我要感谢所有的校对者和修正者。对于一些真正需要的修正，我要感谢MaXX，他在本期Phrack杂志中撰写了更详细的关于GNU C库malloc的文章，对他致以嘉奖！：）


## References 参考资料
==========

[1] Solar Designer,
    http://www.openwall.com/advisories/OW-002-netscape-jpeg.txt
[2] DD Sleator, RE Tarjan, "Self-Adjusting Binary Trees", 1985,
    http://www.acm.org/pubs/citations/journals/jacm/1985-32-3/p652-sleator/
    http://www.math.tau.ac.il/~haimk/adv-ds-2000/sleator-tarjan-splay.pdf
[3] The GNU C Library
    http://www.gnu.org/manual/glibc-2.2.3/html_node/libc_toc.html
[4] Solaris 8 Foundation Source Program
    http://www.sun.com/software/solaris/source/

|=[ EOF ]=---------------------------------------------------------------=|
