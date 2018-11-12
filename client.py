import config as cfg
import clientFunctions import Client

cli = Client(cfg.SOCKET_INFO, cfg.DESTINATION)

cli.connectToServer()