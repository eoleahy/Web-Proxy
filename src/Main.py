import socket
import sys
import os
import socketserver
import time
from Server import Server
from _thread import *



HOSTNAME = "127.0.0.1"
server_port = 8001
blockedUrls = set({})
conn_size = 5
BUFFER_SIZE = 4096
blockFileStr = "src/blocklist.txt"


def main():
    f = open(blockFileStr, "r")

    for line in f:
        blockedUrls.add(line)

    f.close()

    inputOp = input("[*CONSOLE]Enter 's' to start proxy or 'o' for options or 'q' to quit:")

    if inputOp is "s":
        start_new_thread(Server,(HOSTNAME, server_port,conn_size))

    elif(inputOp is 'o'):
        display_Options()

    elif(inputOp is 'q'):
        exit()


    time.sleep(2)


    while(1):
        #

        inputOp = input("[*CONSOLE]Enter 'o' for options or 'q' to quit:")

        if(inputOp is 'q'):
            exit()

        elif(inputOp is 'o'):
            display_Options()


def display_Options():

    while(1):
        print(" 'v' -view or edit url blocklist\n",
              "'q' -quit\n",
              "'c' -return\n")

        inp = input("[*CONSOLE]Type command:")

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
