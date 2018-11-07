import socket as sck

FOLDER_USERS = "./users/"

SOCKET_INFO = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

# Endereco IP do Servidor
HOST = '127.0.0.1'

# Porta do Servidor esta
PORT = 19120

ORIGIN = DESTINATION = (HOST, PORT)