
'''
Használati utasítás:

Indítsa el a szoftvert.

    1. A főmenüből válassza az [1] Foglalás menüpontot.
    2. Adja meg a foglalni kívánt szoba számát (például 301).
    3. Adja meg a foglalás dátumát ÉÉÉÉ.HH.NN formátumban (például 2024.07.25).
    4. Sikeres foglalás esetén megjelenik a foglalási azonosító és az összeg (például ABC123, 18000 Ft).
    5. Foglalások listázása: [3], törlés: [2] (add meg a foglalási azonosítót a törléshez), kilépés: [4].

Példa foglalás:
[1] -> 301 -> 2024.07.25 -> "A foglalás sikeres volt. Foglalási azonosító: ABC123, Díj: 18000 Ft."
'''

from datetime import datetime
import random
import string

#Szoba osztály létrehozása
class Szoba:
    #Szoba osztály inicializálása
    def __init__(self, szobaszam, szobaar):
        self.szobaszam = szobaszam
        self.szobaar = szobaar

#Egyszemélyes szoba osztály
class EgyszemelyesSzoba(Szoba):
    #Egyszemélyes szoba inicializálása
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 18000)

#Kétszemélyes szoba osztály
class KetszemelyesSzoba(Szoba):
    #Kétszemélyes szoba inicializálása
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 25000)

#Foglalás osztály
class Foglalas:
    #Foglalás inicializálása
    def __init__(self, foglalas_id, szoba, datum):
        self.foglalas_id = foglalas_id
        self.szoba = szoba
        self.datum = datum

#Foglalás kezelő osztály
class FoglalasMenedzser:
    #Foglalás kezelő inicializálása
    def __init__(self, hotel):
        self.hotel = hotel
        self.osszes_foglalas = []

    #Generál egy egyedi foglalási számot
    def general_foglalas_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    #Új foglalás létrehozása
    def uj_foglalas(self, szobaszam, datum):
        for szoba in self.hotel.szobak:
            if szoba.szobaszam == szobaszam:
                if not self.foglalt_e(szoba, datum):
                    foglalas_id = self.general_foglalas_id()
                    friss_foglalas = Foglalas(foglalas_id, szoba, datum)
                    self.osszes_foglalas.append(friss_foglalas)
                    return foglalas_id, szoba.szobaar
        return None, None

    #Foglalás törlése
    def foglalas_torles(self, foglalas_id):
        for foglalas in self.osszes_foglalas:
            if foglalas.foglalas_id == foglalas_id:
                self.osszes_foglalas.remove(foglalas)
                print("A foglalást sikeresen töröltük.")
                return True
        print("Érvénytelen foglalási szám.")
        return False

    #Foglalások listázása
    def foglalasok_listazasa(self):
        for foglalas in self.osszes_foglalas:
            print(f"Foglalás ID: {foglalas.foglalas_id}, Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum.strftime('%Y-%m-%d')}")

    #Ellenőrzés, hogy a szoba foglalt-e
    def foglalt_e(self, szoba, datum):
        for foglalas in self.osszes_foglalas:
            if foglalas.szoba == szoba and foglalas.datum.date() == datum.date():
                return True
        return False

#Hotel osztály
class Hotel:
    #Hotel osztály inicializálása
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    #Szoba hozzáadása a hotelhez
    def szoba_hozzaadasa(self, szoba):
        self.szobak.append(szoba)

#Hotel adatok betöltése
def hotel_adatok_betoltese():
    #Hotel adatok inicializálása
    hotel = Hotel("Luxus Hotel")
    hotel.szoba_hozzaadasa(EgyszemelyesSzoba("301"))
    hotel.szoba_hozzaadasa(KetszemelyesSzoba("401"))
    hotel.szoba_hozzaadasa(KetszemelyesSzoba("402"))
    return hotel

#Fő program
def main():
    #Hotel adatok betöltése
    hotel = hotel_adatok_betoltese()
    foglalo = FoglalasMenedzser(hotel)

    #Menü megjelenítése
    while True:
        print("Kérlek, válassz egy menüpontot:")
        print("[1] Szoba foglalása")
        print("[2] Foglalás törlése")
        print("[3] Foglalásaim megtekintése")
        print("[4] Kilépés")

        #Felhasználéói választás
        valasztott_menu = input("Add meg a választott menüpont számát: ")
        if valasztott_menu == "1":
            #Szoba foglalása
            foglalando_szoba = input("Add meg a foglalni kívánt szoba számát: ")
            datum_bemenet = input("Add meg a foglalás dátumát (év.hónap.nap): ")
            try:
                datum = datetime.strptime(datum_bemenet, "%Y.%m.%d")
                if datum >= datetime.now():
                    foglalas_id, szoba_ara = foglalo.uj_foglalas(foglalando_szoba, datum)
                    if szoba_ara:
                        print(f"A foglalás sikeres volt. Foglalási azonosító: {foglalas_id}, Díj: {szoba_ara} Ft.")
                    else:
                        print("Nincs szabad szoba a megadott dátumra.")
                else:
                    print("Csak jövőbeli dátumra lehetséges a foglalás.")
            except ValueError:
                print("Érvénytelen dátum formátum. A helyes formátum: ÉÉÉÉ.HH.NN")
        elif valasztott_menu == "2":
            #Foglalás törlése
            foglalas_id = input("Add meg a törölni kívánt foglalás azonosítóját: ")
            foglalo.foglalas_torles(foglalas_id)
        elif valasztott_menu == "3":
            #Foglalások megtekintése
            print("Foglalások listája:")
            foglalo.foglalasok_listazasa()
            print("Elérhető szobák: 301, 401, 402")
            print("Egyszemélyes szoba díja: 18000 Ft (301)")
            print("Kétszemélyes szoba díja: 25000 Ft (401, 402)")
        elif valasztott_menu == "4":
            #Kilépés a programból
            print("A program bezárása.")
            break
        else:
            #Érvénytelen választás esetén
            print("Érvénytelen választás. Kérlek, próbáld újra.")

#A főprogram indítása
if __name__ == "__main__":
    main()
