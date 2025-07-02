ukoly = []

def hlavni_menu():
    while True:
        print("\nSprávce úkolů - Hlavní menu")
        print("1. Přidat nový úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Odstranit úkol")
        print("4. Konec programu")
        volba = input("Vyberte možnost (1-4): ")

        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            odstranit_ukol()
        elif volba == "4":
            print("Program ukončen. Nashledanou!")
            break
        else:
            print("Neplatná volba. Zkuste to znovu.")

def pridat_ukol():
    while True:
        nazev = input("Zadejte název úkolu: ").strip()
        if not nazev:
            print("Název nemůže být prázdný. Zkuste to znovu.")
            continue

        popis = input("Zadejte popis úkolu: ").strip()
        if not popis:
            print("Popis nemůže být prázdný. Zkuste to znovu.")
            continue

        ukoly.append({"nazev": nazev, "popis": popis})
        print(f"Úkol '{nazev}' byl přidán.")
        break  

def zobrazit_ukoly():
    if not ukoly:
        print("Seznam úkolů je prázdný.")
    else:
        print("Seznam úkolů:")
        for index, u in enumerate(ukoly, start=1):
            print(f"{index}. {u['nazev']} - {u['popis']}")

def odstranit_ukol():
    if not ukoly:
        print("Žádné úkoly k odstranění.")
        return

    print("Seznam úkolů k odstranění:")
    for index, u in enumerate(ukoly, start=1):
        print(f"{index}. {u['nazev']} - {u['popis']}")

    while True:
        try:
            cislo = int(input("Zadejte číslo úkolu, který chcete odstranit: "))

            if 1 <= cislo <= len(ukoly):
                odstraneny = ukoly.pop(cislo - 1)
                print(f"Úkol '{odstraneny['nazev']}' byl odstraněn.")

                break
            else:
                print("Neplatné číslo úkolu. Zadejte číslo z nabídky.")
        except ValueError:
            print("Zadejte platné číslo.")

hlavni_menu()
