file=open("100worst.txt","r")
filearray=file.readlines()

#delete lines that do not contain song names
for i in range (6):
	del filearray[0]
for i in range (23):
	del filearray[len(filearray)-1]
	
#deal with songs that are written across 2 lines
for i in range (len(filearray)) :
	filearray[i]=filearray[i].strip()
	if filearray[i]!="":
		if filearray[i][len(filearray[i])-1].isdigit()==False:
			filearray[i]=filearray[i]+ " " +filearray[i+1]
			filearray[i+1]=""
i=0
while i<len(filearray):
	if filearray[i]=="":
		del filearray[i]
		i-=1
	i+=1
#get rid of song IDs
for i in range (len(filearray)-1) :
	filearray[i]=filearray[i].split("- ")[1]
filearray[99]=filearray[99].split("-")[1]

#alter song number 75 
filearray[74]=filearray[74].replace("19","1-9",1)

#keep only song name and artist
for i in range (len(filearray)):
	filearray[i]=filearray[i].split("19")[0]
	filearray[i]=filearray[i].rstrip()

#alter song number 75 back
filearray[74]=filearray[74].replace("1-9","19",1)

#alter song number 21 in the file so that it has same structure as other songs
filearray[20]=filearray[20].replace("-","  ")

def addSong(song,artist):
	if artist.lower() in song_dict:
		song_dict[artist.lower()].append(song)
	else:
		song_dict[artist.lower()]=[song]
		
#save the songs and artist in a dictionary
song_dict = {}
for i in range(len(filearray)):

	a=filearray[i].split("  ", 1)[0].strip()
	b=filearray[i].split("  ", 1)[1].strip()

	if "/" in b:
		b=b.split("/",1)
		addSong(a,b[0])
		addSong(a,b[1])
	else:
		addSong(a,b)

def returnSongs(artist_name):
	v=""
	for k,v in song_dict.items():
		if artist_name.lower() == k.lower():
			return v



import socket
import logging 
import time
import datetime
import logging
import errno

logging.basicConfig(filename='server.log',level=logging.INFO, format='%(message)s')

# get local machine name
host = socket.gethostname()    
serverAddress = '127.0.0.1'
serverPort = 12349
try:
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#This allows the address/port to be reused immediately instead of it being stuck in the TIME_WAIT state for several minutes, waiting for late packets to arrive
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error as e:
	print("Connection error: ",e)
	logging.info("Oops, something went wrong! Connection unsuccessful")


try:
	serverSocket.bind((serverAddress,serverPort))
	logging.info("Connection successful")
except socket.error as e:
    if e.errno == errno.EADDRINUSE:
        print("Port is already in use")
    else:
        # some other error raised the socket.error exception
        print(e)


serverSocket.listen(1)
t1 = datetime.datetime.now()
logging.info("The server has started at "+ t1.strftime('%m/%d/%Y %H:%M:%S'))
print ('The server is ready to receive')
try:
	connectionSocket, addr = serverSocket.accept()
except socket.error as e:
	print("Connection error: ",e)

t2 = datetime.datetime.now()
keepRunning=True
while True & keepRunning:
	
	try:
		receivedArtist = connectionSocket.recv(1024).decode()
	except socket.error as e:
		print("Error whilst receiving request ",e)
	treceived=datetime.datetime.now()
	logging.info("The server has received client request at "+ treceived.strftime('%m/%d/%Y %H:%M:%S'))
	print('server received:',receivedArtist)
	logging.info("Artist name received: " + receivedArtist)
	fullString="The server received the request successfully and here's what it found: \n"
	if returnSongs(receivedArtist)!=None:
		fullString=fullString + ", ".join(returnSongs(receivedArtist))
	else:
		fullString="no songs associated with artist: " + receivedArtist
	print(fullString)
	connectionSocket.sendall(fullString.encode())
	answerReceived=connectionSocket.recv(1024).decode()
	print(answerReceived=="quit")
	if answerReceived=="quit":
		t3=datetime.datetime.now()
		t=t3-t2
		keepRunning=False
	else:
		print("Socket connection still running")
logging.info("The server was connected to the client for: " + str(t))
connectionSocket.shutdown(socket.SHUT_RDWR)
connectionSocket.close()
print("Connection closed")