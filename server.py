import config as cfg
import serverFunctions as sf

svr = sf.Server(cfg.SOCKET_INFO, cfg.ORIGIN)
svr.prepareConnection()
svr.openConnection()
