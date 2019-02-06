import socket, sys, os
from _thread import *

def main():
    f=open("src/blockedURLS.txt","r+")

    blockedUrls =[]
    for line in f:
        blockedUrls = blockedUrls + f


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
    print("Options go here")



if __name__ == '__main__':
    main()
