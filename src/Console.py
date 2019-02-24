import socket
import sys
import os
import socketserver
import time
from Server import Server
from _thread import *



server_port = 8001
blockedUrls = set({})
blockFileStr = "src/blocklist.txt"


def main():
    f = open(blockFileStr, "r")

    for line in f:
        blockedUrls.add(line)

    f.close()

    while(1):
        inputOp = input("[*CONSOLE]Enter 's' to start proxy or 'o' for options or 'q' to quit:")

        if inputOp is "s":
            start_new_thread(Server,(server_port,))
            break

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


def editBlockList():
    # Opens file in text editor
    print("[*CONSOLE]Opening text editor...")
    os.system('notepad.exe ' + blockFileStr)
    f = open(blockFileStr, "r")

    # Clear url set and read as file is updated
    blockedUrls.clear()

    for line in f:
        blockedUrls.add(line)

    f.close()

def display_Options():

    while(1):
        print(" 'v' -view or edit url blocklist\n",
              "'q' -quit\n",
              "'c' -return\n")

        inp = input("[*CONSOLE]Type command:")

        if(inp is 'v'):
            editBlockList()

        elif(inp is 'q'):
            exit()

        elif(inp is 'c'):
            return

if __name__ == '__main__':
    main()
