import config as cfg
import clientFunctions as cf

cli = cf.Client(cfg.SOCKET_INFO, cfg.DESTINATION)

cli.connectToServer()