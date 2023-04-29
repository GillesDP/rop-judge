# Return Oriented Programming Voorbeeld
Stel dat een hacker een bufferoverloopexploit in het programma heeft gevonden om de controlestroom te kapen door het retouradres op de stapel te overschrijven met het begin van een ROP-keten. Hieronder staan ​​fragmenten uit het programma in kwestie.

Bouw een ROP-keten die de schadelijke functie `attack` aanroept, die geen argumenten vereist en `"ATTACKED!"` naar de console zal afdrukken.

```
000011cd <attack>:
    11cd:	55                   	push   %ebp
    11ce:	89 e5                	mov    %esp,%ebp
    11d0:	53                   	push   %ebx
    11d1:	83 ec 04             	sub    $0x4,%esp
    11d4:	e8 28 01 00 00       	call   1301 <__x86.get_pc_thunk.ax>
    11d9:	05 ef 2d 00 00       	add    $0x2def,%eax
    11de:	83 ec 0c             	sub    $0xc,%esp
    11e1:	8d 90 40 e0 ff ff    	lea    -0x1fc0(%eax),%edx
    11e7:	52                   	push   %edx
    11e8:	89 c3                	mov    %eax,%ebx
    11ea:	e8 71 fe ff ff       	call   1060 <puts@plt>
    11ef:	83 c4 10             	add    $0x10,%esp
    11f2:	b8 01 00 00 00       	mov    $0x1,%eax
    11f7:	8b 5d fc             	mov    -0x4(%ebp),%ebx
    11fa:	c9                   	leave  
    11fb:	c3                   	ret   
```