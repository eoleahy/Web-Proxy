import socket
import sys
import os
import socketserver
import time
from Server import Server
from threading import Timer
from _thread import *



server_port = 8081
blockedUrls = set({})
blockFileStr = "src/blocklist.txt"


def main():
    port = server_port

    while(1):
        inputOp = input("[*CONSOLE]Enter 's' to start proxy at %d ,'o' for options ,'p' to change port, 'q' to quit:" % ( port ))

        if inputOp is "s":
            start_new_thread(Server,(port,blockFileStr))
            break

        elif(inputOp is 'o'):
            display_Options()

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
    # Opens file in text editor
    print("[*CONSOLE]Opening text editor...")
    os.system('notepad.exe ' + blockFileStr)

def display_Options():

    while(1):
        print(" 'v' -view or edit url blocklist\n",
              "'q' -quit\n",
              "'c' -return\n")

        inp = input("[*CONSOLE]Type command:")

        if(inp is 'v'):
            edit_blocklist()

        elif(inp is 'q'):
            exit()

        elif(inp is 'c'):
            return

if __name__ == '__main__':
    main()
