import sqlite3

class DBHelper:
    def __init__(self,dbname="todo.sqlite"):
        self.dbname=dbname
        self.conn=sqlite3.connect(dbname)

    def setup(self):
        stmnt="CREATE TABLE IF NOT EXISTS items(description text)"
        self.conn.execute(semnt)
        self.conn.commit()

    def add_item(self,item_text):
        stmnt="INSERT INTO items (description) VALUES (?)"
        args=(item_text,)
        self.conn.execute(stmnt,args)
        self.conn.commit()

    def delete_item(self,item_text):
        stmnt="DELETE FROM items WHERE description=(?)"
        args=(item_text,)
        self.conn.execute(stmnt,args)
        self.conn.commit()

    def get_item(self):
        stmnt="SELECT Ddescription FROM items"
        return [x[0] for x in self.conn.execute(stmnt)]