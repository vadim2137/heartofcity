import sqlite3 as sql

class DataBase:

    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def isavailable(self, phonenumber):
        self.cur.execute("SELECT * FROM `users` WHERE phonenumber=?", (phonenumber, ))
        user = self.cur.fetchall()
        if user != []:
            return False
        else:
            return True

    

    def adduser(self, firstname, surname, password, phonenumber):
        self.cur.execute("INSERT INTO `users`(firstname, surname, password, phonenumber) VALUES (?, ?, ?, ?)",
                         (firstname, surname, password, phonenumber))
        self.con.commit()
        self.cur.execute("SELECT * FROM `users` WHERE phonenumber=?", (phonenumber, ))
        user = self.cur.fetchall()
        idu = user[0][0]

    def CreateNewUser(self, firstname, surname, password, phonenumber):
        if self.isavailable(phonenumber):
            self.adduser(firstname, surname, password, phonenumber)
            return True, firstname, surname, password, phonenumber, idu
        else:
            return False, "balabolikiz", "barashek", 3, 4, 5

    def LoginUser(self, phonenumber, password):
        print(phonenumber)
        self.cur.execute("SELECT * FROM `users` WHERE phonenumber=?", (phonenumber, ))
        user = self.cur.fetchall()
        print(user)
        pw = user[0][3]
        firstname = user[0][1]
        surname = user[0][2]
        idu = user[0][0]

        if pw == password:
            return True, firstname, surname, idu
        else:
            return False, "balabolikiz", "barashek", -1


    def AddIdea(self, title, desc, filename, userid):
        self.cur.execute("INSERT INTO `idea`(title, description, photo, userid) VALUES (?, ?, ?, ?)",
                         (title, desc, filename, userid))
        self.con.commit()

