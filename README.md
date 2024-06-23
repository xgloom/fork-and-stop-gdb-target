# Fork and stop a GDB target

## Info
GDB script and (preloaded) library that enables a user to fork of a binary gdb 
target in a stopped/suspended state.

I did not find any reference online on how to do this, so I am sharing this
method. This can be useful if you want to interfer with the debugged program
without it affecting your original debugged session.  

## How
It instructs the loader to load an additional library that contains code to 
fork and raises a stop signal on x86-64. This uses `LD_PRELOAD` and this trick
works when you start a program (see usage below).

If you are attaching to a running process instead, you could generalise this by
calling `dlopen (3)` to first load the library at runtime and then jump to the
`inject` function defined in there as defined by the script. This should
require a minor modification, I have put a comment with info in `fork.py`.

In GDB, it contains commands to save the register that will be clobbered
during execution of that library to the stack and pop these after executing
the library code to ensure correct program state.

## Usage
```bash
# in this directory
make
gdb ./binary-target

# in gdb
source fork.py

# example usage (still in gdb)
b main
r

fork

# in shell (there should be two now)
pidof binary-target
```
