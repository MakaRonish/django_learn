import socket

mysock= socket.socket(socket.AF_INET,socket.SOCK_STREAM) #make a phone
mysock.connect(('data.pr4e.org',80)) #dial the phone to doman name and port 80 if mistake is made or server not exist this connect is blow up
cmd='GET http://data.pr4e.org/page1.htm HTTP/1.0\r\n\r\n'.encode() #one we get here it means send command Get url protocol return and new line twice for not headers encode is compressed
mysock.send(cmd)

#receive data until socket ends
while True:
    data=mysock.recv(512)
    if len(data)<1:
        break
    print(data.decode(),end='')
mysock.close()
#closing our end of socket / end call
