import socket
import sys
import os
import requests
import ssl
from _thread import *


BUFFER_SIZE = 8192000


class Server:

    HOSTNAME = "127.0.0.1"

    def __init__(self,port):
        connection_queue = 1000

        self.port = port
        server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr =(Server.HOSTNAME,int(port))
        server.bind(server_addr)
        server.listen(connection_queue)


        print("[*SERVER] Server is initialised and listening at",server_addr)

        while 1:
            incoming_connection, incoming_addr = server.accept()
        #    print("\n[*SERVER]Incoming request from",incoming_addr,"\n")
            data = incoming_connection.recv(BUFFER_SIZE)
            start_new_thread(self.string_extract,(incoming_connection,incoming_addr,data))
    #        self.string_extract(incoming_connection,incoming_addr,data.decode())

        s.close()

    def string_extract(self, connection, client_addr,data):

        data=data.decode()
    #    print(data)
    #    try:
        data_lines = data.split('\n')
        if("CONNECT" in data):
            print("\n", data)

            first_line = data_lines[0]
            url = first_line.split(' ')[1]

            host = url.split(':')[0]
            port = url.split(':')[1]
            print("url" ,url)

            self.https_proxy(data.encode(),connection,host,int(port))
        #    connection.close()
            return
        else:
            print(data)
            first_line = data_lines[0]


            url = first_line.split(' ')[1]
            #    print("url",url)

            http_position = url.find("://")

            if(http_position == -1):
                temp=url
            else:
                temp=url[(http_position+3):]


            port_pos = temp.find(":")
            webserver_pos =temp.find("/")



            if(webserver_pos == -1):
                webserver_pos=len(temp)


            webserver=""
            port = -1

            if(port_pos == -1 or webserver_pos < port_pos):
                port=80
                webserver=temp[:webserver_pos]
            else:
                port = int((temp[(port_pos+1):])[:webserver_pos-port_pos+1])
                webserver = temp[:port_pos]


            self.http_handler(webserver,port,connection,data,client_addr)
    #    except Exception as e:
    #        print(e)
    #        pass

    def http_handler(self,remote_webserver,remote_port,client_connection,data,client_addr):

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((remote_webserver,remote_port))
            sock.send(data.encode())

            while 1:
                response = sock.recv(BUFFER_SIZE)
                print("[*SERVER] Response from remote:")#, response)

                if(len(response) > 0):
                    client_connection.send(response)
                else:
                    break

            sock.close()

            client_connection.close()

        except socket.error:
            sock.close()
            client_connection.close()

    def https_proxy(self,data,client_connection, remote_webserver, remote_port):

        try:
        #    client_connection.send(data)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((remote_webserver,remote_port))
            #client_connection.sendall(data.encode())

            reply = "HTTP/1.0 200 Connection establish\r\n"
            reply+= "Proxy-agent: Pyx\r\n"
            reply+= "\r\n"
            client_connection.sendall( reply.encode() )
        except sock.error as err:
            pass

    #    sock.setblocking(0)
    #    client_connection.setblocking(0)
        while 1:
            request = client_connection.recv(BUFFER_SIZE)
            print("Request:")#, request)
            sock.sendall(request)


            reply = sock.recv(BUFFER_SIZE)
            print("Reply:")#, reply)
            client_connection.sendall( reply )
