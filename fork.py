import gdb
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class ForkCommand(gdb.Command):
    def __init__(self):
        self.inject_path = os.path.join(SCRIPT_DIR, 'inject.so')

        # one could use LD_PRELOAD at loadtime by uncommenting the next line. 
        # gdb.execute(f"set environment LD_PRELOAD={self.inject_path}");

        super(ForkCommand, self).__init__("fork", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        if (not (gdb.selected_inferior().pid == 0)):
            # use dlopen (3) to dynamically link at runtime (requires libc).
            gdb.execute(f'call (void*) dlopen("{self.inject_path}", 2)',
                        from_tty=False, to_string=False)

            # remove breakpoints to prevent fork crash; "jmp" to fork.
            # steps through the 7 instructions in assembly "restore"-label. 
            commands = ['d',
                        'set {long long}($rsp-0x8) = $rip',
                        'set {long long}($rsp-0x10) = $rdi',
                        'set {long long}($rsp-0x18) = $rsi',
                        'set {long long}($rsp-0x20) = $rax',
                        'set {long long}($rsp-0x28) = $rcx',
                        'set {long long}($rsp-0x30) = $r11',
                        'set $rip = (uintptr_t)inject',
                        'c',
                        'si 7',
                        'si 7']

            for command in commands:
                gdb.execute(command, from_tty=False, to_string=False)
            gdb.write("Target program should be forked.\n")
        else:
            raise gdb.GdbError("Target program is not running, can't fork.")

ForkCommand()
