from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User, Wallet, Transaction
from app.fraud import advanced_fraud_check
from app.utils import send_email_alert
from typing import List

def create_user(db: Session, username: str, hashed_password: str) -> User:
    """Create a new user and associated wallet."""
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Always create a wallet for the new user
    db_wallet = Wallet(user_id=db_user.id)
    db.add(db_wallet)
    db.commit()
    return db_user

def deposit(db: Session, user: User, amount: float) -> Transaction:
    """Deposit amount into user's wallet with fraud check and alert."""
    if not user.wallet:
        raise HTTPException(status_code=404, detail="Wallet not found for user")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid deposit amount")
    user.wallet.balance += amount
    transactions: List[Transaction] = db.query(Transaction).filter(
        Transaction.wallet_id == user.wallet.id,
        Transaction.deleted == False
    ).all()
    flags = advanced_fraud_check(transactions, amount, txn_type="deposit")
    flagged = bool(flags)
    txn = Transaction(
        wallet_id=user.wallet.id,
        type="deposit",
        amount=amount,
        flagged=flagged,
        flag_reason=", ".join(flags) if flagged else None
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    if flagged:
        send_email_alert(
            to_email="admin@example.com",
            subject="Suspicious Transaction Detected",
            message=f"User {user.username} made a flagged deposit of {amount}. Reason: {', '.join(flags)}"
        )
    return txn

def withdraw(db: Session, user: User, amount: float) -> Transaction:
    """Withdraw amount from user's wallet with fraud check and alert."""
    if not user.wallet:
        raise HTTPException(status_code=404, detail="Wallet not found for user")
    if amount <= 0 or user.wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds or invalid amount")
    user.wallet.balance -= amount
    transactions: List[Transaction] = db.query(Transaction).filter(
        Transaction.wallet_id == user.wallet.id,
        Transaction.deleted == False
    ).all()
    flags = advanced_fraud_check(transactions, amount, txn_type="withdraw")
    flagged = bool(flags)
    txn = Transaction(
        wallet_id=user.wallet.id,
        type="withdraw",
        amount=amount,
        flagged=flagged,
        flag_reason=", ".join(flags) if flagged else None
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    if flagged:
        send_email_alert(
            to_email="admin@example.com",
            subject="Suspicious Transaction Detected",
            message=f"User {user.username} made a flagged withdrawal of {amount}. Reason: {', '.join(flags)}"
        )
    return txn

def transfer(db: Session, sender: User, recipient: User, amount: float) -> Transaction:
    """Transfer amount from sender to recipient with fraud check and alert."""
    if not sender.wallet or not recipient.wallet:
        raise HTTPException(status_code=404, detail="Sender or recipient wallet not found")
    if amount <= 0 or sender.wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds or invalid amount")
    sender.wallet.balance -= amount
    recipient.wallet.balance += amount
    transactions: List[Transaction] = db.query(Transaction).filter(
        Transaction.wallet_id == sender.wallet.id,
        Transaction.deleted == False
    ).all()
    flags = advanced_fraud_check(transactions, amount, txn_type="transfer")
    flagged = bool(flags)
    txn = Transaction(
        wallet_id=sender.wallet.id,
        type="transfer",
        amount=amount,
        target_wallet_id=recipient.wallet.id,
        flagged=flagged,
        flag_reason=", ".join(flags) if flagged else None
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    if flagged:
        send_email_alert(
            to_email="admin@example.com",
            subject="Suspicious Transaction Detected",
            message=f"User {sender.username} made a flagged transfer of {amount} to {recipient.username}. Reason: {', '.join(flags)}"
        )
    return txn

def get_transaction_history(db: Session, user: User) -> List[Transaction]:
    """Get non-deleted transaction history for a user."""
    return db.query(Transaction).filter(
        Transaction.wallet_id == user.wallet.id,
        Transaction.deleted == False
    ).all()

def soft_delete_user(db: Session, user_id: int) -> None:
    """Soft delete a user by setting deleted flag."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.deleted = True  # type: ignore
    db.commit()

def soft_delete_transaction(db: Session, txn_id: int) -> None:
    """Soft delete a transaction by setting deleted flag."""
    txn = db.query(Transaction).filter(Transaction.id == txn_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    txn.deleted = True  # type: ignore
    db.commit()
