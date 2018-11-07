import config
import socket as sck
from threading import Thread
import _thread as thread
import os

origin = config.ORIGIN

tcp = config.SOCKET_INFO

## SERVER
def openConnection():    
    tcp.bind(origin)
    tcp.listen(1)

def authentication(user, password):
    if not os.path.exists(config.FOLDER_USERS + user):
        os.mkdir(config.FOLDER_USERS + user)    


def h_client(c_sck, addr):
    while True:
        data = c_sck.recv(1024).decode()              
        if not data: break
        if data == "\x18": 
            break
        print("Cliente: {0}\nMensagem: {1}".format(addr, data))
        c_sck.send(data.encode())
    print("Finalizando conexao do Cliente {0}".format(addr))
    c_sck.close()

def establishConnection():
    while True:
        con, addr = tcp.accept()
        print("Conectado por {0}".format(addr))
        thread.start_new_thread(h_client ,(con, addr))    
    con.close()