from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.crud import transfer, get_transaction_history
from app.models import User, Transaction
from app.schemas import TransactionCreate, TransactionOut, WalletOut
from app.database import get_db

router = APIRouter()

@router.post("/transfer", response_model=TransactionOut)
def transfer_cash(
    txn: TransactionCreate, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    recipient = db.query(User).filter(User.username == txn.target_username).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return transfer(db, user, recipient, txn.amount)

@router.get("/history", response_model=WalletOut)
def get_history(
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    wallet = user.wallet
    transactions = get_transaction_history(db, user)
    
    # Ensure transactions match expected schema format
    transactions_out = [TransactionOut(**txn.__dict__) for txn in transactions]

    return WalletOut(balance=wallet.balance, transactions=transactions_out)
