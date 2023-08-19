struct malloc_chunk {
  INTERNAL_SIZE_T      mchunk_prev_size;  
  INTERNAL_SIZE_T      mchunk_size;  
  struct malloc_chunk* fd;         
  struct malloc_chunk* bk;
  ...
};
static void
_int_free (mstate av, mchunkptr p, int have_lock)
{
    ...
    /* consolidate backward */
    if (!prev_inuse(p)) {
      prevsize = prev_size (p);
      size += prevsize;
      p = chunk_at_offset(p, -((long) prevsize));
      unlink(av, p, bck, fwd);
    }
    ...
}
#define unlink(AV, P, BK, FD) { \
...
FD = P->fd;								      \
BK = P->bk;								      \
if (__builtin_expect (FD->bk != P || BK->fd != P, 0))		  \
  malloc_printerr ("corrupted double-linked list");			  \
else {								      \
    FD->bk = BK;							      \
    BK->fd = FD;							      \
    if (!in_smallbin_range (chunksize_nomask (P))			    \
        && __builtin_expect (P->fd_nextsize != NULL, 0)) {\
        ...
        if (FD->fd_nextsize == NULL) {				      \
            ...
        } else {							      \
          P->fd_nextsize->bk_nextsize = P->bk_nextsize;		 \
          P->bk_nextsize->fd_nextsize = P->fd_nextsize;		 \
            ...
}
