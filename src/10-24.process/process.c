enum procstate {
  UNUSED,
  EMBRYO,
  SLEEPING,
  RUNNABLE,
  RUNNING,
  ZOMBIE
};
struct context {
  uint edi;
  uint esi;
  uint ebx;
  uint ebp;
  uint eip;
};
struct proc {
  enum procstate state;
  uint sz;
  int pid;
  pde_t* pgdir;
  struct context *context;
  struct trapframe *tf;
  char *kstack;
  struct file *ofile[NOFILE];
  struct inode *cwd;
  struct proc *parent;
  void *chan;
  int killed;
};
