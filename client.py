import socket
import time
import datetime
import logging
import errno

logging.basicConfig(filename='client.log',level=logging.INFO, format='%(message)s')

host = socket.gethostname() 
serverAddress = '127.0.0.1'
serverPort = 12349

try:
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
	print("Socket error: ",e)

try:
	clientSocket.connect((serverAddress, serverPort)) 
	print('Successfully connected')
except socket.error as e:
	print("Connection error: ",e)

quit=False
valid=False
while quit==False:
	while valid==False:
		sentence = input('Enter artist to find:\n')
		if sentence!="":
			valid = True
	valid=False
	t1 = datetime.datetime.now()
	clientSocket.sendall(sentence.encode())
	print('Message sent, waiting for responses')
	modifiedSentence = clientSocket.recv(1024)
	print ('From Server: ', modifiedSentence.decode())
	time.sleep(0.000001)
	t2 = datetime.datetime.now()
	t=t2-t1
	logging.info("It took " + str(t) + " ms to receive a response from the server for the request to get songs for " + sentence)
	logging.info("The response length is: "+ str(len(modifiedSentence)))
	logging.info("Server response received on: " + t2.strftime('%m/%d/%Y %H:%M:%S'))
	answer=input("Do you wish to disconnect from server? Type 'quit' if so\n")
	clientSocket.sendall(answer.lower().encode())
	if answer.lower()=="quit":
		quit=True
	else:
		print("Quit option not selected, connection still running")
print("Disconnected from server! Connection closed.")
clientSocket.close()