import config as cfg
from serverFunctions import Server

svr = Server(cfg.SOCKET_INFO, cfg.ORIGIN)
svr.prepareConnection()
svr.openConnection()
