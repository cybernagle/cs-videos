bpf = r'''
int hello(void *ctx) {
    bpf_trace_printk("I'm BPF Program!");
    return 0;
}'''
