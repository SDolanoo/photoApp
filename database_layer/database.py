from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()

# Association table for the many-to-many relationship between Users and Groups
user_receipts = Table('user_receipts', Base.metadata,
                      Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                      Column('receipt_id', Integer, ForeignKey('receipts.id'), primary_key=True)
                      )

# UserReports junction table
user_invoices = Table('user_invoices', Base.metadata,
                      Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                      Column('invoice_id', Integer, ForeignKey('invoices.id'), primary_key=True)
                     )


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed passwords
    invoices = relationship('Invoices', secondary=user_invoices, back_populates='users')
    receipts = relationship('Receipts', secondary=user_receipts, back_populates='users')


class Receipts(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_name = Column(String(100), nullable=False)
    receipt_description = Column(Text)
    receipt_amount = Column(String(100), nullable=False)
    users = relationship('Users', secondary=user_receipts, back_populates='receipts')


class Invoices(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_name = Column(String(100), unique=True, nullable=False)
    invoice_description = Column(Text)
    invoice_amount = Column(String(100), nullable=False)
    users = relationship('Users', secondary=user_invoices, back_populates='invoices')


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///paragon_database.db')

# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)

# Bind the engine to the session and create a configured "Session" class
Session = sessionmaker(bind=engine)
# Create a Session
session = Session()
