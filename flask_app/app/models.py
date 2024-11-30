from typing import List
from flask import current_app
from sqlalchemy import Boolean, Date, Enum, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapper


class Base(DeclarativeBase):
    __abstract__ = True
    __allow_unmapped__ = True

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key = True)
    type = mapped_column(String(20))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='transactions')
    __mapper_args__ = {
        'polymorphic_identity': 'transaction',
        'polymorphic_on': type
    }

    def __repr__(self):
        return f'Transaction(id={self.id}, type={self.type})'

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(30))
    is_authenticated: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=True)

    transactions: Mapped[list['Transaction']] = relationship()

    __table_args__ = (UniqueConstraint(email, username),)
    @staticmethod
    def get_id():
        return str(id)
    
    def get_active(self):
        return self.is_active

    def __repr__(self) -> str:
        return f'User(id={self.id}, email={self.email}, username={self.username}, password={self.password}, is_authenticated={self.is_authenticated}, is_active={self.is_active}, is_anonymous={self.is_anonymous})'



class Receipt(Transaction):
    __tablename__ = "receipts"
    __mapper_args__ = {'polymorphic_identity': 'receipt'}

    id: Mapped[int] = mapped_column(ForeignKey('transactions.id'), primary_key=True)
    purchase_date = mapped_column(Date)
    store_name: Mapped[str] = mapped_column(String(30))
    total_amount: Mapped[str] = mapped_column(Float)

    def __repr__(self) -> str:
        return f'Receipt(id={self.id}, type={self.type} purchase_date={self.purchase_date}, store_name={self.store_name}, total_amount={self.total_amount})'

class Invoice(Transaction):
    __tablename__ = "invoices"
    __mapper_args__ = {'polymorphic_identity': 'invoice'}

    id: Mapped[int] = mapped_column(ForeignKey('transactions.id'), primary_key=True)
    purchase_date = mapped_column(Date)
    store_name: Mapped[str] = mapped_column(String(30))
    total_amount: Mapped[str] = mapped_column(Float)

    




def create_all():
    Base.metadata.create_all(current_app.config['ENGINE'])

def drop_all():
    Base.metadata.drop_all(current_app.config['ENGINE'])

session = Session(current_app.config['ENGINE'])



