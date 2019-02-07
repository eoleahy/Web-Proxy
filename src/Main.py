import socket
import sys
import os
from _thread import *


serverPort = 8001
blockedUrls = set({})
connSize = 50
BUFFER_SIZE = 4096
blockFileStr = "src/blocklist.txt"


def main():
    f = open(blockFileStr, "r")

    for line in f:
        blockedUrls.add(line)

    f.close()

    while(1):

        inputOp = input("Enter 'a' to set up a connection or 'o' for options or 'q' to quit:")

        if(inputOp is 'q'):
            exit()

        elif(inputOp is 'o'):
            display_Options()

        elif(inputOp is 'a'):
            start()


def start():

    HOSTNAME = 'localhost'
    port = input("Enter Port (80 is recommended) or type 'q' to return:")
    if(port is 'q'):
        return

    else:
        try:
            port = int(port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((HOSTNAME, port))
            print("[*]Socket created...")

            sock.listen(connSize)
            print("[*]Socket listening on [" +
                  HOSTNAME + ":" + str(port) + ']...')


            while(1):
                print("here")
                (connection,client_addr) = sock.accept()
                _thread.start_new_thread(request_handler, (connection,client_addr))

            sock.close()

        except (OSError, socket.error):
            print("Port is in use")
        except (ValueError, TypeError):
            print("Incorrect")

def request_handler(connection, client_addr):
    print("here")
    data = connection.recv(BUFFER_SIZE)

    dataStr = data.split('n')[0]
    url = dataStr.split('   ')[1]

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



def display_Options():

    while(1):
        print(" 'v' -view or edit url blocklist\n",
              "'q' -quit\n",
              "'c' -return\n")

        inp = input("Type command:")

        # Opens file in text editor
        if(inp is 'v'):
            os.system('notepad.exe ' + blockFileStr)
            f = open(blockFileStr, "r")

            # Clear url set and readd as file is updated
            blockedUrls.clear()

            for line in f:
                blockedUrls.add(line)

            f.close()

        elif(inp is 'q'):
            exit()

        elif(inp is 'c'):
            return


if __name__ == '__main__':
    main()
