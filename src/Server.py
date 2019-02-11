import socket
import sys
import os
import socketserver
from _thread import *

req_queue = 5
HOSTNAME = "localhost"
BUFFER_SIZE = 4096

class Server:

    def __init__(self,port):
        self.port = port
        server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOSTNAME,port))
        server_socket.listen(5)

        print("[*SERVER]Server is listening at", HOSTNAME , port)

        while(1):
            connection,addr = server_socket.accept()

            print("[*SERVER]Incoming connection from", addr)

            start_new_thread(self.request_handler,(connection,addr))


    def request_handler(self, connection, client_addr):

        print("[*SERVER]Running handler code")

        data = connection.recv(BUFFER_SIZE)
    #    print("[*SERVER]Incoming message:", data.decode())

    #    print('received {!r}'.format(data)  )

        dataStr = data.decode().split('n')[0]
        url = dataStr.split('   ')[0]

        print(dataStr)
        print(url)

        http_position = url.find("://")

        if(http_position is -1):
            temp = url

        else:
            temp = url[(http_position+3):]

        port_position = temp.find(":")

        webserver_position = temp.find("/")

        if(webserver_position is -1):
            webserver_position=len(temp)

        webserver = ""
        port = -1


        if(port is -1 or webserver_position < port_position ):

            port = 443
            webserver = temp[:webserver_position]

        else:
            port = int((temp[(port_position+1):])[:webserver_position-1])
            webserver = temp[:port_position]


        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        sock.connect((webserver,port))
        sock.sendall(data)

        data = sock.recv(BUFFER_SIZE)

        connection.send(data)
