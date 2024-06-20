# Fork and stop a GDB target

GDB script and (preloaded) library that enables a user to fork of a binary gdb 
target in a suspended state.

I did not find any reference online on how to do this online, so I am sharing
this method. 

# Usage
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
