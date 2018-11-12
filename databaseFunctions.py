import sqlite3
import gc

class Database:
    def __init__(self):
        self.__path = 'database/users.db'
        self.__con = None
        self.__cursor = None
        self.openConn()

    def __del__(self):
        self.__con.close()
        del self.__path
        del self.__cursor
        del self.__con        
        gc.collect()

    def openConn(self):
        self.__con = sqlite3.connect(self.__path)
        self.__cursor = self.__con.cursor()

    def closeConn(self):
        self.__con.close()

    def addNewUser(self,user,password):
        self.__cursor.execute("""
        INSERT INTO authentication (login, password)
        VALUES (?,?)
        """, (user,password))
        self.__con.commit()
        print('Dados inseridos com sucesso.')

    def searchForUser(self, user):
        table = []
        self.__cursor.execute("""
        SELECT * FROM authentication WHERE login = ?;
        """, (user,))
        return self.__cursor.fetchone()

    def getAllAccounts(self):
        table = []
        self.__cursor.execute("""
        SELECT * FROM authentication;
        """)
        for linha in self.__cursor.fetchall():
            table.append(linha)
        return table

    
