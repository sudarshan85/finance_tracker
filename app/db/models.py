# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # 'expense' or 'income'
    monthly_budget = Column(Float)
    is_default = Column(Boolean, default=False)
    goal_amount = Column(Float, nullable=True)

    transactions = relationship("Transaction", back_populates="category")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # 'checking', 'savings', 'credit_card', etc.
    balance = Column(Float)

    transactions = relationship("Transaction", back_populates="account")

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    user_defined = Column(Boolean, default=True)

    transactions = relationship("Transaction", back_populates="store")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    amount = Column(Float)
    description = Column(String)
    memo = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    store = relationship("Store", back_populates="transactions")

class BudgetAllocation(Base):
    __tablename__ = "budget_allocations"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    amount = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category")