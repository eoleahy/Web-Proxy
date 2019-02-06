import socket, sys, os
from _thread import *

blockedUrls ={}
blockedUrls = set()

blockFileStr = "src/blocklist.txt"

def main():
    f=open(blockFileStr,"r")

    for line in f:
        blockedUrls.add(line)

    f.close()

    while(1):

        inputOp = input("Enter 'a' to continue or 'o' for options or 'q' to quit\n")

        if(inputOp is 'q'):
            exit()

        elif(inputOp is 'o'):
            display_Options()

        elif(inputOp is 'a'):
            start()


def start():
        while(1):

            HOSTNAME = ''
            port = input("Enter Port or type 'q' to return:")
            if(port is 'q'):
                return

            else:
                try:
                    port = int(port)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.bind((HOSTNAME,port))
                    print("Socket created...")

                except (OSError,socket.error):
                    print("Port is in use")
                except (ValueError,TypeError):
                    print("Incorrect")


def display_Options():

    while(1):
        print(" 'v' -view or edit url blocklist\n",
                "'q' -quit\n",
                "'c' -return\n")

        inp = input()

        if(inp is 'v'):
            os.system('notepad.exe ' + blockFileStr)
            f=open(blockFileStr,"r")

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
