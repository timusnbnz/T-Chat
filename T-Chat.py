import socket
from threading import Thread
from datetime import datetime
import time
import os

HOST1 = "0.0.0.0"
PORT1 = 5000
HOST2 = "0.0.0.0"
PORT2 = 5001

maxIncomingConnections = 1
globalStop = False

choice = input("Connection Part 1 or 2 : ")
if(choice=="1"):
    clientAdress = HOST1
    clientPort = PORT1
    serverAdress = HOST2
    serverPort = PORT2
else:
    clientAdress = HOST2
    clientPort = PORT2
    serverAdress = HOST1
    serverPort = PORT1

def client(cs):
    global globalStop
    print("---Chat---")
    while True:
        to_send =  input()
        if to_send.lower() == 'q':
            print("[!] Closed the session")
            globalStop = True
            break
        to_send = f"{to_send}"
        try:
            cs.send(to_send.encode())
        except:
            print("[!] Connection lost")
            globalStop = True
            break
        print(">>>" + str(to_send))

def server(ss):
    global globalStop
    while True:
        client_socket, client_address = ss.accept()
        while True:
            try:
                msg = client_socket.recv(1024).decode()
            except Exception as e:
                print("[!] Connection lost")
            if(msg!=""):
                print("[#] " + str(msg))
            else:
                time.sleep(1)
            if(globalStop==True):
                break
        if(globalStop==True):
            break

def main():
    os.system("clear")
    ss = socket.socket()
    while True:
        try:
            ss.bind((serverAdress,serverPort))
            ss.listen(maxIncomingConnections)
            t1 = Thread(target=server, args=(ss,))
            t1.daemon = True
            t1.start()
            print("[i] Server started")
            break
        except:
            pass

    cs = socket.socket()
    while True:
        try:
            cs.connect((clientAdress,clientPort))
            print("[+] Connection established")
            t2 = Thread(target=client, args=(cs,))
            t2.daemon = True
            t2.start()
            break
        except:
            pass

    while True:
        if(globalStop==True):
            input("Press enter to continue")
            break

main()
