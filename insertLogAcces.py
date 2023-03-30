def insertLogAcces(numeroPhase,identification,numeroBadge,commentaire):
    con = sqlite3.connect('kliemie.db')
    cur = con.cursor()
    success = False
    try:
        cur.execute("INSERT INTO logAcces(numPhase,identifiant,numBadge,commentaire) values ("+str(numeroPhase)+",'"+identification+"','"+numeroBadge+"','"+commentaire+"');")
        con.commit()
        success = True
    except sqlite3.IntegrityError:
        print("Error during insertion")
    con.close()
    return success