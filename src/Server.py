import os
import sys
import socket
import ssl
from _thread import *

BUFFER_SIZE = 819200

class Server:

    HOSTNAME = "127.0.0.1"
    connection_queue = 100
    blocklist=""

    def __init__(self,port,blockFileStr):

        Server.blocklist=blockFileStr

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_addr=(Server.HOSTNAME,port)
        server.bind(server_addr)

        print("[*SERVER]Proxy is initialised and listening at",server_addr)
        server.listen(Server.connection_queue)

        #Listening loop for server
        while 1:

            # Establish the connection
            (connection, client_addr) = server.accept()
        #    print("[*Server]Incoming connection from",client_addr,"\n")
            start_new_thread(self.https_proxy, (connection, client_addr))

    def https_proxy(self,client_connection, client_addr):

        data = client_connection.recv(BUFFER_SIZE)

        #byte -> string
        try:
            data = data.decode("utf-8")
        except UnicodeDecodeError:
            pass

        #print(data)

        #This is the line that typically has the CONNECT www.website.com:443
        first_line=""

        try:
            first_line = data.split("\n")[0]

        except TypeError:
            pass

        # get details
        url =""

        try:
            url = first_line.split(" ")[1]
        except IndexError:
            pass

        webserver = ""
        port = ""

        reqType = first_line.split(" ")[0]

        #Finding web details for HTTP CONNECT
        if(reqType is "CONNECT"):

            webserver = url.split(':')[0]
            port = url.split(':')[1]


        #For other types of requests (GET/POST)
        else:

            http_pos = url.find("://") # find pos of ://

            if(http_pos==-1):
                temp = url
            else:
                temp = url[(http_pos+3):] # get the rest of url

            port_pos = temp.find(":") # find the port pos (if any)


            # find end of web server
            webserver_pos = temp.find("/")
            if(webserver_pos == -1):
                webserver_pos = len(temp)

            webserver = "localhost"
            port = -1
            if(port_pos==-1 or webserver_pos < port_pos):

                # default port
                port = 80
                webserver = temp[:webserver_pos]

            else: # specific port
                port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
                webserver = temp[:port_pos]

        if(self.checkBlockList(webserver) is 1):
            client_connection.close()
            return

        if(reqType is not ""):
            print("[*SERVER] REQUEST:[",reqType,webserver,"]")


        #--- The below code is for the communication from client to proxy to browser ---

        #Create a socket for connecting to web
        try:
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((webserver, port))
        except OSError:
            pass

        if(reqType == "CONNECT"):
            #HTTP CONNECT reply
            reply = "HTTP/1.0 200 Connection established\r\n"
            reply += "Proxy-agent: Pyx\r\n"
            reply += "\r\n"
            client_connection.sendall( reply.encode() )

        elif(reqType == 'GET'):
            #we can just send off the data from client for GET
            try:
                remote_socket.sendall(data.encode())
            except OSError:
                pass
        #Set up an I0 stream
        try:
            client_connection.setblocking(0)
            remote_socket.setblocking(0)
        except OSError:
            pass

        #Two way communication streams
        while 1:
            #client -> proxy -> web
            try:
                request_from_client = client_connection.recv(BUFFER_SIZE)
                remote_socket.sendall( request_from_client )
            except socket.error as err:
                pass
            #web -> proxy -> client
            try:
                reply_from_web = remote_socket.recv(BUFFER_SIZE)
                print(reply_from_web)
                client_connection.sendall( reply_from_web )
            except socket.error as err:
                pass

    def checkBlockList(self,host):

        f = open(Server.blocklist, "r")
    #    print("HOST:",host)
        if(len(host)<=1):
            f.close()
            return 0
        for line in f:
            #print("line:",line)
            #print("HOST: %s LINE: %s" % (host, line))
            if(host in line):
                print("[*SERVER] Attempted access to banned url:",line)
                f.close()
                return 1

        f.close()
        return 0
