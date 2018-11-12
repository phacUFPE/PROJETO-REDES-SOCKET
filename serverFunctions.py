import config as cfg
from threading import Thread
import _thread as thrd
import os
import gc
from databaseFunctions import Database

class Server:
    def __init__(self, ip=cfg.HOST, port=cfg.PORT):
        self.__ip = ip
        self.__port = port
        self.__sck = cfg.SOCKET_INFO
        self.__orig = (ip, port)
        self.__cliConnecteds = {}
        self.__usersFolder = cfg.FOLDER_USERS
        self.__db = Database()    

    def __del__(self):
        del self.__db
        del self.__ip
        del self.__port
        del self.__sck
        del self.__orig
        del self.__cliConnecteds
        gc.collect()

    def prepareConnection(self):    
        self.__sck.bind(self.__orig)
        self.__sck.listen(1)

    def checkDirExist(self, user):
        return os.path.isdir(self.__usersFolder + str(user))
    
    def createUserDir(self, user):
        os.mkdir(self.__usersFolder + str(user))

    def authentication(self, addr, user, password):
        user = str(user)
        aut = self.__db.searchForUser(user)
        if aut is None: return
        if aut[1] == user and aut[2] == password:
            if not self.checkDirExist(user): self.createUserDir(user)
            self.__cliConnecteds[addr] = self.__usersFolder + user
            print("Logado com sucesso, {0}!".format(user))

            return True
        else:
            print("Senha ou login incorretos!")
            
            return False

    def h_client(self, c_sck, addr):
        while True:
            data = c_sck.recv(1024).decode()              
            if not data: break
            if data == "EXIT": 
                break
            print("Cliente: {0}\nMensagem: {1}".format(addr, data))
            c_sck.send(data.encode())
        print("Finalizando conexao do Cliente {0}".format(addr))
        self.__cliConnecteds.pop(addr)
        c_sck.close()

    def openConnection(self):
        print("Servidor Inicializado!!\n")        
        while True:            
            con, addr = self.__sck.accept()
            self.__cliConnecteds[addr] = None
            print("Cliente {0} conectado!!".format(addr))
            thrd.start_new_thread(self.h_client ,(con, addr))    
        con.close()

    def getClientsConnected(self):
        for keys, vals in self.__cliConnecteds.items():
            print(keys)