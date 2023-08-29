from pwn import *
i=process(['YoS','./level3'], env={'CSeC' : 'Awesome'})
print(i.recvline())
