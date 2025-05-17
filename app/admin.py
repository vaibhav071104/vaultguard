from sqlalchemy import func
from app.models import Transaction, User, Wallet

def get_flagged_transactions(db):
    return db.query(Transaction).filter(Transaction.flagged == True).all()

def get_total_balances(db):
    return db.query(func.sum(Wallet.balance)).scalar()

def get_top_users(db, limit=10):
    return db.query(User).join(Wallet).order_by(Wallet.balance.desc()).limit(limit).all()
