import gdb
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def init():
    inject_path = os.path.join(SCRIPT_DIR, 'inject.so')
    gdb.execute(f"set environment LD_PRELOAD={inject_path}");

class ForkCommand(gdb.Command):
    def __init__(self):
        super(ForkCommand, self).__init__("fork", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        # Save addresses to negative stack.
        current_rip = gdb.parse_and_eval("$rip")

        # Remove breakpoints so that fork will continue.
        gdb.execute('d')
        gdb.execute('set {long long}($rsp-0x8) = $rip')
        gdb.execute('set {long long}($rsp-0x10) = $rdi')
        gdb.execute('set {long long}($rsp-0x18) = $rsi')
        gdb.execute('set {long long}($rsp-0x20) = $rax')

        # "jmp" to injected library to fork off a suspended child.
        gdb.execute('set $rip = (uintptr_t)inject')
        gdb.execute('c')
        gdb.execute('s')
        gdb.execute('s')


init()
ForkCommand()
