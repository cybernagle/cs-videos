0000000000400880 <_IO_getc@plt>:
  jmpq   *0x2019da(%rip)        # 602260 <_GLOBAL_OFFSET_TABLE_+0x70>
  pushq  $0xb
  jmpq   4007c0 <_init+0x10>
0000000000400cb0 <Gets>:
  push   %r14
  ...
  callq  400880 <_IO_getc@plt>
  jmpq   400ce0 <Gets+0x30>
  nop
0000000000400da0 <getbuf>:
  push   %rbp
  mov    %rsp,%rbp
  sub    $0x30,%rsp
  lea    -0x30(%rbp),%rdi
  callq  400cb0 <Gets>
  ...
  retq   
  nopl   0x0(%rax,%rax,1)
0000000000400ed0 <test>:
  push   %rbp
  mov    $0xdeadbeef,%ecx
  xor    %eax,%eax
  mov    %rsp,%rbp
  push   %rbx
  sub    $0x18,%rsp
  ...
  callq  400da0 <getbuf>
  ...
  retq   
0000000000400f80 <launch.isra.1>:
  push   %rbp
  mov    $0xf4,%esi
  mov    %rsp,%rbp
  sub    $0x40,%rsp
  lea    -0x40(%rbp),%rax
  ...
  callq  400ed0 <test>
  ...
  jmp    400fd6 <launch.isra.1+0x56>
  ...
00000000004008f0 <main>:
  ... 
  callq  400f80 <launch.isra.1>
  ...
