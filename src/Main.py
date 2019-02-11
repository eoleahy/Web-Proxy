import socket
import sys
import os
import socketserver
import time
from Server import Server
from _thread import *



HOSTNAME = 'localhost'
server_port = 8001
server_addr = (HOSTNAME, server_port)
blockedUrls = set({})
connSize = 50
BUFFER_SIZE = 4096
blockFileStr = "src/blocklist.txt"


def main():
    f = open(blockFileStr, "r")

    for line in f:
        blockedUrls.add(line)

    f.close()

    start_new_thread(Server,(server_port,))
    #proxy_server = Server(8001)

    time.sleep(2)

    while(1):

        inputOp = input("Enter 'a' to set up a connection or 'o' for options or 'q' to quit:\n")

        if(inputOp is 'q'):
            exit()

        elif(inputOp is 'o'):
            display_Options()

        elif(inputOp is 'a'):
            start()


def start():

    port = input("Enter Port (80 is recommended) or type 'q' to return:")
    if(port is 'q'):
        return

    else:
        try:
            port = int(port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_addr = (HOSTNAME,port)
            sock.bind(sock_addr)
            print("[*CLIENT]Socket created at ", sock_addr)
            sock.connect(server_addr)
            print("[*CLIENT]Socket created a connected to ", server_addr)

    #        while(1):
    #            start_new_thread(request_handler, (connection,client_addr))


            sock.close()

        except (OSError, socket.error):
            print("Port is in use")
        except (ValueError, TypeError):
            print("Incorrect")



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
