import socket
import sys
import os
import socketserver
import time
from Server import Server
from threading import Timer
from _thread import *

server_port = 8081
blockFileStr = "blocklist.txt"


def main():
    f=open(blockFileStr,"w+")
    f.close()
    port = server_port

    while(1):
        inputOp = input("[*CONSOLE]Enter 's' to start proxy at %d ,'v' to edit blocklist ,'p' to change port, 'q' to quit:" % ( port ))

        if inputOp is "s": # Create new thread the server runs on
            start_new_thread(Server,(port,blockFileStr))
            break

        elif(inputOp is 'v'):
            edit_blocklist()

        elif(inputOp is 'p'):
            port=int(input("Enter new port:"))

        elif(inputOp is 'q'):
            exit()

    while(1):
        time.sleep(1)
        inputOp = input("[*CONSOLE]Enter 'o' for options or 'q' to quit:")

        if(inputOp is 'q'):
            exit()

        elif(inputOp is 'o'):
            display_Options()


def edit_blocklist():
    """Opens the blockfile list in default text editor"""
    print("[*CONSOLE]Opening text editor...")
    os.system('notepad.exe ' + blockFileStr)

if __name__ == '__main__':
    main()
