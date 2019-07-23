
import socket
import ssl
import os


port= 6789



s= ssl.wrap_socket(socket.socket(), server_side=True, do_handshake_on_connect=True,
	keyfile='certificate\\private.key',
	certfile='certificate\\selfsigned.crt',
	ssl_version=ssl.PROTOCOL_SSLv23,
	)
s.bind(('', port))
s.listen(1)
print('ready')

while 1:
	con, (ip,_)= s.accept()
	print()
	print(f'Connction from: {ip}')

	while 1:
		doing_it= con.recv(1)
		if doing_it==b'0':
			print('File transfer complete')
			break
		elif doing_it==b'1':
			pass
		else:
			print('DOING_IT ERROR')
			input('END')
			sys.exit(1)

		f_name= ''
		while 1:
			byte= con.recv(1).decode('utf-8')
			if byte==';':
				break
			f_name += byte
		print('Reciving file: '+f_name)

		size= ''
		while 1:
			byte= con.recv(1).decode('utf-8')
			if byte==';':
				break
			size+= byte
		print(f'File size: {size} bytes')
		size= int(size)

		f_dir= 'recived\\'+f_name
		while 1:
			if os.path.isfile(f_dir):
				f_name= 'new_'+f_name
				f_dir= 'recived\\'+f_name

				print('File already exists, renaming recived file to: '+f_name)
			else:
				break

		f= open(f_dir, 'wb')
		while size:
			recived= con.recv(size)
			f.write(recived)
			size-= len(recived)
		f.close()
		print('File recived')