section .text
    global inject

; forks and suspends both processes.
inject:
    ; fork 
    mov rax, 57
    syscall

    ; comment these two lines out if you only want to suspend child.
    ; test rax, rax
    ; jnz restore

suspend:
    ; getpid.
    mov rax, 39
    syscall

    ; kill self with SIGSTOP.
    mov rdi, rax
    mov rax, 62
    mov rsi, 19
    syscall

restore:
    ; unconventional stack usage:
    ; ret. addr. at rsp-0x8.
    ; rdi at rsp-0x10.
    ; rsi at rsp-0x18
    ; rax at rsp-0x20.
    sub rsp, 0x20
    pop rax
    pop rsi
    pop rdi
    ret
