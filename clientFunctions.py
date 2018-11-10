import config
import socket as sck

class Client:
    def __init__(self, socket, destination):
        self.sck = socket
        self.dest = destination

    def connectToServer(self):
        try:
            self.sck.connect(self.dest)
        except ConnectionRefusedError:
            print("Servidor offline!")
            return            
        print("Para sair use o  comando 'EXIT'\n")
        try:
            msg = input()
            while msg != "EXIT":
                self.sck.send(msg.encode())        
                msg = input()
            if msg == "EXIT":
                self.sck.send(msg.encode())
        except ConnectionResetError:
            print("Servidor foi desligado!")
        self.sck.close()
