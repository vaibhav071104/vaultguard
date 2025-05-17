from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)  # Soft delete
    wallet = relationship("Wallet", back_populates="user", uselist=False)

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    balance = Column(Float, default=0.0)
    user = relationship("User", back_populates="wallet")
    transactions = relationship("Transaction", back_populates="wallet")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    type = Column(String)  # deposit, withdraw, transfer
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    target_wallet_id = Column(Integer, nullable=True)
    flagged = Column(Boolean, default=False)
    flag_reason = Column(String, nullable=True)
    deleted = Column(Boolean, default=False)  # Soft delete
    wallet = relationship("Wallet", back_populates="transactions")
