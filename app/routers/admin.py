from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from app.admin import get_top_users
from app.models import Transaction, User, Wallet
from app.database import get_db
from app.schemas import TransactionOut
from app.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/flagged-transactions", response_model=List[TransactionOut])
def flagged_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.flagged == True, Transaction.deleted == False).all()

@router.get("/total-balances")
def total_balances(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Not authorized")
    total_sum = (
        db.query(func.sum(Wallet.balance))
        .join(User, Wallet.user_id == User.id)
        .filter(User.is_active == True, User.deleted == False)
        .scalar() or 0
    )
    return {"total_balance": total_sum}

@router.get("/top-users")
def top_users(db: Session = Depends(get_db), limit: int = 10):
    return get_top_users(db, limit)

# --- SOFT DELETE ENDPOINTS ---

@router.delete("/users/{user_id}")
def soft_delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Not authorized")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.deleted = True  # type: ignore
    db.commit()
    return {"msg": f"User {user_id} soft deleted"}

@router.delete("/transactions/{txn_id}")
def soft_delete_transaction_endpoint(
    txn_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Not authorized")
    txn = db.query(Transaction).filter(Transaction.id == txn_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    txn.deleted = True  # type: ignore
    db.commit()
    return {"msg": f"Transaction {txn_id} soft deleted"}
