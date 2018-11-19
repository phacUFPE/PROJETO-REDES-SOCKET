import config as cfg
import gc

class Client:
    def __init__(self, ip=cfg.HOST, port=cfg.PORT):
        self.__sck = cfg.SOCKET_INFO
        self.__dest = (ip, port)

    def __del__(self):
        del self.__sck
        del self.__dest
        gc.collect()

    def connectToServer(self):
        try:
            self.__sck.connect(self.__dest)
        except ConnectionRefusedError:
            print("Servidor offline!")
            return            
        print("Para sair use o  comando 'EXIT'\n")
        self.__sck.send("sucessfully!".encode())
        print(self.__sck.recv(1024).decode())
        try:
            msg = input()
            while msg != "EXIT":
                self.__sck.send(msg.encode())
                msg = input()
            if msg == "EXIT":
                self.__sck.send(msg.encode())
        except ConnectionResetError:
            print("Servidor foi desligado!")
        self.__sck.close()
