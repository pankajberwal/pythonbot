import sqlite3

class DBHelper:
    def __init__(self,dbname="todo.sqlite"):
        self.dbname=dbname
        self.conn=sqlite3.connect(dbname)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    def add_item(self,item_text,owner):
        stmnt="INSERT INTO items (description,owner) VALUES (?,?)"
        args=(item_text,owner)
        self.conn.execute(stmnt,args)
        self.conn.commit()

    def delete_item(self,item_text,owner):
        stmnt="DELETE FROM items WHERE description=(?)& owner=(?)"
        args=(item_text,owner)
        self.conn.execute(stmnt,args)
        self.conn.commit()

    def get_item(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner,)
        return [x[0] for x in self.conn.execute(stmt, args)]