from sqlalchemy import Column, String, Date, Numeric, Integer, ForeignKey, Text
from sqlalchemy_utils import ChoiceType
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(Text, nullable=False)
    email = Column(String(50), nullable=False)
    debt = relationship('Debt', back_populates='user')
    def __repr__(self):
        return '<User:{self.username}>'

class Debt(Base):
    TYPE = (
        ('OWED_TO', 'owed_to'),
        ('OWED_BY', 'owed_by'),
        ('INDIVIDUAL', 'individual')
    )

    VALYUTA = (
        ('UZS', 'uzs'),
        ('USD', 'usd'),
        ('EUR', 'eur'),
        ('RUB', 'rub'),
    )

    __tablename__ = 'debt'
    id = Column(Integer, primary_key=True)
    debt_type = Column(ChoiceType(TYPE), nullable=False, default='OWED_TO')
    debt_valyuta = Column(ChoiceType(VALYUTA), nullable=False, default='UZS')
    amount = Column(Numeric(12, 2), nullable=False)
    given_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    first_name = Column(String(50), nullable=False)
    phone= Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, back_populates='debt')

    def __repr__(self):
        return '<Debt:{self.debt_type}:{self.amount}>'



