import config
from threading import Thread
import _thread as thrd
import os

class Server:
    def __init__(self, socket, origin):
        self.sck = socket
        self.orig = origin

    def prepareConnection(self):        
        self.sck.bind(self.orig)
        self.sck.listen(1)    

    def authentication(self, user, password):
        if not os.path.exists(config.FOLDER_USERS + user):
            os.mkdir(config.FOLDER_USERS + user)    

    def h_client(self, c_sck, addr):
        while True:
            data = c_sck.recv(1024).decode()              
            if not data: break
            if data == "EXIT": 
                break
            print("Cliente: {0}\nMensagem: {1}".format(addr, data))
            c_sck.send(data.encode())
        print("Finalizando conexao do Cliente {0}".format(addr))
        c_sck.close()

    def openConnection(self):
        print("Servidor Inicializado!!\n")        
        while True:            
            con, addr = self.sck.accept()
            print("Cliente {0} conectado!!".format(addr))
            thrd.start_new_thread(self.h_client ,(con, addr))    
        con.close()