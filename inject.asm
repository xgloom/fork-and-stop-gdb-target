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
    ; stored clobbered values on stack.
    ; ret. addr. at rsp-0x8.
    sub rsp, 0x30
    pop r11
    pop rcx
    pop rax
    pop rsi
    pop rdi
    ret

