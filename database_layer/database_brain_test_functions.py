from database_layer.database import (
    Uzytkownik, Odbiorcy, Sprzedawca, Paragony, ProduktyParagon, Faktury, ProduktyFaktury, Kategoria, session
)
from sqlalchemy import and_, or_, between, func
from datetime import date
import random

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
            data_zakupu=date(2024, i+1, i+5),  # Ustalona data testowa
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
                paragon_id=paragon.id,
                kategoria_id=None,  # Zakładamy brak kategorii dla uproszczenia
                nazwa_produktu=produkt["nazwa_produktu"],
                cena_suma=produkt["cena_suma"],
                ilosc=ilosc
            )
            session.add(produkt_paragon)
            session.commit()


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