import config as cfg
import base64
from threading import Thread
import _thread as thrd
import os
import gc
from databaseFunctions import Database
from shutil import copyfile

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
        if aut is None:
            db.addNewUser(user,password)
            self.createUserDir(user)
            self.__cliConnecteds[addr] = self.__usersFolder + user
            print("Usuario {0} logado com sucesso!".format(user))            
            return [True, user]
        elif aut[1] == user and aut[2] == password:
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

    def GET(self, c_sck, arc):
        fBytes = b"1"
        #c_sck.send(os.path.basename(arc.name).encode())
        while fBytes != b"":   
            fBytes = arc.read(1024)
            c_sck.send(fBytes)
            print("Enviando...")
        arc.close()
        c_sck.send("Arquivo Transferido!".encode())
        #copyfile(self.__usersFolder + path, self.__usersFolder + str(user) + "/"+ "CÓPIA.TXT") ## Não pode salvar como cópia.txt, tem que ter uma maneira única de salvar cada cópia. 
        #return "Arquivo copiado com sucesso"
        

    def POST(self, c_sck, arc):
        arc = open()
        c_sck.recv(1024)
        #arq = os.open(self.__usersFolder + str(user) + "/" + str(name), os.O_RDWR|os.O_CREAT)
        #os.close(arq)
        #return str(name) + " foi criado!"

    def DELETE(self, user, name):
        os.remove((self.__usersFolder + str(user) + "/"+ str(name)))
        return str(name) + " removido com sucesso"

    def LIST(self, user):
        diretorios = os.listdir(self.__usersFolder + str(user))
        return "Arquivos e diretórios presentes no seu diretório" + str(diretorios)

    def commands(self, c_sck, string, user, dft_dir):
        cmd = string.split(" ")[0]
        if cmd != "DELETE" and cmd != "LIST":
            arg0 = None
            try:
                arg0 = string.split(" ")[1]
            except:
                pass
        if string == "LIST":
            result = self.LIST(user)
            c_sck.send(result.encode())
            pass
        elif string == "PUT":
            pass
        elif cmd == "GET":
            #c_sck.send("DIGITE O NOME DO ARQUIVO QUE VOCÊ QUER COPIAR ".encode())
            #path = c_sck.recv(1024).decode()
            arc = open(dft_dir + "/" + arg0, "rb")
            self.GET(c_sck, arc)  
        elif string == "POST":
            c_sck.send("DIGITE O NOME DO ARQUIVO QUE VOCÊ QUER CRIAR ".encode())
            name = c_sck.recv(1024).decode()
            #result = self.POST(user,name)
            #c_sck.send(result.encode())
        elif string == "DELETE":
            c_sck.send("DIGITE O NOME DO ARQUIVO QUE VOCÊ QUER DELETAR".encode())
            name = c_sck.recv(1024).decode()
            result = self.DELETE(user,name)
            c_sck.send(result.encode())
        else:
            c_sck.send("Digite o comando corretamente".encode())          
 
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
            print("Cliente: {0} - Login: {1}\nMensagem: {2}".format(addr, user, data))
            self.commands(c_sck, data, user, self.__cliConnecteds[addr])
            if not data: break
            if data == "EXIT": 
                break            
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