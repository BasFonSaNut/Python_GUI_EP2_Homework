import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS pricelist (id INTEGER PRIMARY KEY, quantity text, priceperkilo text, totalprice text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM pricelist")
        rows = self.cur.fetchall()
        return rows

    def insert(self, quantity, priceperkilo, totalprice):
        self.cur.execute("INSERT INTO pricelist VALUES (NULL, ?, ?, ?)",
                         (quantity, priceperkilo, totalprice))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM pricelist WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, quantity, priceperkilo, totalprice):
        self.cur.execute("UPDATE pricelist SET quantity = ?, priceperkilo = ?, totalprice = ? WHERE id = ?",
                         (quantity, priceperkilo, totalprice, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


# db = Database('store.db')
# db.insert("10", "10",  "100")
# db.insert("5", "10",  "50")
# db.insert("13", "10", "130")

