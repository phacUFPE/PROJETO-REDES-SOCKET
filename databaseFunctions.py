import sqlite

DATABASE = "./database/users.db"

con = sqlite.connect(DATABASE)
cursor = con.cursor()

def getUserInfo(user):
    cursor.execute("SELECT * FROM authenticate WHERE login = '?'", (user))
    rs = cursor.dictfetchall()
    