import gdb
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class ForkCommand(gdb.Command):
    def __init__(self):
        # LD_PRELOAD inject library that takes care of forking.
        inject_path = os.path.join(SCRIPT_DIR, 'inject.so')
        gdb.execute(f"set environment LD_PRELOAD={inject_path}");

        # if attaching to a running process, use dl_open instead of LD_PRELOAD.
        # gdb.execute(f'call (void*) dlopen("{inject_path}", 2)')
        
        super(ForkCommand, self).__init__("fork", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        # remove breakpoints to prevent fork crash; "jmp" to fork instructions.
        commands = ['d',
                    'set {long long}($rsp-0x8) = $rip',
                    'set {long long}($rsp-0x10) = $rdi',
                    'set {long long}($rsp-0x18) = $rsi',
                    'set {long long}($rsp-0x20) = $rax',
                    'set $rip = (uintptr_t)inject',
                    'c',
                    's',
                    's']

        for command in commands:
            gdb.execute(command, from_tty=False, to_string=True) 

ForkCommand()
