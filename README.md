# rop-judge
This repository is meant to be used to built the Return Oriented Programming Judge for Dodona.

*Still in the discovery phase.* The idea is that the program will be given a string (separated by `\n`) representing the ROP chain. It will then execute the given stack and (hopefully) return unwanted behavior.

Use the following command to compile `attack.c`:
```bash
gcc -O0 -fno-pie -no-pie -m32 -fno-stack-protector attack.c
```
To see the address space, use:
```bash
objdump -d a.out
```
To run the program use:
```bash
./a.out 
```
