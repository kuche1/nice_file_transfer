

import os
import sys
import socket
import ssl



f= open('reciver_ip')
ip= f.read()
f.close()
port= 6789




for (d,folds,fils) in os.walk('to_send'):
	break

if len(fils) == 0:
	print('nothing to send')
	sys.exit(0)


s= ssl.wrap_socket(socket.socket(), server_side=False, do_handshake_on_connect=True,
	ssl_version=ssl.PROTOCOL_SSLv23
	)
try:
	s.connect((ip, port))
except ConnectionRefusedError:
	print('You buddy hasnt turned the reciver on')
	input('END')
	sys.exit(0)
except ConnectionResetError:
	print('Connection broke')
	input('END')
	sys.exit(0)

for fil in fils:
	s.sendall(b'1')

	print(f'Sending: {fil}')
	s.sendall( (fil+';').encode('utf-8') )
	fd= 'to_send\\'+fil
	s.sendall( (str( os.path.getsize(fd) )+';').encode('utf-8') )
	f= open(fd, 'rb')
	while 1:
		cont= f.read(10240)
		if cont:
			s.sendall(cont)
		else:
			f.close()
			break

s.sendall(b'0')
s.shutdown(0)
s.close()