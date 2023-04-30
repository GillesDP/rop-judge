# Return Oriented Programming Voorbeeld
Stel dat een hacker een bufferoverloopexploit in het programma heeft gevonden om de controlestroom te kapen door het retouradres op de stapel te overschrijven met het begin van een ROP-keten. Hieronder staan ​​fragmenten uit het programma in kwestie.

Bouw een ROP-keten die de schadelijke functie `attack` aanroept, die geen argumenten vereist en `"ATTACKED!"` naar de console zal afdrukken.

```
000011c9 <attack>:
    11c9:	55                   	push   %ebp
    11ca:	89 e5                	mov    %esp,%ebp
    11cc:	53                   	push   %ebx
    11cd:	83 ec 04             	sub    $0x4,%esp
    11d0:	e8 3e 01 00 00       	call   1313 <__x86.get_pc_thunk.ax>
    11d5:	05 2b 2e 00 00       	add    $0x2e2b,%eax
    11da:	83 ec 0c             	sub    $0xc,%esp
    11dd:	8d 90 08 e0 ff ff    	lea    -0x1ff8(%eax),%edx
    11e3:	52                   	push   %edx
    11e4:	89 c3                	mov    %eax,%ebx
    11e6:	e8 45 fe ff ff       	call   1030 <printf@plt>
    11eb:	83 c4 10             	add    $0x10,%esp
    11ee:	b8 01 00 00 00       	mov    $0x1,%eax
    11f3:	8b 5d fc             	mov    -0x4(%ebp),%ebx
    11f6:	c9                   	leave  
    11f7:	c3                   	ret
```