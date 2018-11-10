import socket as sck

FOLDER_USERS = "./users/"

IPV4 = sck.AF_INET

TCP = sck.SOCK_STREAM

SOCKET_INFO = sck.socket(IPV4, TCP)

# Endereco IP do Servidor
HOST = '127.0.0.1'

# Porta do Servidor esta
PORT = 19120

ORIGIN = DESTINATION = (HOST, PORT)