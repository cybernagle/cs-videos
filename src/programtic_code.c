unsigned long long *chunk1, *chunk2;

// First grab two chunks (non fast)
chunk1 = malloc(0x80);        // Points to 0xa0e010
chunk2 = malloc(0x80);        // Points to 0xa0e0a0

free(chunk2);

chunk1[3] = (unsigned long long)data;

strcpy(data, "Victim's data");
