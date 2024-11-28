from database_layer.database import (
    Uzytkownik, Odbiorcy, Sprzedawca, Paragony, ProduktyParagon, Faktury, ProduktyFaktury, Kategoria, session
)
from datetime import date
import random

# ########################################### TESTY ###########################################
# ########################################### TESTY ###########################################
# ########################################### TESTY ###########################################


# Funkcja do dodawania testowych paragonów
def add_test_receipt():
    """
    Dodaje 10 przykładowych paragonów do bazy danych.
    """
    # Przykładowi użytkownicy
    uzytkownicy = session.query(Uzytkownik).all()
    if not uzytkownicy:
        raise ValueError("Brak użytkowników w bazie danych. Najpierw dodaj użytkowników.")

    # Tworzenie 10 testowych paragonów
    testowe_kwoty = [100.50, 200.75, 50.30, 80.99, 120.00, 300.00, 15.75, 60.45, 500.20, 250.10]
    for i in range(10):
        paragon = Paragony(
            uzytkownik_id=random.choice(uzytkownicy).id,
            data_zakupu=date(2024, 11, 28),  # Ustalona data testowa
            nazwa_sklepu=f"Sklep {i}",
            kwota_calkowita=random.choice(testowe_kwoty)
        )
        session.add(paragon)

    # Zatwierdzanie transakcji
    session.commit()
    print("Dodano 10 testowych paragonów.")


def add_test_recipe_products():
    """
    Dodaje produkty do istniejących paragonów w bazie danych.
    Każdy paragon otrzymuje losową liczbę produktów.
    Najpierw add_test_recipe
    """
    # Pobieramy istniejące paragony
    paragony = session.query(Paragony).all()
    if not paragony:
        raise ValueError("Brak paragonów w bazie danych. Najpierw dodaj paragony.")

    # Przykładowe dane produktów
    produkty_testowe = [
        {"nazwa_produktu": "Mleko", "cena_suma": 3.50},
        {"nazwa_produktu": "Chleb", "cena_suma": 2.80},
        {"nazwa_produktu": "Masło", "cena_suma": 7.50},
        {"nazwa_produktu": "Ser", "cena_suma": 10.99},
        {"nazwa_produktu": "Kawa", "cena_suma": 25.00},
        {"nazwa_produktu": "Cukier", "cena_suma": 5.00},
        {"nazwa_produktu": "Czekolada", "cena_suma": 8.50},
        {"nazwa_produktu": "Woda mineralna", "cena_suma": 2.00},
        {"nazwa_produktu": "Sok pomarańczowy", "cena_suma": 4.50},
        {"nazwa_produktu": "Makaron", "cena_suma": 6.00}
    ]

    # Tworzenie produktów dla każdego paragonu
    for paragon in paragony:
        liczba_produktow = random.randint(1, 5)  # Każdy paragon dostanie od 1 do 5 produktów
        for _ in range(liczba_produktow):
            produkt = random.choice(produkty_testowe)
            ilosc = random.randint(1, 10)  # Losowa ilość od 1 do 10

            produkt_paragon = ProduktyParagon(
                id_paragonu=paragon.id,
                id_kategorii=None,  # Zakładamy brak kategorii dla uproszczenia
                nazwa_produktu=produkt["nazwa_produktu"],
                cena_suma=produkt["cena_suma"],
                ilosc=ilosc,
                kategoria_id=None
            )
            session.add(produkt_paragon)
            session.commit()


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


def add_recipe(uzytkownik_id: int, data: list, nazwa_sklepu: str, kwota_calkowita: str, produkty: list) -> None:
    def add_product(id_paragonu: int):
        # Dodawanie produktów
        for produkt in produkty:
            try:
                nazwa_produktu, cena_suma, ilosc = produkt
                ilosc = int(ilosc)  # Upewniamy się, że ilość jest liczbą całkowitą
                cena_jednostkowa = round(float(cena_suma) / ilosc, 2)  # Obliczamy cenę jednostkową
            except (ValueError, TypeError):
                raise ValueError(
                    "Każdy produkt musi być w formacie [nazwa_produktu, cena_suma, ilosc] z poprawnymi danymi.")

            # Tworzenie obiektu produktu
            produkt_paragon = ProduktyParagon(
                id_paragonu=id_paragonu,
                nazwa_produktu=nazwa_produktu,
                cena_jednostkowa=cena_jednostkowa,
                ilosc=ilosc,
                id_kategorii=None,  # Zakładamy brak kategorii
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
        data_zakupu=date(data[0], data[1], data[2]),  # Ustalona data testowa
        nazwa_sklepu=nazwa_sklepu,
        kwota_calkowita=kwota_calkowita
    )
    session.add(paragon)
    session.commit()

    add_product(id_paragonu=paragon.id)


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
        .filter(Paragony.uzytkownik_id == uzytkownik_id)
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
            .filter(ProduktyParagon.id_paragonu == paragon.id)
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
                    "cena_jednostkowa": produkt.cena_suma,
                    "ilosc": produkt.ilosc,
                }
                for produkt in produkty
            ],
        }
        result.append(paragon_data)

    return result


def add_test_invoices(
    uzytkownik_id: int,
    odbiorca_data: dict,
    sprzedawca_data: dict,
    faktura_data: dict
) -> None:
    """
        Dodaje 10 przykładowych paragonów do bazy danych.
        """
    # Przykładowi użytkownicy
    uzytkownicy = session.query(Uzytkownik).all()
    if not uzytkownicy:
        raise ValueError("Brak użytkowników w bazie danych. Najpierw dodaj użytkowników.")

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
        data_sprzedazy=faktura_data.get("data_sprzedaży"),
        razem_netto=faktura_data["razem_netto"],
        razem_stawka=faktura_data["razem_stawka"],
        razem_podatek=faktura_data["razem_podatek"],
        razem_brutto=faktura_data["razem_brutto"],
        waluta=faktura_data["waluta"],
        forma_platnosci=faktura_data["forma_płatnosci"]
    )
    session.add(faktura)
    session.flush()  # Upewnij się, że faktura ma ID

    # Zatwierdzanie transakcji
    session.commit()
    print("Dodano tekstowa fakture.")


def add_test_invoice_products():
    """
        Dodaje produkty do istniejących faktur w bazie danych.
        Każda faktura otrzymuje losową liczbę produktów.
        Najpierw add_test_invoice
    """

    faktury = session.query(Faktury).all()
    if not faktury:
        raise ValueError("Brak paragonów w bazie danych. Najpierw dodaj paragony.")

    produkty_testowe = [
        {
            "nazwa_produktu": "Produkt A",
            "jednostka_miary": "szt.",
            "ilosc": "10",
            "wartosc_netto": "50.00",
            "stawka_vat": "23%",
            "podatek_vat": "11.50",
            "brutto": "61.50"
        },
        {
            "nazwa_produktu": "Produkt B",
            "jednostka_miary": "kg",
            "ilosc": "5",
            "wartosc_netto": "100.00",
            "stawka_vat": "23%",
            "podatek_vat": "23.00",
            "brutto": "123.00"
        }
    ]

    for faktura in faktury:
        # Dodawanie produktów do faktury
        for produkt_data in produkty_testowe:
            produkt = ProduktyFaktury(
                faktura_id=faktura.id,
                nazwa_produktu=produkt_data["nazwa_produktu"],
                jednostka_miary=produkt_data.get("jednostka_miary"),
                ilosc=produkt_data.get("ilosc"),
                wartosc_netto=produkt_data["wartosc_netto"],
                stawka_vat=produkt_data["stawka_vat"],
                podatek_vat=produkt_data["podatek_vat"],
                brutto=produkt_data["brutto"]
            )
            session.add(produkt)
            session.commit()


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
                id_paragonu=id_faktury,
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
        .filter(Faktury.uzytkownik_id == uzytkownik_id)
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
#                     "data_wystawienia": date(2024, 11, 28),
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