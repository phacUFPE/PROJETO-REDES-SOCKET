import config as cfg
from serverFunctions import Server
import os
import gc

class Client:
    def __init__(self, ip=cfg.HOST, port=cfg.PORT):
        self.__sck = cfg.SOCKET_INFO
        self.__dest = (ip, port)

    def __del__(self):
        del self.__sck
        del self.__dest
        gc.collect()

    def client_commands(self, string):
        arg0 = None
        arg1 = None
        command = string.split(" ")[0]
        try:
            arg0 = string.split(" ")[1]
            arg1 = string.split(" ")[2]
        except:
            pass
        if not command or command is None: 
            return
        if not arg0 or arg0 is None:
            return
        if command == "GET":
            self.__sck.send(string.encode())
            #resp = self.__sck.recv(1024)
            resp = b""
            arc = open(arg0, "wb")
            while resp != b"Arquivo Transferido!":                
                resp = self.__sck.recv(1024)
                if resp != b"Arquivo Transferido!":
                    arc.write(resp)
            arc.close()
            msg = input()
            self.__sck.send(msg.encode())  
        elif command == "POST":
            self.__sck.send(string.encode())
            arc = open(arg0, "rb")
            fBytes = b"1"
            while fBytes != b"":
                fBytes = arc.read(1024)
                self.__sck.send(fBytes)
            arc.close()
            msg = input()
            self.__sck.send(msg.encode())
        elif command == "PUT":
            pass
        elif command == "LIST":
            self.__sck.send(command)
            print(self.__sck.recv(1024).decode())
        elif command == "DELETE":
            self.__sck.send(command)
            print(self.__sck.recv(1024).decode())
            msg = input()
            self.__sck.send(msg.encode())
        else:
            return

    def connectToServer(self):
        try:
            self.__sck.connect(self.__dest)
        except ConnectionRefusedError:
            print("Servidor offline!")
            return
        print("Para sair use o  comando 'EXIT'\n")
        print(self.__sck.recv(1024).decode())
        try:
            msg = input(":: ")            
            while msg != "EXIT":                
                self.__sck.send(msg.encode())
                fromsrv = self.__sck.recv(1024).decode()
                print("SERVER DIZ: " + fromsrv)
                msg = input(":: ")
                self.client_commands(msg)        
            if msg == "EXIT":
                self.__sck.send(msg.encode())
        except ConnectionResetError:
            print("Servidor foi desligado!")
        self.__sck.close()
