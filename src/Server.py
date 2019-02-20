import socket
import sys
import os
import socketserver
import requests
from _thread import *

req_queue = 1
BUFFER_SIZE = 4096

class Server:

    def __init__(self,HOSTNAME,port,connection_queue):
        self.port = port
        server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOSTNAME,port))
        server_socket.listen(connection_queue)

        print("[*SERVER]Server is listening at", HOSTNAME +":"+ str(port),"\n")


        while(1):
            client_connection,client_addr = server_socket.accept()
            print('\n[*SERVER]Incoming connection from ' + client_addr[0] + ':' + str(client_addr[1]))
        #    start_new_thread(self.request_handler,(client_connection,client_addr))
            self.request_handler(client_connection,client_addr)

        server_socket.close()

    def request_handler(self, connection, addr):

        print("[*SERVER]Running handler code")

        data = connection.recv(BUFFER_SIZE)
        dataStr = data.decode()
        print("[*SERVER]Incoming message:\n", dataStr)

        dataParts = dataStr.splitlines()

        temp = dataParts[0]
        URL = temp[temp.find("http://")+7:temp.find("/ HTTP")]
        print("URL is", URL)
#        remote_host = dataStr[dataStr.find("Host: "):]
#        remote_host = remote_host[remote_host.find("www.")+4:remote_host.find("\n")]
#        print("host is:"+remote_host)


        remote_port=80
    #    remote_port = temp[temp.find(":")+1:temp.find(" HTTP")]
    #    print("port is",remote_port)

        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((URL,int(remote_port)))
        s.sendall(data)

        while(1):
            web_data = s.recv(4096)
    #        print("[*SERVER]Response from web: ",web_data.decode())
            #Send to client
            if(len(web_data) > 0):
                connection.send(web_data)
            else:
                break

        s.close()
    #    print("Host     :", incomingHost)
    #    connection.send(dataStr.encode())
