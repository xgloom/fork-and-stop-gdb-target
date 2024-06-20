CC = gcc
CFLAGS = -shared -fPIC
LDFLAG = -ldl 

all: inject.so

inject.so: inject.asm
	nasm -f elf64 inject.asm -o inject.o
	$(CC) $(CFLAGS) -o inject.so inject.o $(LDFLAG)

clean:
	rm -f inject.so 
