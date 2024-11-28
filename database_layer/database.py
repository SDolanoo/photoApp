from sqlalchemy import (
    create_engine, Column, Integer, String, Text, ForeignKey, Date, Float
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# Tabela Uzytkownik
class Uzytkownik(Base):
    __tablename__ = 'uzytkownik'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)

    paragony = relationship('Paragony', back_populates='uzytkownik')
    faktury = relationship('Faktury', back_populates='uzytkownik')


# Tabela Odbiorcy
class Odbiorcy(Base):
    __tablename__ = 'odbiorcy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nazwa = Column(Text, nullable=False, unique=True)
    nip = Column(Text, nullable=False, unique=True)
    adres = Column(Text, nullable=False)

    faktury = relationship('Faktury', back_populates='odbiorca')


# Tabela Sprzedawca
class Sprzedawca(Base):
    __tablename__ = 'sprzedawca'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nazwa = Column(Text, nullable=False)
    nip = Column(Text, unique=True, nullable=False)
    adres = Column(Text, nullable=False)

    faktury = relationship('Faktury', back_populates='sprzedawca')


# Tabela Paragony
class Paragony(Base):
    __tablename__ = 'paragony'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uzytkownik_id = Column(Integer, ForeignKey('uzytkownik.id'), nullable=False)
    data_zakupu = Column(Date, nullable=False)
    nazwa_sklepu = Column(Text, nullable=False)
    kwota_calkowita = Column(Float, nullable=False)

    uzytkownik = relationship('Uzytkownik', back_populates='paragony')
    produkty = relationship('ProduktyParagon', back_populates='paragon')


# Tabela Produkty_paragon
class ProduktyParagon(Base):
    __tablename__ = 'produkty_paragon'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_paragonu = Column(Integer, ForeignKey('paragony.id'), nullable=False)
    id_kategorii = Column(Integer, ForeignKey('kategoria.id'), nullable=True)
    nazwa_produktu = Column(Text, nullable=False)
    cena_suma = Column(Float, nullable=False)
    ilosc = Column(Integer, nullable=False)
    kategoria_id = Column(Integer)

    paragon = relationship('Paragony', back_populates='produkty')
    kategoria = relationship('Kategoria', back_populates='produkty')


# Tabela Faktury
class Faktury(Base):
    __tablename__ = 'faktury'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uzytkownik_id = Column(Integer, ForeignKey('uzytkownik.id'), nullable=False)
    odbiorca_id = Column(Integer, ForeignKey('odbiorcy.id'), nullable=False)
    sprzedawca_id = Column(Integer, ForeignKey('sprzedawca.id'), nullable=False)
    numer_faktury = Column(Text, nullable=False)
    nr_rachunku_bankowego = Column(Text, nullable=True)
    data_wystawienia = Column(Date, nullable=False)
    data_sprzedazy = Column(Date, nullable=True)
    razem_netto = Column(Text, nullable=False)
    razem_stawka = Column(Text, nullable=False)
    razem_podatek = Column(Text, nullable=False)
    razem_brutto = Column(Text, nullable=False)
    waluta = Column(Text, nullable=False)
    forma_platnosci = Column(Text, nullable=False)

    uzytkownik = relationship('Uzytkownik', back_populates='faktury')
    odbiorca = relationship('Odbiorcy', back_populates='faktury')
    sprzedawca = relationship('Sprzedawca', back_populates='faktury')
    produkty = relationship('ProduktyFaktury', back_populates='faktura')


# Tabela Produkty_faktury
class ProduktyFaktury(Base):
    __tablename__ = 'produkty_faktury'

    id = Column(Integer, primary_key=True, autoincrement=True)
    faktura_id = Column(Integer, ForeignKey('faktury.id'), nullable=False)
    nazwa_produktu = Column(Text, nullable=False)
    jednostka_miary = Column(Text, nullable=True)
    ilosc = Column(Text, nullable=True)
    wartosc_netto = Column(Text, nullable=False)
    stawka_vat = Column(Text, nullable=False)
    podatek_vat = Column(Text, nullable=False)
    brutto = Column(Text, nullable=False)

    faktura = relationship('Faktury', back_populates='produkty')


# Tabela Kategoria
class Kategoria(Base):
    __tablename__ = 'kategoria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nazwa = Column(Text, nullable=False)

    produkty = relationship('ProduktyParagon', back_populates='kategoria')


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///paragon_database.db')

# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)

# Bind the engine to the session and create a configured "Session" class
Session = sessionmaker(bind=engine)
# Create a Session
session = Session()
