import pytest
from task_manager_project import (
    pripojeni_test_db,
    pridat_ukol_do_db,
    aktualizovat_ukol_v_db,
    odstranit_ukol_z_db
)

@pytest.fixture
def db_spoj():
    spoj = pripojeni_test_db()
    assert spoj is not None, "Nepodarilo sa pripojiť k testovacej databáze"
    
    # Vymažeme všetky dáta pred každým testom
    kurzor = spoj.cursor()
    kurzor.execute("DELETE FROM ukoly")
    spoj.commit()
    kurzor.close()

    yield spoj  # odovzdáme spoj testom

    spoj.close()


# TESTY PRIDANIA ÚKOLU 

def test_pridat_ukol_pozitivny(db_spoj):
    vysledok = pridat_ukol_do_db("Testovací úkol", "Popis testu", spojeni=db_spoj)
    assert vysledok is True

    kurzor = db_spoj.cursor()
    kurzor.execute("SELECT nazev, popis FROM ukoly WHERE nazev = %s", ("Testovací úkol",))
    zaznam = kurzor.fetchone()
    kurzor.close()

    assert zaznam is not None
    assert zaznam[0] == "Testovací úkol"
    assert zaznam[1] == "Popis testu"

def test_pridat_ukol_negativny_prazdny_nazev(db_spoj):
    vysledok = pridat_ukol_do_db("", "Popis testu", spojeni=db_spoj)
    assert vysledok is False

    kurzor = db_spoj.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE popis = %s", ("Popis testu",))
    vysledky = kurzor.fetchall()
    kurzor.close()

    assert len(vysledky) == 0

def test_pridat_ukol_negativny_prazdny_popis(db_spoj):
    vysledok = pridat_ukol_do_db("Názov bez popisu", "", spojeni=db_spoj)
    assert vysledok is False

    kurzor = db_spoj.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Názov bez popisu",))
    vysledky = kurzor.fetchall()
    kurzor.close()

    assert len(vysledky) == 0


# TESTY AKTUALIZÁCIE ÚKOLU

def test_aktualizovat_ukol_pozitivny(db_spoj):
    pridat_ukol_do_db("Na aktualizáciu", "Popis", spojeni=db_spoj)

    kurzor = db_spoj.cursor()
    kurzor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Na aktualizáciu",))
    ukol_id = kurzor.fetchone()[0]
    kurzor.close()

    vysledok = aktualizovat_ukol_v_db(ukol_id, "Hotovo", spojeni=db_spoj)
    assert vysledok is True

    kurzor = db_spoj.cursor()
    kurzor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
    stav = kurzor.fetchone()[0]
    kurzor.close()

    assert stav == "Hotovo"

def test_aktualizovat_ukol_negativny_neplatny_stav(db_spoj):
    pridat_ukol_do_db("Úkol s neplatným stavem", "Popis", spojeni=db_spoj)

    kurzor = db_spoj.cursor()
    kurzor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol s neplatným stavem",))
    ukol_id = kurzor.fetchone()[0]
    kurzor.close()

    vysledok = aktualizovat_ukol_v_db(ukol_id, "Dokončeno", spojeni=db_spoj)
    assert vysledok is False

    kurzor = db_spoj.cursor()
    kurzor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
    stav = kurzor.fetchone()[0]
    kurzor.close()

    assert stav == "Nezahájeno"

def test_aktualizovat_ukol_negativny_neexistujuci_id(db_spoj):
    vysledok = aktualizovat_ukol_v_db(99999, "Hotovo", spojeni=db_spoj)
    assert vysledok is False


# TESTY ODSTRÁNENIA ÚKOLU 

def test_odstranit_ukol_pozitivny(db_spoj):
    pridat_ukol_do_db("Na zmazanie", "Test", spojeni=db_spoj)

    kurzor = db_spoj.cursor()
    kurzor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Na zmazanie",))
    ukol_id = kurzor.fetchone()[0]
    kurzor.close()

    vysledok = odstranit_ukol_z_db(ukol_id, spojeni=db_spoj)
    assert vysledok is True

    kurzor = db_spoj.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE id = %s", (ukol_id,))
    zaznam = kurzor.fetchone()
    kurzor.close()

    assert zaznam is None

def test_odstranit_ukol_negativny_neexistujuci_id(db_spoj):
    vysledok = odstranit_ukol_z_db(99999, spojeni=db_spoj)
    assert vysledok is False
