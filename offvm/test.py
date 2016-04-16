
import socket
import time

sock = None

def host_connect_chardev():
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	#sock.sun_family = socket.AF_UNIX
	#sock.family = socket.AF_UNIX
	conn = '/var/lib/libvirt/qemu/channels/com.massclouds.cclassroom.0'
	
	sock.connect(conn)
 	time.sleep(1)
  	sock.send('1048x768x')
  	print sock.recv(1024)
	sock.close() 



if __name__ == '__main__':
   host_connect_chardev()
