import sqlite3

class dataBase():

    def addNewUser(self,user,password):
        con = sqlite3.connect('database/users.db')
        cursor = con.cursor()
        cursor.execute("""
        INSERT INTO authentication (user,password)
        VALUES (?,?)
        """, (user,password))
        con.commit()
        print('Dados inseridos com sucesso.')
        con.close()
    def openDB(self):
        con = sqlite3.connect('database/users.db')
        cursor = con.cursor()
        db = []
        cursor.execute("""
        SELECT * FROM authentication;
        """)
        for linha in cursor.fetchall():
            db.append(linha)
        return db
        con.close()


    