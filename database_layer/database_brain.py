from database_layer.database import (
    Uzytkownik, Odbiorcy, Sprzedawca, Paragony, ProduktyParagon, Faktury, ProduktyFaktury, Kategoria, session
)
from sqlalchemy import and_, or_, between, func
from datetime import date
import random


def add_user(login: str, password: str, email: str):
    # Tworzenie nowego użytkownika
    new_user = Uzytkownik(
        login=login,
        password=password,
        email=email
    )

    # Dodanie użytkownika do sesji
    session.add(new_user)

    # Zatwierdzanie transakcji
    session.commit()
    print(f"Użytkownik '{login}' został dodany do bazy danych.")


def add_recipe(uzytkownik_id: int, recipe_date: list, nazwa_sklepu: str, kwota_calkowita: str, produkty: list) -> None:
    def add_product(paragon_id: int):
        # Dodawanie produktów
        for produkt in produkty:
            nazwa_produktu = produkt['nazwa_produktu']
            cena_suma = produkt['cena_suma']
            ilosc = produkt['ilosc']
            # Tworzenie obiektu produktu
            produkt_paragon = ProduktyParagon(
                paragon_id=paragon_id,
                nazwa_produktu=nazwa_produktu,
                cena_suma=cena_suma,
                ilosc=ilosc,
                kategoria_id=None
            )
            session.add(produkt_paragon)

            # Zatwierdzanie transakcji
            session.commit()
    """
        :param data: eg. [2024, 11, 28]/ [YYYY, MM, DD]
    """
    paragon = Paragony(
        uzytkownik_id=uzytkownik_id,
        data_zakupu=date(recipe_date[0], recipe_date[1], recipe_date[2]),  # Ustalona data testowa
        nazwa_sklepu=nazwa_sklepu,
        kwota_calkowita=kwota_calkowita
    )
    session.add(paragon)
    session.commit()

    add_product(paragon_id=paragon.id)


def list_all_receipts(uzytkownik_id: int) -> list:
    """
    Zwraca listę paragonów powiązanych z określonym użytkownikiem.

    Args:
        uzytkownik_id (int): Identyfikator użytkownika.

    Returns:
        list: Lista słowników, gdzie każdy słownik zawiera dane paragonu
              i listę powiązanych produktów.
    """
    # Pobierz wszystkie paragony dla danego użytkownika
    paragony = (
        session.query(Paragony)
        .filter(Paragony.uzytkownik_id == uzytkownik_id).order_by(Paragony.data_zakupu.desc())
        .all()
    )

    if not paragony:
        print("Brak paragonów dla podanego użytkownika.")
        return []

    # Lista wyników
    result = []
    for paragon in paragony:
        # Pobierz produkty powiązane z paragonem
        produkty = (
            session.query(ProduktyParagon)
            .filter(ProduktyParagon.paragon_id == paragon.id)
            .all()
        )
        # Tworzenie słownika z danymi paragonu i produktami
        paragon_data = {
            "id": paragon.id,
            "data_zakupu": paragon.data_zakupu,
            "nazwa_sklepu": paragon.nazwa_sklepu,
            "kwota_calkowita": paragon.kwota_calkowita,
            "produkty": [
                {
                    "nazwa_produktu": produkt.nazwa_produktu,
                    "cena_suma": produkt.cena_suma,
                    "ilosc": produkt.ilosc,
                }
                for produkt in produkty
            ],
        }
        result.append(paragon_data)

    return result


def add_invoice(
        uzytkownik_id: int,
        odbiorca_data: dict,
        sprzedawca_data: dict,
        faktura_data: dict,
        produkty: list
) -> None:
    def add_product(id_faktury: int):
        for produkt in produkty:
            try:
                nazwa_produktu, jednostka_miary, ilosc, wartosc_netto, stawka_vat, podatek_vat, brutto = produkt
                ilosc = int(ilosc)  # Upewniamy się, że ilość jest liczbą całkowitą
            except (ValueError, TypeError):
                raise ValueError(
                    "Każdy produkt musi być w formacie\
                    [nazwa_produktu, jednostka_miary, ilosc, wartosc_netto, stawka_vat, podatek_vat, brutto]\
                     z poprawnymi danymi.")
            # Tworzenie obiektu produktu
            produkt_faktura = ProduktyFaktury(
                paragon_id=id_faktury,
                nazwa_produktu=nazwa_produktu,
                jednostka_miary=jednostka_miary,
                ilosc=ilosc,
                wartosc_netto=wartosc_netto,
                stawka_vat=stawka_vat,
                podatek_vat=podatek_vat,
                brutto=brutto
            )
            session.add(produkt_faktura)

            # Zatwierdzanie transakcji
            session.commit()

    # Dodawanie odbiorcy, jeśli nie istnieje
    odbiorca = (
        session.query(Odbiorcy)
        .filter_by(nip=odbiorca_data["nip"])
        .first()
    )
    if not odbiorca:
        odbiorca = Odbiorcy(
            nazwa=odbiorca_data["nazwa"],
            nip=odbiorca_data["nip"],
            adres=odbiorca_data["adres"]
        )
        session.add(odbiorca)
        session.flush()  # Upewnij się, że odbiorca ma ID

    # Dodawanie sprzedawcy, jeśli nie istnieje
    sprzedawca = (
        session.query(Sprzedawca)
        .filter_by(nip=sprzedawca_data["nip"])
        .first()
    )
    if not sprzedawca:
        sprzedawca = Sprzedawca(
            nazwa=sprzedawca_data["nazwa"],
            nip=sprzedawca_data["nip"],
            adres=sprzedawca_data["adres"]
        )
        session.add(sprzedawca)
        session.flush()  # Upewnij się, że sprzedawca ma ID

    # Dodawanie faktury
    faktura = Faktury(
        uzytkownik_id=uzytkownik_id,
        odbiorca_id=odbiorca.id,
        sprzedawca_id=sprzedawca.id,
        numer_faktury=faktura_data["numer_faktury"],
        nr_rachunku_bankowego=faktura_data["nr_rachunku_bankowego"],
        data_wystawienia=faktura_data["data_wystawienia"],
        data_sprzedaży=faktura_data.get("data_sprzedaży"),
        razem_netto=faktura_data["razem_netto"],
        razem_stawka=faktura_data["razem_stawka"],
        razem_podatek=faktura_data["razem_podatek"],
        razem_brutto=faktura_data["razem_brutto"],
        waluta=faktura_data["waluta"],
        forma_płatnosci=faktura_data["forma_płatnosci"]
    )
    session.add(faktura)
    session.flush()  # Upewnij się, że faktura ma ID

    # Zatwierdzanie transakcji
    session.commit()
    print("Dodano fakture.")
    print("Dodaje produkty.")

    add_product(id_faktury=faktura.id)


def list_all_invoices(uzytkownik_id: int) -> list:
    """
    Zwraca listę paragonów powiązanych z określonym użytkownikiem.

    Args:
        uzytkownik_id (int): Identyfikator użytkownika.

    Returns:
        list: Lista słowników, gdzie każdy słownik zawiera dane paragonu
              i listę powiązanych produktów.
    """
    # Pobierz wszystkie paragony dla danego użytkownika
    faktury = (
        session.query(Faktury)
        .filter(Faktury.uzytkownik_id == uzytkownik_id).order_by(Faktury.data_wystawienia.desc())
        .all()
    )

    if not faktury:
        print("Brak faktur dla podanego użytkownika.")
        return []

    # Lista wyników
    result = []
    for faktura in faktury:
        # Pobierz produkty powiązane z paragonem
        produkty = (
            session.query(ProduktyFaktury)
            .filter(ProduktyFaktury.faktura_id == faktura.id)
            .all()
        )
        # Tworzenie słownika z danymi paragonu i produktami
        faktura_data = {
            "id": faktura.id,
            "numer_faktury": faktura.numer_faktury,
            "data_wystawienia": faktura.data_wystawienia,
            "razem_netto": faktura.razem_netto,
            "razem_stawka": faktura.razem_stawka,
            "razem_podatek": faktura.razem_podatek,
            "razem_brutto": faktura.razem_brutto,
            "produkty": [
                {
                    "nazwa_produktu": produkt.nazwa_produktu,
                    "jednostka_miary": produkt.jednostka_miary,
                    "ilosc": produkt.ilosc,
                    "wartosc_netto": produkt.wartosc_netto,
                    "stawka_vat": produkt.stawka_vat,
                    "podatek_vat": produkt.podatek_vat,
                    "brutto": produkt.brutto,
                }
                for produkt in produkty
            ],
        }
        result.append(faktura_data)

    return result

def search_for_documents(doc_type: str, date_from: date, date_to: date, price_from: str, price_to: str,
                         uzytkownik_id=1, odbiorcy=None, sprzedawcy=None, sklepy=None):
    if doc_type == 'paragon':
        query = session.query(Paragony)
        query = query.filter(Paragony.uzytkownik_id == uzytkownik_id)
        if date_from and date_to:
            query = query.filter(Paragony.data_zakupu.between(date_from, date_to))
        if price_from and price_to:
            query = query.filter(Paragony.kwota_calkowita.between(price_from, price_to))
        if sklepy and sklepy != "Wszyscy":
            query = query.filter(Paragony.nazwa_sklepu.in_(sklepy))
        query = query.order_by(Paragony.data_zakupu.desc())
    elif doc_type == 'faktura':
        query = session.query(Faktury)
        query = query.filter(Faktury.uzytkownik_id == uzytkownik_id)
        if date_from and date_to:
            query = query.filter(Faktury.data_wystawienia.between(cleft=date_from, cright=date_to))
        if price_from and price_to:
            query = query.filter(Faktury.razem_brutto.between(price_from, price_to))
        if odbiorcy:
            query = query.join(Odbiorcy).filter(Odbiorcy.nazwa.in_(odbiorcy))
        if sprzedawcy:
            query = query.join(Sprzedawca).filter(Sprzedawca.nazwa.in_(sprzedawcy))
        query = query.order_by(Faktury.data_wystawienia.desc())
    else:
        raise ValueError("Nieprawidłowy typ dokumentu")

    return query.all()


def list_filtered_receipts(doc_type: str, date_from: date, date_to: date, price_from: str, price_to: str,
                         uzytkownik_id=1, odbiorcy=None, sprzedawcy=None, sklepy=None) -> list:
    paragony = search_for_documents(doc_type, date_from, date_to, price_from, price_to,
                                    uzytkownik_id=1, odbiorcy=None, sprzedawcy=None, sklepy=None)

    if not paragony:
        print("Brak paragonów dla podanego użytkownika.")
        return []

    # Lista wyników
    result = []
    for paragon in paragony:
        # Pobierz produkty powiązane z paragonem
        produkty = (
            session.query(ProduktyParagon)
            .filter(ProduktyParagon.paragon_id == paragon.id)
            .all()
        )
        # Tworzenie słownika z danymi paragonu i produktami
        paragon_data = {
            "id": paragon.id,
            "data_zakupu": paragon.data_zakupu,
            "nazwa_sklepu": paragon.nazwa_sklepu,
            "kwota_calkowita": paragon.kwota_calkowita,
            "produkty": [
                {
                    "nazwa_produktu": produkt.nazwa_produktu,
                    "cena_suma": produkt.cena_suma,
                    "ilosc": produkt.ilosc,
                }
                for produkt in produkty
            ],
        }
        result.append(paragon_data)
    return result

def list_filtered_invoice(doc_type: str, date_from: date, date_to: date, price_from: str, price_to: str,
                              uzytkownik_id=1, odbiorcy=None, sprzedawcy=None, sklepy=None) -> list:
    faktury = search_for_documents(doc_type, date_from, date_to, price_from, price_to,
                                    uzytkownik_id=1, odbiorcy=None, sprzedawcy=None, sklepy=None)

    if not faktury:
        print("Brak faktur dla podanego użytkownika.")
        return []

    # Lista wyników
    result = []
    for faktura in faktury:
        # Pobierz produkty powiązane z paragonem
        produkty = (
            session.query(ProduktyFaktury)
            .filter(ProduktyFaktury.faktura_id == faktura.id)
            .all()
        )
        # Tworzenie słownika z danymi paragonu i produktami
        faktura_data = {
            "id": faktura.id,
            "numer_faktury": faktura.numer_faktury,
            "data_wystawienia": faktura.data_wystawienia,
            "razem_netto": faktura.razem_netto,
            "razem_stawka": faktura.razem_stawka,
            "razem_podatek": faktura.razem_podatek,
            "razem_brutto": faktura.razem_brutto,
            "produkty": [
                {
                    "nazwa_produktu": produkt.nazwa_produktu,
                    "jednostka_miary": produkt.jednostka_miary,
                    "ilosc": produkt.ilosc,
                    "wartosc_netto": produkt.wartosc_netto,
                    "stawka_vat": produkt.stawka_vat,
                    "podatek_vat": produkt.podatek_vat,
                    "brutto": produkt.brutto,
                }
                for produkt in produkty
            ],
        }
        result.append(faktura_data)

    return result

# add_user(login="test", password="123", email="test@test.com")
# add_test_receipt()
# add_test_recipe_products()
# for i in range(10):
#     add_test_invoices(
#                 uzytkownik_id=1,  # ID użytkownika
#                 odbiorca_data={
#                     "nazwa": "Firma X",
#                     "nip": "1234567890",
#                     "adres": "ul. Przykładowa 1, Warszawa"
#                 },
#                 sprzedawca_data={
#                     "nazwa": "Firma Y",
#                     "nip": "0987654321",
#                     "adres": "ul. Testowa 2, Kraków"
#                 },
#                 faktura_data={
#                     "numer_faktury": f"FV/2024/11/00{i}",
#                     "nr_rachunku_bankowego": f"{i}{i} 3456 7890 1234 5678 9012 3456",
#                     "data_wystawienia": date(2024, i+1, i+3),
#                     "data_sprzedaży": None,
#                     "razem_netto": f"{i}000.00",
#                     "razem_stawka": "23%",
#                     "razem_podatek": "230.00",
#                     "razem_brutto": f"{i}230.00",
#                     "waluta": "PLN",
#                     "forma_płatnosci": "Przelew"
#                 },
#             )
# add_test_invoice_products()