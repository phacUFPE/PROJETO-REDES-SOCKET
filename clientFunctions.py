import config as cfg
from serverFunctions import Server
import gc

class Client:
    def __init__(self, ip=cfg.HOST, port=cfg.PORT):
        self.__sck = cfg.SOCKET_INFO
        self.__dest = (ip, port)

    def __del__(self):
        del self.__sck
        del self.__dest
        gc.collect()

    def client_commands(self, command):
        command = string.split(" ")[0]
        arg0 = string.split(" ")[1]
        arg1 = string.split(" ")[2]
        if not command or command is None: 
            return
        if not arg0 or arg0 is None:
            return
        if command == "GET":
            with open(arg1, "w") as f:
                while self.__sck.recv(1024) != "COMPLETO!":
                    fBytes = Server.__decrypt(self.__sck.recv(1024))
                    f.write(fBytes)

        elif command == "POST":
            pass
        elif command == "PUT":
            pass
        elif command == "LIST":
            pass
        elif command = "DELETE":
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
                print(self.__sck.recv(1024).decode())
                msg = input(":: ")
            if msg == "EXIT":
                self.__sck.send(msg.encode())
        except ConnectionResetError:
            print("Servidor foi desligado!")
        self.__sck.close()
