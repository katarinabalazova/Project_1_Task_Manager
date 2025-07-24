import unittest
from task_manager_project import (
    pripojeni_test_db,
    pridat_ukol_do_db,
    aktualizovat_ukol_v_db,
    odstranit_ukol_z_db
)

class TestUkoly(unittest.TestCase):

    def setUp(self):
        # Pripojenie sa k testovacej databáze 
        self.spoj = pripojeni_test_db()
        self.assertIsNotNone(self.spoj, "Nepodarilo sa pripojiť k testovacej databáze")

        # Vyčistenie tabuľky
        kurzor = self.spoj.cursor()
        kurzor.execute("DELETE FROM ukoly")
        self.spoj.commit()
        kurzor.close()

    def tearDown(self):
        # Po každom teste zatvorím pripojenie k databáze
        self.spoj.close()

    # TESTY PRIDANIA ÚKOLU 

    def test_pridat_ukol_pozitivny(self):
        # Test pridania platného úkolu
        vysledok = pridat_ukol_do_db("Testovací úkol", "Popis testu", spojeni=self.spoj)
        self.assertTrue(vysledok)

        # Overenie, že úkol sa skutočne uložil do DB
        kurzor = self.spoj.cursor()
        kurzor.execute("SELECT nazev, popis FROM ukoly WHERE nazev = %s", ("Testovací úkol",))
        zaznam = kurzor.fetchone()
        kurzor.close()

        self.assertIsNotNone(zaznam)
        self.assertEqual(zaznam[0], "Testovací úkol")
        self.assertEqual(zaznam[1], "Popis testu")

    def test_pridat_ukol_negativny_prazdny_nazev(self):
        # Test pridania úkolu s prázdnym názvom (neplatné)
        vysledok = pridat_ukol_do_db("", "Popis testu", spojeni=self.spoj)
        self.assertFalse(vysledok)

        kurzor = self.spoj.cursor()
        kurzor.execute("SELECT * FROM ukoly WHERE popis = %s", ("Popis testu",))
        vysledky = kurzor.fetchall()
        kurzor.close()

        self.assertEqual(len(vysledky), 0)

    def test_pridat_ukol_negativny_prazdny_popis(self):
        # Test pridania úkolu s prázdnym popisom (neplatné)
        vysledok = pridat_ukol_do_db("Názov bez popisu", "", spojeni=self.spoj)
        self.assertFalse(vysledok)

        kurzor = self.spoj.cursor()
        kurzor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Názov bez popisu",))
        vysledky = kurzor.fetchall()
        kurzor.close()

        self.assertEqual(len(vysledky), 0)

    # TESTY AKTUALIZÁCIE ÚKOLU

    def test_aktualizovat_ukol_pozitivny(self):
        # Pridáme úkol na aktualizáciu
        pridat_ukol_do_db("Na aktualizáciu", "Popis", spojeni=self.spoj)

        kurzor = self.spoj.cursor()
        kurzor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Na aktualizáciu",))
        ukol_id = kurzor.fetchone()[0]
        kurzor.close()

        vysledok = aktualizovat_ukol_v_db(ukol_id, "Hotovo", spojeni=self.spoj)
        self.assertTrue(vysledok)

        kurzor = self.spoj.cursor()
        kurzor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
        stav = kurzor.fetchone()[0]
        kurzor.close()

        self.assertEqual(stav, "Hotovo")

    def test_aktualizovat_ukol_negativny_neplatny_stav(self):
        # Pridáme úkol s platným stavom
        pridat_ukol_do_db("Úkol s neplatným stavem", "Popis", spojeni=self.spoj)

        kurzor = self.spoj.cursor()
        kurzor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol s neplatným stavem",))
        ukol_id = kurzor.fetchone()[0]
        kurzor.close()

        vysledok = aktualizovat_ukol_v_db(ukol_id, "Dokončeno", spojeni=self.spoj)
        self.assertFalse(vysledok)

        kurzor = self.spoj.cursor()
        kurzor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
        stav = kurzor.fetchone()[0]
        kurzor.close()

        self.assertEqual(stav, "Nezahájeno")

    def test_aktualizovat_ukol_negativny_neexistujuci_id(self):
        # Aktualizácia s neexistujúcim ID (mala by zlyhať)
        vysledok = aktualizovat_ukol_v_db(99999, "Hotovo", spojeni=self.spoj)
        self.assertFalse(vysledok)

    # TESTY ODSTRÁNENIA ÚKOLU

    def test_odstranit_ukol_pozitivny(self):
        # Pridáme úkol, ktorý budeme mazať
        pridat_ukol_do_db("Na zmazanie", "Test", spojeni=self.spoj)

        kurzor = self.spoj.cursor()
        kurzor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Na zmazanie",))
        ukol_id = kurzor.fetchone()[0]
        kurzor.close()

        vysledok = odstranit_ukol_z_db(ukol_id, spojeni=self.spoj)
        self.assertTrue(vysledok)

        kurzor = self.spoj.cursor()
        kurzor.execute("SELECT * FROM ukoly WHERE id = %s", (ukol_id,))
        zaznam = kurzor.fetchone()
        kurzor.close()

        self.assertIsNone(zaznam)  # Úkol by už nemal existovať v DB

    def test_odstranit_ukol_negativny_neexistujuci_id(self):
        # Odstránime úkol, ktorý neexistuje
        neexistujuce_id = 99999  # ID, ktoré v DB nebude

        vysledok = odstranit_ukol_z_db(neexistujuce_id, spojeni=self.spoj)

        # Funkcia by mala vrátiť False, lebo nič neodstránila
        self.assertFalse(vysledok)


if __name__ == "__main__":
    unittest.main()


