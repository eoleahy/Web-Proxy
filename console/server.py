import os
import sys
import socket
import ssl
from _thread import *

BUFFER_SIZE = 819200

class Server:
    """Main class that implements the actual proxy"""
    HOSTNAME = "127.0.0.1"
    connection_queue = 100
    blocklist=""

    def __init__(self,port,blockFileStr):
        """
        Constructor for the server. Creates the server socket and starts
        listening for incoming connections. Creates a new thread for incoming
        connections.

        @param port: Integer of the port the server is listening atself.
        @param blockFileStr: a string for the address of the blocklist
        """
        Server.blocklist=blockFileStr

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_addr=(Server.HOSTNAME,port)
        server.bind(server_addr)

        print("[*SERVER]Proxy is initialised and listening at",server_addr)
        server.listen(Server.connection_queue)

        #Listening loop for server
        while 1:

            #Accept the incoming connection
            (connection, client_addr) = server.accept()
        #    print("[*Server]Incoming connection from",client_addr,"\n")
            start_new_thread(self.request_handler, (connection, client_addr))

    def request_handler(self,connection, client_addr):
        """
        Parses the details of the incoming connection. Finds the host and port
        of the website the client is trying to connect to.

        @param connection: the connection to the client
        @param client_addr: address of the client
        """

        data = connection.recv(BUFFER_SIZE)

        #byte -> string
        try:
            data = data.decode("utf-8")
            #print(data)

            #This is the line that typically has the CONNECT www.website.com:443
            first_line = data.split("\n")[0]
            url = first_line.split(" ")[1]
            webserver = ""
            remote_port = ""
            reqType = first_line.split(" ")[0]

            #Finding web details for HTTP CONNECT
            if(reqType == "CONNECT"):
                webserver = url.split(':')[0]
                remote_port = url.split(':')[1]
            #For other types of requests (GET/POST)
            else:

                http_pos = url.find("://") # find pos of ://

                if(http_pos==-1):
                    temp = url
                else:
                    temp = url[(http_pos+3):] # get the rest of url

                # find the port pos (if any)
                port_pos = temp.find(":")
                # find end of web server
                webserver_pos = temp.find("/")
                if(webserver_pos == -1):
                    webserver_pos = len(temp)

                remote_port = -1
                #if it has no specified port default to 80
                if(port_pos==-1 or webserver_pos < port_pos):
                    remote_port = 80
                    webserver = temp[:webserver_pos]

                else: # specific port
                    remote_port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
                    webserver = temp[:port_pos]

            # check the blocklist for the host
            if(self.checkBlockList(webserver) == 1):
                connection.close()
                return

            if(reqType != ""):
                print("[*SERVER] REQUEST:[",reqType,webserver,"]")

            self.https_proxy(reqType,webserver,remote_port,connection,data)

        except OSError:
            pass
        except TypeError:
            pass
        except IndexError:
            pass
        except UnicodeDecodeError:
            pass

    def https_proxy(self,reqType,webserver,port,client_connection,data):
        """
        Main functionality of the proxy, opens up a socket to connect to webserver.
        If the connection type is CONNECT it will send the 200 code and set up a
        connection between the client and webserver.
        It then opens an unblocked stream from webserver to proxy to client &
        vice-versa.
        @param reqType: Type of request
        @param webserver: Host of the webserver
        @param port: Port of the webserver
        @param client_connection: Connection to client
        @param data: data from client
        """

        #--- The below code is for the communication from client to proxy to browser ---

        #Create a socket for connecting to web
        try:
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((webserver, int(port)))

            if(reqType == "CONNECT"):
                #HTTP CONNECT reply
                head = "HTTP/1.0 200 Connection established\r\n"
                agent = "Proxy-agent: web-proxy\r\n"
                reply = head + agent +  "\r\n"
                client_connection.sendall( reply.encode() )

            elif(reqType == 'GET'):
                #we can just send off the data from client for GET
                remote_socket.sendall(data.encode())

            #No blocking on socket to prevent hanging state
            client_connection.setblocking(False)
            remote_socket.setblocking(False)

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
                    client_connection.sendall( reply_from_web )
                except socket.error as err:
                    pass
        except OSError:
            pass
    def checkBlockList(self,host):
        """
        Checks to see if website trying to connect to in in the blocklist.
        Reads in from blocklist file. Must be in the form www.website.com.

        @param host: Host of the site proxy is trying to connect to.
        @returns: 1 if host is blocked
                  0 if host is unblocked
        """
        f = open(Server.blocklist, "r")

        if(len(host)<=1):
            f.close()
            return 0
        for line in f:
            if(host in line):
                print("[*SERVER] Attempted access to banned url:",line)
                f.close()
                return 1

        f.close()
        return 0
