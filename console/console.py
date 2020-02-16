import socket
import sys
import os
import socketserver
import time
from server import Server
from threading import Timer
from _thread import start_new_thread


class Console:

    def __init__(self,block_file_str,server_port):
        self.block_file_str = block_file_str
        self.server_port = server_port

    def run(self):
        with open(self.block_file_str,"w+") as f:
            pass 

    
        while(1):
            inputOp = input("[*CONSOLE]Enter 's' to start proxy at %d ,'v' to edit blocklist ,'p' to change port, 'q' to quit:" % ( self.server_port ))

            if inputOp == "s": # Create new thread the server runs on
                start_new_thread(Server,(self.server_port,self.block_file_str))
                break

            elif(inputOp == 'v'):
                self.edit_blocklist(self.block_file_str)

            elif(inputOp == 'p'):
                self.server_port=int(input("Enter new port:"))

            elif(inputOp == 'q'):
                exit()

        while(1):
            time.sleep(1)
            inputOp = input("[*CONSOLE]Enter 'v' to edit blocklist or 'q' to quit:")

            if(inputOp == 'q'):
                exit()

            elif(inputOp == 'v'):
                self.edit_blocklist(self.block_file_str)

  
    def edit_blocklist(self,block_file_str):
        """Opens the blockfile list in default text editor"""
        print("[*CONSOLE]Opening text editor...")
        os.system('notepad.exe ' + block_file_str)
