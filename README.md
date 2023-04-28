# Return Oriented Programming Judge
This repository was made to allow educators to create Return Oriented Programming exercises for Dodona. Please note, this judge has a very specific application which may not suit your needs. Students will be given a set of assembly instructions with their associated (position-independent) addresses and will be prompted the question: 

> Suppose a hacker has found a buffer overflow exploit in the program to hijack control flow by overwriting the return address on the stack with the start of a ROP chain. Build the ROP chain that invokes a (possibly) malicious function.

The submission is a plain-text file where each line represents a stack slot (hexadecimal values). We assume the stack grows to lower addresses, hence the first line of the submission (the return address) has a lower address than the bottom line of the submission. An example of a submission is given below. 

```
0x01104
0x02

0x02340
0x08
0x01560


0x01000
```

The first element on the ROP chain is `0x01104`, this value will be written at the original return address, starting the attack (or ROP execution). Note that empty slots or represented with empty lines.

## Development
> **Note:** This judge is still in development. 

Currently building a program `attack.c` that's given a string of stack slots (with separator `|`) representing the ROP chain. Each substring (separated by `|`) is assumed to be a hexadecimal value. The program will then execute the given ROP chain.

Use the following command to compile `attack.c` (for x86, 32-bit). Note that we allow **position-independent executables** (PIE). The addresses given in the ROP chain are hence relative, they'll be offset by the actual address where the binary is loaded.
```bash
gcc -O0 -m32 -fno-stack-protector attack.c
```
To see the address space of the output program, use `objdump`.
```bash
objdump -d a.out
```
### Example
A simple example of this program in use. Suppose our program has the following code we would like to execute with a ROP chain (obtained using `objdump`). This particular function `do_something` will just print `"ATTACKED!"` to the console.
```
00001266 <do_something>:
    1266:	55                   	push   %ebp
    1267:	89 e5                	mov    %esp,%ebp
    1269:	53                   	push   %ebx
    126a:	83 ec 04             	sub    $0x4,%esp
    126d:	e8 2a 02 00 00       	call   149c <__x86.get_pc_thunk.ax>
    1272:	05 4e 2d 00 00       	add    $0x2d4e,%eax
    1277:	83 ec 0c             	sub    $0xc,%esp
    127a:	8d 90 48 e0 ff ff    	lea    -0x1fb8(%eax),%edx
    1280:	52                   	push   %edx
    1281:	89 c3                	mov    %eax,%ebx
    1283:	e8 e8 fd ff ff       	call   1070 <puts@plt>
    1288:	83 c4 10             	add    $0x10,%esp
    128b:	b8 01 00 00 00       	mov    $0x1,%eax
    1290:	8b 5d fc             	mov    -0x4(%ebp),%ebx
    1293:	c9                   	leave  
    1294:	c3                   	ret
```
Our ROP chain is very simple, as no actual arguments need to be passed. For the sake of demonstration, we'll just add additional elements (that are not actually needed) to the stack.
```bash
./a.out "0x1266|0x2|0x1000"
```
This indeed, will output:
```bash
ATTACKED!
```

