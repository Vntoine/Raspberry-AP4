import sqlite3
con = sqlite3.connect('kliemie.db')
cur = con.cursor()
cur.execute("select * from logAcces")
rows = cur.fetchall()
for row in rows:
    print(row)
con.close()