import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    try:
        spojeni = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',          
            password='ozzy1234',     
            database='task_manager'
        )
        return spojeni
    except Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None
# Vytvoření tabulky
def vytvoreni_tabulky():
    spojeni = pripojeni_db()
    if spojeni is None:
        return

    kurzor = spojeni.cursor()
    kurzor.execute("""
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
            datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    spojeni.commit()
    kurzor.close()
    spojeni.close()

def pripojeni_test_db():
    try:
        spojeni = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='ozzy1234',
            database='task_manager_test'  # testovacia databáza
        )
        return spojeni
    except Error as e:
        print(f"Chyba při připojení k testovací databázi: {e}")
        return None    

# Přidání nového úkolu do databáze
def pridat_ukol_do_db(nazev, popis, spojeni=None):
    if not nazev or not popis:
        return False  

    vlastne_spojeni = False
    if spojeni is None:
        spojeni = pripojeni_db()
        vlastne_spojeni = True

    if spojeni is None:
        return False

    kurzor = spojeni.cursor()
    sql = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
    kurzor.execute(sql, (nazev, popis))
    spojeni.commit()
    kurzor.close()

    if vlastne_spojeni:
        spojeni.close()

    return True  

def pridat_ukol():
    nazev = input("Zadejte název úkolu: ").strip()
    popis = input("Zadejte popis úkolu: ").strip()

    if pridat_ukol_do_db(nazev, popis):
        print(f"Úkol '{nazev}' byl úspěšně přidán.")
    else:
        print("Chyba: Úkol se nepodařilo přidat.")

# Zobrazení aktivních úkolů z databáze
def zobrazit_ukoly():
    spojeni = pripojeni_db()
    if spojeni is None:
        return

    kurzor = spojeni.cursor(dictionary=True)
    sql = "SELECT * FROM ukoly WHERE stav IN ('Nezahájeno', 'Probíhá')"
    kurzor.execute(sql)
    vysledky = kurzor.fetchall()

    if not vysledky:
        print("Seznam úkolů je prázdný.")
    else:
        print("\nAktivní úkoly:")
        for u in vysledky:
            print(f"{u['id']}. {u['nazev']} - {u['popis']} [{u['stav']}]")

    kurzor.close()
    spojeni.close()

    return vysledky

# Aktualizace stavu úkolu
def aktualizovat_ukol_v_db(ukol_id, novy_stav, spojeni=None):
    if novy_stav not in ("Probíhá", "Hotovo"):
        return False  # neplatný stav

    vlastne_spojeni = False
    if spojeni is None:
        spojeni = pripojeni_db()
        vlastne_spojeni = True

    if spojeni is None:
        return False

    kurzor = spojeni.cursor()
    sql = "UPDATE ukoly SET stav = %s WHERE id = %s"
    kurzor.execute(sql, (novy_stav, ukol_id))
    spojeni.commit()
    uspesne = kurzor.rowcount > 0
    kurzor.close()

    if vlastne_spojeni:
        spojeni.close()

    return uspesne

def aktualizovat_ukol():
    zobrazit_ukoly()
    try:
        id_ukolu = int(input("Zadejte ID úkolu, který chcete aktualizovat: "))
    except ValueError:
        print("Neplatné ID.")
        return

    print("Možnosti stavu: 1. Probíhá, 2. Hotovo")
    volba = input("Vyberte nový stav (1/2): ")
    if volba == "1":
        novy_stav = "Probíhá"
    elif volba == "2":
        novy_stav = "Hotovo"
    else:
        print("Neplatná volba.")
        return

    if aktualizovat_ukol_v_db(id_ukolu, novy_stav):
        print("Stav úkolu byl aktualizován.")
    else:
        print("Úkol s tímto ID neexistuje nebo došlo k chybě.")

# Odstranění úkolu z databáze
def odstranit_ukol_z_db(ukol_id, spojeni=None):
    vlastne_spojeni = False
    if spojeni is None:
        spojeni = pripojeni_db()
        vlastne_spojeni = True

    if spojeni is None:
        return False

    kurzor = spojeni.cursor()
    sql = "DELETE FROM ukoly WHERE id = %s"
    kurzor.execute(sql, (ukol_id,))
    spojeni.commit()
    uspesne = kurzor.rowcount > 0
    kurzor.close()

    if vlastne_spojeni:
        spojeni.close()

    return uspesne

def odstranit_ukol():
    zobrazit_ukoly()
    try:
        id_ukolu = int(input("Zadejte ID úkolu, který chcete odstranit: "))
    except ValueError:
        print("Neplatné ID.")
        return

    if odstranit_ukol_z_db(id_ukolu):
        print("Úkol byl úspěšně odstraněn.")
    else:
        print("Úkol s tímto ID neexistuje nebo došlo k chybě.")

# Hlavní menu aplikace
def hlavni_menu():
    vytvoreni_tabulky()  

    while True:
        print("\n=== SPRÁVCE ÚKOLŮ ===")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit")

        volba = input("Zvolte možnost (1-5): ")

        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            aktualizovat_ukol()
        elif volba == "4":
            odstranit_ukol()
        elif volba == "5":
            print("Program ukončen.")
            break
        else:
            print("Neplatná volba. Zkuste to znovu.")

# Spustenie projektu
if __name__ == "__main__":
    hlavni_menu()