import config
import socket as sck

tcp = config.SOCKET_INFO
destination = config.DESTINATION

def connectToServer():
    try:
        tcp.connect(destination)
    except ConnectionRefusedError:
        print("Servidor offline!")
        return            
    print("Para sair use CTRL+X\n")
    msg = input()
    while msg != "\x18":
        tcp.send(msg.encode())        
        msg = input()
    if msg == "\x18":
        tcp.send(msg.encode())
    tcp.close()
