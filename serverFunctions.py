import config as cfg
import base64
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
        self.__commandsDict = cfg.COMMANDS_DICT

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
        if not os.path.isdir(self.__usersFolder): os.mkdir(self.__usersFolder)
        os.mkdir(self.__usersFolder + str(user))

    def authentication(self, c_sck, addr, user, password):
        user = str(user)
        db = Database()
        aut = db.searchForUser(user)
        del db
        if not aut is None:
            if aut[1] == user and aut[2] == password:
                if not self.checkDirExist(user): self.createUserDir(user)
                self.__cliConnecteds[addr] = self.__usersFolder + user
                print("Usuario {0} logado com sucesso!".format(user))            
                return [True, user]
            else:
                return [False, False]
        return [False, None]

    @staticmethod
    def __decrypt(enc):
        key = "IF975 - Projeto de Redes"
        result = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            result_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            result.append(result_c)
        return "".join(result)

    @staticmethod
    def __crypt(text):
        cript = []
        key = "IF975 - Projeto de Redes"
        for i in range(len(text)):
            key_c = key[i % len(key)]
            cript_c = chr((ord(text[i]) + ord(key_c)) % 256)
            cript.append(cript_c)
        return base64.urlsafe_b64encode("".join(cript).encode()).decode()

    def GET(self, fServerPath, clientPath):
        with open(fServerPath, "rb") as f:
            fBytes = f.read(1024)
            fBytes_Crypted = Server.__crypt(fBytes)
        return fBytes_Crypted

    def POST(self, filePath, fServerPath):
        with open(filePath, "rb") as f:
            fileBytes = f.read()


    def PUT(self, filePath, fServerPath):
        pass

    def DELETE(self, fServerPath):
        pass

    def LIST(self, path):
        return os.listdir(path)

    def commands(self, c_sck, string, dft_dir):
        command = string.split(" ")[0]
        arg0 = string.split(" ")[1]
        arg1 = string.split(" ")[2]
        c_sck.send("{0} - {1} - {2}".format(command, arg0, arg1).encode())
        if not command or command is None: 
            c_sck.send("Digite um comando com as especifica��es!".encode()) 
            return
        if not arg0 or arg0 is None: 
            c_sck.send("Digite o caminho do arquivo!".encode()) 
            return        
        if command in self.__commandsDict:
            operation_number = self.__commandsDict[command]
            if operation_number == 0:
                f = " "
                while f != "":
                    f = self.GET(dft_dir+"/"+arg0, arg1)
                    c_sck.send(f.encode())
                #GET (PEGAR ARQUIVO)
            elif operation_number == 1:
                self.POST(arg0, arg1)
                #POST (COLOCAR ARQUIVO)
            elif operation_number == 2:
                self.PUT(arg0, arg1)
                #PUT (SUBSTITUIR ARQUIVO)
            elif operation_number == 3:
                self.LIST(dft_dir+arg0)
            else:
                self.DELETE(arg0)
                #DELETE (DELETAR ARQUIVO)
        else:
            c_sck.send("Isso n�o � um comando!".encode())
            return
 
    def h_client(self, c_sck, addr):
        firstTime = True
        authenticated = [False]
        user = None
        while True:
            while not authenticated[0]:
                c_sck.send("Digite seu usuario e senha\nExemplo: jerome 12345\n".encode())
                answ = c_sck.recv(1024).decode()
                answ = answ.split(" ")
                if len(answ) > 1:
                    authenticated = self.authentication(c_sck, addr, answ[0], answ[1])
                    if authenticated[1] is False:
                        c_sck.send("Senha ou login incorretos!\n".encode())
                    elif authenticated[1] is None:
                        c_sck.send("Usuario inexistente!\n".encode())
                try:
                    user = authenticated[1]
                except:
                    pass
            if firstTime:
                firstTime = False
                c_sck.send("Bem vindo, {0}".format(user).encode())            
            c_sck.send("""\n
            \n - COMANDOS
            \n GET
            \n POST
            \n PUT
            \n LIST
            \n DELETE\n            
            """.encode())
            data = c_sck.recv(1024).decode()
            self.commands(c_sck, data, self.__cliConnecteds[addr])
            if not data: break
            if data == "EXIT": 
                break
            print("Cliente: {0} - Login:{1}\nMensagem: {2}".format(addr, user, data))
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