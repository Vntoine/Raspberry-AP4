import sqlite3
def insertLogAcces(numeroPhase,identification,numeroBadge,commentaire):
    con = sqlite3.connect('kliemie.db')
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO logAcces(numPhase,identifiant,numBadge,commentaire) values ("+numeroPhase+",'"+identification+"','"+numeroBadge+"','"+commentaire+"');")
        con.commit()
    except sqlite3.IntegrityError:
        print("Error during insertion")
    con.close()