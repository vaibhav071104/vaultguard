from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.crud import deposit, withdraw, transfer  # Added transfer
from app.schemas import TransactionCreate, TransactionOut, TransferRequest  # Added TransferRequest
from app.database import get_db
from app.models import User, Transaction

router = APIRouter()

@router.post("/deposit", response_model=TransactionOut)
def deposit_cash(
    txn: TransactionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return deposit(db, user, txn.amount)

@router.post("/withdraw", response_model=TransactionOut)
def withdraw_cash(
    txn: TransactionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return withdraw(db, user, txn.amount)

@router.post("/transfer", response_model=TransactionOut)
def transfer_funds(
    req: TransferRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recipient = db.query(User).filter(User.username == req.recipient_username).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    txn = transfer(db, user, recipient, req.amount)
    return txn

# --- Endpoint: Get current user's wallet balance ---
@router.get("/wallet/balance")
def get_my_balance(user: User = Depends(get_current_user)):
    if user.wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"balance": user.wallet.balance}

# --- Endpoint: Get current user's balance AND transaction history ---
@router.get("/wallet/history")
def get_my_wallet_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    transactions = (
        db.query(Transaction)
        .filter(Transaction.wallet_id == user.wallet.id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )
    return {
        "balance": user.wallet.balance,
        "transactions": [
            {
                "id": txn.id,
                "type": txn.type,
                "amount": txn.amount,
                "timestamp": txn.timestamp,
                "flagged": txn.flagged,
                "flag_reason": txn.flag_reason,
            }
            for txn in transactions
        ]
    }
