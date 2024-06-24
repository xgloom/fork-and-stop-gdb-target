# Fork and stop a GDB target

## Info
GDB script and (preloaded) library that enables a user to fork of a binary gdb 
target in a stopped/suspended state.

I did not find any reference online on how to do this, so I am sharing this
method. This can be useful if you want to interfer with the debugged program
without it affecting your original debugged session.  

## How
It instructs the loader to load an additional library that contains code to 
fork and raises a stop signal on x86-64. 

This uses `dlopen (3)` to load the library at runtime, which depends on libc
being present. Loading this library at runtime allows attaching to a running
process and still fork it. Alternatively, one could use `LD_PRELOAD` at load-
time- see comment in script to use this.

In GDB, it contains commands to save the register that will be clobbered
during execution of that library to the stack and pop these after executing
the library code to ensure correct program state.

## Usage
I have tested this using version: GNU gdb (Debian 13.1-3) 13.1.

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

